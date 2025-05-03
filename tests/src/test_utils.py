import mongomock
from src.utils import (
    insert_user,
    get_user_by_id,
    get_user_by_email,
    update_user,
    delete_user,
    create_or_retrieve_user,
    insert_magic_link,
    get_magic_link_by_token,
    update_magic_link,
)
from src.models import User


def test_insert_user()-> None:
    """
    Test the insert_user function.
    """
    client: mongomock.MongoClient = mongomock.MongoClient()
    user = User(email="sample@mail.com")
    inserted_user = insert_user(client, user)

    retrieved_user = get_user_by_id(client, inserted_user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == inserted_user.id
    assert retrieved_user.email == inserted_user.email

def test_get_user_by_id()-> None:
    """
    Test the get_user_by_id function.
    """
    client: mongomock.MongoClient = mongomock.MongoClient()
    user = User(email="sample@mail.com")
    insert_user(client, user)

    retrieved_user = get_user_by_id(client, user.id)
    assert retrieved_user is not None
    assert retrieved_user.email == user.email
    assert retrieved_user.id == user.id

def test_get_user_by_email() -> None:
    """
    Test the get_user_by_email function.
    """
    client: mongomock.MongoClient = mongomock.MongoClient()
    user = User(email="sample@mail.com")
    insert_user(client, user)

    retrieved_user = get_user_by_email(client, "sample@mail.com")
    assert retrieved_user is not None
    assert retrieved_user.email == "sample@mail.com"


def test_update_user()-> None:
    """
    Test the update_user function.
    """
    client: mongomock.MongoClient = mongomock.MongoClient()
    user = User(email="sample@mail.com")
    insert_user(client, user)

    user.email = "updated@mail.com"
    updated_user = update_user(client, user)

    assert updated_user is not None
    assert updated_user.email == "updated@mail.com"
    assert client["streamlit-magic-link"]["users"].find_one({"email": "updated@mail.com"}) is not None


def test_delete_user()-> None:
    """
    Test the delete_user function.
    """
    client: mongomock.Mongoclient = mongomock.MongoClient()
    user = User(email="sample@mail.com")
    insert_user(client, user)

    deleted_user = delete_user(client, user)
    assert deleted_user is not None

    assert get_user_by_id(client, user.id) is None
    assert client["streamlit-magic-link"]["users"].find_one({"email": "sample@mail.com"}) is None


def test_create_or_retrieve_user()-> None:
    """
    Test the create_or_retrieve_user function.
    """
    client: mongomock.MongoClient = mongomock.MongoClient()

    # Test creating a new user
    user = create_or_retrieve_user(client, "new_user@mail.com")
    assert user.email == "new_user@mail.com"

    # Test retrieving an existing user
    existing_user = create_or_retrieve_user(client, "new_user@mail.com")
    assert existing_user.email == "new_user@mail.com"
    assert existing_user.id == user.id


def test_insert_magic_link()-> None:
    """
    Test the insert_magic_link function.
    """
    client: mongomock.MongoClient = mongomock.MongoClient()
    user_id = "12345"
    magic_link = insert_magic_link(client, user_id)

    assert magic_link.user_id == user_id

    assert get_magic_link_by_token(client, magic_link.token) is not None
    assert client["streamlit-magic-link"]["magic-links"].find_one({"token": magic_link.token}) is not None


def test_get_magic_link_by_token()-> None:
    """
    Test the get_magic_link_by_token function.
    """
    client: mongomock.MongoClient = mongomock.MongoClient()
    user_id = "12345"
    magic_link = insert_magic_link(client, user_id)

    retrieved_magic_link = get_magic_link_by_token(client, magic_link.token)
    assert retrieved_magic_link is not None
    assert retrieved_magic_link.token == magic_link.token


def test_update_magic_link():
    """
    Test the update_magic_link function.
    """
    client: mongomock.MongoClient = mongomock.MongoClient()
    user_id = "12345"
    magic_link = insert_magic_link(client, user_id)

    magic_link.is_used = True
    updated_magic_link = update_magic_link(client, magic_link)

    assert updated_magic_link is not None
    assert updated_magic_link.is_used
    assert client["streamlit-magic-link"]["magic-links"].find_one({"is_used": True}) is not None