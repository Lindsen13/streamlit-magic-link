from datetime import datetime, timedelta
from typing import Optional
from unittest.mock import MagicMock, patch

import mongomock

from src.magiclink import StreamlitMagicLink
from src.models import User
from src.utils import (
    get_user_by_email,
    get_user_by_id,
    insert_magic_link,
    update_magic_link,
    update_user,
)


def test_initiate_magic_link() -> None:
    """Test initiating a magic link."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    magic_link_auth = StreamlitMagicLink(mongo_client, base_url)

    assert magic_link_auth is not None
    assert magic_link_auth.mongo_client == mongo_client
    assert magic_link_auth.base_url == base_url
    assert magic_link_auth.cookie_controller is not None
    assert magic_link_auth.user is None


def test_initiate_magic_link_with_existing_cookie_placed() -> None:
    """Test initiating a magic link."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    sample_user = _set_user(mongo_client)
    cookie_controller.get.return_value = sample_user.model_dump()

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    assert magic_link_auth is not None
    assert magic_link_auth.mongo_client == mongo_client
    assert magic_link_auth.base_url == base_url
    assert magic_link_auth.cookie_controller is not None
    assert magic_link_auth.user["id"] == sample_user.id
    assert magic_link_auth.user["email"] == sample_user.email


def test_authenticate() -> None:
    """Test user authentication."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url)

    sample_mail = "sample@mail.com"
    with patch("src.magiclink.st.toast") as mock_toast:
        magic_link_auth.authenticate(sample_mail)
        mock_toast.assert_called_once_with(
            f"A magic link has been sent to {sample_mail}. Please check your inbox.",
            icon=":material/check:",
        )


def test_sign_in() -> None:
    """Test signing in a user."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    sample_user = _set_user(mongo_client)
    cookie_controller.get.return_value = sample_user.model_dump()

    magic_link = insert_magic_link(mongo_client, sample_user.id)

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    with patch("src.magiclink.st") as mock_streamlit:
        mock_toast = MagicMock()
        mock_streamlit.query_params.get.return_value = magic_link.token
        mock_streamlit.toast = mock_toast
        magic_link_auth.sign_in()

        assert mock_streamlit.query_params.clear.called
        mock_toast.assert_called_once_with(
            "You are now signed in.", icon=":material/check:"
        )


def test_sign_in_without_token() -> None:
    """Test signing in without a token."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    magic_link_auth = StreamlitMagicLink(mongo_client, base_url)

    with patch("src.magiclink.st") as mock_streamlit:
        mock_streamlit.query_params.get.return_value = None
        magic_link_auth.sign_in()

        mock_streamlit.query_params.clear.assert_not_called()


def test_sign_in_without_user() -> None:
    """Test signing in without a user."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    magic_link = insert_magic_link(mongo_client, "fake_user_id")

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    with patch("src.magiclink.st") as mock_streamlit:
        mock_toast = MagicMock()
        mock_streamlit.query_params.get.return_value = magic_link.token
        mock_streamlit.toast = mock_toast
        magic_link_auth.sign_in()

        assert mock_streamlit.query_params.clear.called
        mock_toast.assert_called_once_with(
            "Invalid or expired magic link.", icon=":material/error:"
        )


def test_sign_out() -> None:
    """Test signing out a user."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    sample_user = _set_user(mongo_client)
    cookie_controller.get.return_value = sample_user.model_dump()

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    with patch("src.magiclink.st") as mock_streamlit:
        mock_toast = MagicMock()
        mock_streamlit.toast = mock_toast
        assert magic_link_auth.user is not None

        magic_link_auth.sign_out()

        cookie_controller.remove.assert_called_once_with("user")
        mock_toast.assert_called_once_with(
            "You are now signed out.", icon=":material/check:"
        )


def test_update_user() -> None:
    """Test updating user information."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    sample_user = _set_user(mongo_client)
    cookie_controller.get.return_value = sample_user.model_dump()

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    with patch("src.magiclink.st") as mock_streamlit:
        mock_toast = MagicMock()
        mock_streamlit.toast = mock_toast
        magic_link_auth.update_user(name="New Name")

    updated_user = get_user_by_id(mongo_client, sample_user.id)
    assert updated_user is not None
    assert updated_user.name == "New Name"


def test_update_user_without_user() -> None:
    """Test updating user information without a user."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    cookie_controller.get.return_value = None

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    with patch("src.magiclink.st") as mock_streamlit:
        mock_toast = MagicMock()
        mock_streamlit.toast = mock_toast
        magic_link_auth.update_user(name="New Name")

        mock_toast.assert_not_called()


def test_delete_user() -> None:
    """Test deleting a user."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    sample_user = _set_user(mongo_client)
    cookie_controller.get.return_value = sample_user.model_dump()

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    with patch("src.magiclink.st") as mock_streamlit:
        mock_toast = MagicMock()
        mock_streamlit.toast = mock_toast
        magic_link_auth.delete_user()

    retrieved_user = get_user_by_id(mongo_client, sample_user.id)
    assert not retrieved_user
    assert mock_streamlit.rerun.called
    mock_toast.assert_called_once_with(
        "User deleted successfully!", icon=":material/check:"
    )


