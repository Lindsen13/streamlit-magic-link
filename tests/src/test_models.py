from src.models import User, MagicLink
import datetime


def test_user_model() -> None:
    """Test User model"""
    user_id = "12345"
    user_email = "sample@mail.com"
    name = "Sample User"
    is_verified = True
    is_payed_user = True
    additional_data = "Some additional data"

    user = User(
        id=user_id,
        email=user_email,
        name=name,
        is_verified=is_verified,
        is_payed_user=is_payed_user,
        additional_data=additional_data,
    )

    assert user.id == user_id
    assert user.email == user_email
    assert user.name == name
    assert user.is_verified == is_verified
    assert user.is_payed_user == is_payed_user
    assert user.additional_data == additional_data


def test_user_model_without_optional_fields() -> None:
    """Test User model without optional fields"""
    user_email = "sample@mail.com"
    user = User(email=user_email)
    assert user.id is not None
    assert user.email == user_email
    assert user.name is None
    assert not user.is_verified
    assert not user.is_payed_user
    assert user.additional_data is None


def test_magic_link_model() -> None:
    """Test Magic Link model"""
    magic_link_token = "sample_token"
    user_id = "12345"
    is_used = False
    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=15)

    magic_link = MagicLink(
        token=magic_link_token,
        user_id=user_id,
        is_used=is_used,
        expiration_time=expiration_time,
    )

    assert magic_link.token == magic_link_token
    assert magic_link.user_id == user_id
    assert magic_link.is_used == is_used
    assert magic_link.expiration_time == expiration_time
