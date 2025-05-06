import os

import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src import StreamlitMagicLink


@st.cache_resource
def get_mongo_client() -> MongoClient:
    """
    Create a MongoDB client
    """
    mongodb_password = os.environ["MONGODB_PASSWORD"]
    mongodb_username = os.environ["MONGODB_USERNAME"]
    mongodb_host = os.environ["MONGODB_HOST"]

    uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}@{mongodb_host}/?retryWrites=true&w=majority"

    client: MongoClient = MongoClient(uri, server_api=ServerApi("1"))
    return client


mongo_client = get_mongo_client()

magic_link = StreamlitMagicLink(
    mongo_client=mongo_client,
    base_url="http://localhost:8501/",
)

magic_link.sign_in()

st.title("Example Magic Link Streamlit App!")

if not magic_link.user:
    with st.container(border=True):
        email = st.text_input("Email", "Enter your email")
        if st.button("Login or Sign up"):
            magic_link.authenticate(email)
else:
    with st.container(border=True):
        st.text(f"Hello, {magic_link.user['email']}!")
        if st.button("Sign out"):
            magic_link.sign_out()


    with st.container(border=True):
        email = st.text_input(
            "Email",
            magic_link.user.get("email") if magic_link.user.get("email") else "",
        )
        name = st.text_input(
            "Name",
            magic_link.user.get("name") if magic_link.user.get("name") else "",
        )

        is_payed_user = st.checkbox(
            "Is payed user",
            value=magic_link.user.get("is_payed_user")
            if magic_link.user.get("is_payed_user")
            else False,
        )

        additional_data = st.text_input(
            "Additional data",
            magic_link.user.get("additional_data")
            if magic_link.user.get("additional_data")
            else "",
        )

        if st.button("Update user"):
            magic_link.update_user(
                email=email,
                name=name,
                is_payed_user=is_payed_user,
                additional_data=additional_data,
            )

        if st.button("Delete user", type="primary"):
            magic_link.delete_user()
