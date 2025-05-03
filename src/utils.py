from typing import Optional

from pymongo.mongo_client import MongoClient

from src.db import (
    get_magic_link_collection,
    get_user_collection,
)
from src.models import MagicLink, User


def insert_user(client: MongoClient, user: User) -> User:
    """
    Insert a user into the MongoDB collection.
    """
    users = get_user_collection(client)
    if users.find_one({"$or": [{"id": user.id}, {"email": user.email}]}):
        print(f"User with id {user.id} or email {user.email} already exists.")
    else:
        users.insert_one(user.model_dump())
    return user


def get_user_by_id(client: MongoClient, user_id: str) -> Optional[User]:
    """
    Get a user from the MongoDB collection.
    """
    users = get_user_collection(client)
    user = users.find_one({"id": user_id})
    if not user:
        print(f"User with id {user_id} not found.")
        return None
    return User(**user)


def get_user_by_email(client: MongoClient, email: str) -> Optional[User]:
    """
    Get a user from the MongoDB collection by email.
    """
    users = get_user_collection(client)
    user = users.find_one({"email": email})
    if not user:
        print(f"User with email {email} not found.")
        return None
    return User(**user)


def update_user(client: MongoClient, user: User) -> Optional[User]:
    """
    Update a user in the MongoDB collection.
    """
    users = get_user_collection(client)
    result = users.update_one({"id": user.id}, {"$set": user.model_dump()})
    if result.matched_count == 0:
        print(f"User with id {user.id} not found.")
        return None
    return get_user_by_id(client, user.id)


def delete_user(client: MongoClient, user: User) -> Optional[User]:
    """
    Delete a user from the MongoDB collection.
    """
    users = get_user_collection(client)
    result = users.delete_one({"id": user.id})
    if result.deleted_count == 0:
        print(f"User with id {user.id} not found.")
        return None
    return user


def create_or_retrieve_user(client, email: str) -> User:
    """
    Create a new user or retrieve an existing one from the MongoDB collection.
    """
    user = get_user_by_email(client, email)
    if user:
        return user
    return insert_user(client, User(email=email))


def insert_magic_link(client: MongoClient, user_id: str) -> MagicLink:
    """
    Insert a magic link into the MongoDB collection.
    """
    magic_links = get_magic_link_collection(client)

    magic_link = MagicLink(user_id=user_id)
    magic_links.insert_one(magic_link.model_dump())
    return magic_link


def get_magic_link_by_token(client: MongoClient, token: str) -> Optional[MagicLink]:
    """
    Get a magic link from the MongoDB collection by token.
    """
    magic_links = get_magic_link_collection(client)
    magic_link = magic_links.find_one({"token": token})
    if not magic_link:
        print(f"Magic link with token {token} not found.")
        return None
    return MagicLink(**magic_link)


def update_magic_link(
    client: MongoClient, magic_link: MagicLink
) -> Optional[MagicLink]:
    """
    Update a magic link in the MongoDB collection.
    """
    magic_links = get_magic_link_collection(client)
    result = magic_links.update_one(
        {"token": magic_link.token}, {"$set": magic_link.model_dump()}
    )
    if result.matched_count == 0:
        print(f"Magic link with token {magic_link.token} not found.")
        return None
    return get_magic_link_by_token(client, magic_link.token)