def test_delete_user_without_user() -> None:
    """Test deleting a user without a user."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    cookie_controller.get.return_value = None

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    with patch("src.magiclink.st") as mock_streamlit:
        mock_toast = MagicMock()
        mock_streamlit.toast = mock_toast
        magic_link_auth.delete_user()

    assert mock_streamlit.rerun.not_called
    mock_toast.assert_not_called()


def test_sync_user() -> None:
    """Test syncing user information."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    sample_user = _set_user(mongo_client)
    cookie_controller.get.return_value = sample_user.model_dump()

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    with patch("src.magiclink.st") as mock_streamlit:
        mock_toast = MagicMock()
        mock_streamlit.toast = mock_toast

        sample_user.name = "Updated Name"
        updated_user = update_user(mongo_client, sample_user)
        magic_link_auth._sync_user()

    assert updated_user is not None
    assert cookie_controller.set.called__once_with("user", updated_user.model_dump())


def test_sync_user_without_user() -> None:
    """Test syncing user information without a user."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    cookie_controller.get.return_value = None

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    magic_link_auth._sync_user()

    assert cookie_controller.set.not_called


def test_set_user() -> None:
    """Test setting a user."""
    sample_user = _set_user(mongomock.MongoClient())

    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    magic_link_auth._set_user(sample_user)
    assert cookie_controller.set.called_once_with("user", sample_user.model_dump())


def test_remove_user() -> None:
    """Test removing a user."""
    sample_user = _set_user(mongomock.MongoClient())

    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    magic_link_auth._remove_user()
    assert cookie_controller.remove.called_once_with("user", sample_user.model_dump())


def test_handle_magic_link() -> None:
    """Test handling a magic link."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    sample_user = _set_user(mongo_client)
    magic_link = insert_magic_link(mongo_client, sample_user.id)

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    retrieved_user = magic_link_auth._handle_magic_link(magic_link.token)

    assert retrieved_user is not None
    assert retrieved_user.id == sample_user.id


def test_handle_magic_link_invalid_token() -> None:
    """Test handling a magic link with an invalid token."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    retrieved_user = magic_link_auth._handle_magic_link("invalid_token")

    assert retrieved_user is None

def test_handle_magic_link_expired_token() -> None:
    """Test handling a magic link with an expired token."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    sample_user = _set_user(mongo_client)
    magic_link = insert_magic_link(mongo_client, sample_user.id)
    magic_link.expiration_time = datetime.now() - timedelta(days=1)
    update_magic_link(mongo_client, magic_link)

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    retrieved_user = magic_link_auth._handle_magic_link(magic_link.token)

    assert retrieved_user is None

def test_handle_magic_link_without_user() -> None:
    """Test handling a magic link without a user."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()
    base_url = "https://example.com"
    cookie_controller = MagicMock()

    magic_link = insert_magic_link(mongo_client, "some_invalid_user_id")

    magic_link_auth = StreamlitMagicLink(mongo_client, base_url, cookie_controller)

    retrieved_user = magic_link_auth._handle_magic_link(magic_link.token)

    assert retrieved_user is None

def test_validate_magic_link() -> None:
    """Test validating a magic link."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()

    sample_user = _set_user(mongo_client)
    magic_link = insert_magic_link(mongo_client, sample_user.id)

    magic_link_auth = StreamlitMagicLink(mongo_client, "")

    validated = magic_link_auth._validate_magic_link(magic_link, magic_link.token)

    assert validated is True


def test_validate_magic_link_used_token() -> None:
    """Test validating a magic link with a used token."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()

    sample_user = _set_user(mongo_client)
    magic_link = insert_magic_link(mongo_client, sample_user.id)
    magic_link.is_used = True
    update_magic_link(mongo_client, magic_link)

    magic_link_auth = StreamlitMagicLink(mongo_client, "")

    validated = magic_link_auth._validate_magic_link(magic_link, magic_link.token)

    assert validated is False

def test_validate_magic_link_expired_token() -> None:
    """Test validating a magic link with an expired token."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()

    sample_user = _set_user(mongo_client)
    magic_link = insert_magic_link(mongo_client, sample_user.id)
    magic_link.expiration_time = datetime.now() - timedelta(days=1)
    update_magic_link(mongo_client, magic_link)

    magic_link_auth = StreamlitMagicLink(mongo_client, "")

    validated = magic_link_auth._validate_magic_link(magic_link, magic_link.token)

    assert validated is False

def test_send_magic_link() -> None:
    """Test sending a magic link."""
    mongo_client: mongomock.MongoClient = mongomock.MongoClient()

    email = "sample@mail.com"

    magic_link_auth = StreamlitMagicLink(mongo_client, "")

    magic_link_auth._send_magic_link(email)

    created_user = get_user_by_email(mongo_client, email)
    assert created_user is not None
    assert created_user.email == email

    created_magic_link = mongo_client["streamlit-magic-link"]["magic-links"].find_one()
    assert created_magic_link is not None
    assert created_magic_link["user_id"] == created_user.id


def _set_user(
    mongo_client: mongomock.MongoClient,
    user: Optional[User] = None,
) -> User:
    """Set a user in the database."""
    if not user:
        user = User(email="sample@mail.com")
    mongo_client["streamlit-magic-link"]["users"].insert_one(user.model_dump())
    return user
