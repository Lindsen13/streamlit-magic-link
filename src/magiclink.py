from datetime import datetime
from typing import Optional, cast

import streamlit as st
from pymongo.mongo_client import MongoClient
from streamlit_cookies_controller import CookieController

from src.models import MagicLink, User
from src.utils import (
    create_or_retrieve_user,
    get_magic_link_by_token,
    get_user_by_id,
    insert_magic_link,
    update_magic_link,
    update_user,
    delete_user,
)


class StreamlitMagicLink:
    """
    StreamlitMagicLink is a class that provides methods for generating and verifying magic links for user authentication.

    Attributes:
        mongo_client (MongoClient): The MongoDB client used for database operations.
        base_url (str): The base URL of the application, used for generating magic links.
        cookie_controller (CookieController): An optional controller for managing cookies. If not provided, a default instance is created.
    Methods:
        user:
            Returns the current user stored in the cookie.
        authenticate(email: str) -> None:
            Authenticates the user by generating a magic link and sending it to the user's email.
            Args:
                email (str): The email address of the user to authenticate.
        sign_in() -> None:
            Signs in a user by validating the magic link token from the query parameters.
        sign_out() -> None:
            Signs out the current user by removing their cookie and rerunning the Streamlit app.
    """

    def __init__(
        self,
        mongo_client: MongoClient,
        base_url: str,
        cookie_controller: Optional[CookieController] = None,
    ):
        """
        Initializes the MagicLinkAuth class
        """
        self.mongo_client = mongo_client
        self.base_url = base_url
        if cookie_controller:
            self.cookie_controller = cookie_controller
        else:
            self.cookie_controller = CookieController()

        self._sync_user()

    @property
    def user(self):
        """Returns the current user"""
        return self.cookie_controller.get("user")

    def authenticate(self, email: str) -> None:
        """Authenticates the user by generating a magic link and sending it to the user's email."""
        self._send_magic_link(email)
        st.toast(f"A magic link has been sent to {email}. Please check your inbox.", icon=":material/check:")

    def sign_in(self) -> None:
        """Signs in a user"""
        token = st.query_params.get("token")
        if token:
            print("Trying to sign in")
            user = self._handle_magic_link(token)
            if not user:
                st.query_params.clear()
                st.toast("Invalid or expired magic link.", icon=":material/error:")
            else:
                self._set_user(user)
                st.query_params.clear()
                st.toast("You are now signed in.", icon=":material/check:")
                

    def sign_out(self) -> None:
        """Signs out the current user"""
        self._remove_user()
        st.toast("You are now signed out.", icon=":material/check:")

    def update_user(self, **kwargs) -> None:
        """Updates the current user"""
        if not self.user:
            return None

        updated_user = update_user(self.mongo_client, User(**{**self.user, **kwargs}))
        if updated_user:
            self._set_user(updated_user)
        
        st.toast("User updated successfully!", icon=":material/check:")

    def delete_user(self) -> None:
        """Deletes the current user"""
        if not self.user:
            return
        delete_user(self.mongo_client, User(**self.user))
        self._remove_user()
        st.rerun()
        st.toast("User deleted successfully!", icon=":material/check:")

    def _sync_user(self) -> None:
        """Sets the current user in the cookie. We do this ongoing, to ensure
        any changes to the user are reflected in the cookie.
        This is useful for example when a backend process updates the user 
        in the database.
        
        We remove the user from the cookie if the user is not found in the database.
        This is useful for example when the user is deleted from the database or if
        something went wrong.
        """
        if not self.user:
            return None
        user = get_user_by_id(self.mongo_client, self.user['id'])
        if not user:
            self._remove_user()
            return None
        self._set_user(user)

    def _set_user(self, user: User) -> None:
        """Sets the current user in the cookie"""
        self.cookie_controller.set("user", user.model_dump())

    def _remove_user(self) -> None:
        """Removes the current user from the cookie"""
        self.cookie_controller.remove("user")

    def _handle_magic_link(self, magic_link_id: str) -> Optional[User]:
        """
        Validate a magic link by its ID, and return the user if valid.
        """
        magic_link = get_magic_link_by_token(self.mongo_client, magic_link_id)

        if not self._validate_magic_link(magic_link, magic_link_id):
            return None

        magic_link = cast(MagicLink, magic_link)

        user = get_user_by_id(self.mongo_client, magic_link.user_id)
        if not user:
            print(f"User with id {magic_link.user_id} not found.")
            return None

        magic_link.is_used = True
        update_magic_link(self.mongo_client, magic_link)

        user.is_verified = True
        update_user(self.mongo_client, user)
        return user

    @staticmethod
    @st.cache_resource(ttl=1)
    def _validate_magic_link(
        _magic_link: Optional[MagicLink], magic_link_id: str
    ) -> bool:
        """Validate a magic link

        We are caching this function to handle Streamlit's rerun behavior.
        If we would not cache this function, a magic link would be validated
        multiple times, which would lead to an invalid login for the user.

        NOTE: `_magic_link` is assigned an underscore to avoid caching over the pydantic
        model, which is not possible.
        """
        if not _magic_link:
            print(f"Magic link with id {magic_link_id} not found.")
            return False
        if _magic_link.is_used:
            print(f"Magic link with id {magic_link_id} is already used.")
            return False
        if _magic_link.expiration_time < datetime.now():
            print(f"Magic link with id {magic_link_id} is expired.")
            return False
        return True

    def _send_magic_link(self, email: str) -> None:
        """
        Send a magic link to the user.
        """
        user = create_or_retrieve_user(self.mongo_client, email)
        magic_link = insert_magic_link(self.mongo_client, user.id)
        # Here you would send the magic link to the user's email
        print(f"Magic link sent to {email}: {self.base_url}?token={magic_link.token}")
