# Streamlit Magic Link

Streamlit Magic Link is a Python package that simplifies the process of creating secure, single-use magic links for authentication in Streamlit applications.

## Features

- ✨ **Magic Link Authentication**: Generate secure, time-limited links for user authentication.
- 🤝 **Easy Integration**: Seamlessly integrate with your Streamlit app.
- 🔒 **Secure**: Built with security best practices to ensure safe authentication.

## Installation

Install the package using pip:

```bash
pip install streamlit-magic-link
```

## Usage

Here’s a quick example of how to use Streamlit Magic Link:

Install dependencies
```python
import streamlit as st
from streamlit_magic_link import MagicLink
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
```

Create a MongoDB connection.
```python
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
```

Initialize MagicLink
```python
magic_link = StreamlitMagicLink(
    mongo_client=mongo_client,
    base_url="http://localhost:8501/",
)
```
Log a user in based on url parameters
```python
magic_link.sign_in()
```
Send a magic link to the user:
```python
magic_link.authenticate(email)
```

Log a user out
```python
magic_link.sign_out()
```

Update a user
```python
magic_link.update_user(
    email=email,
    name=name,
    is_payed_user=is_payed_user, # boolean
    additional_data=additional_data, # Any additional string data
)
```
Delete a user from the database
```python
magic_link.delete_user()
```
Get a dict with the User's info:
```python
magic_link.user
```

An example application can be found in `example/main.py`

## Configuration

The following environment variables are required to configure `Streamlit Magic Link`:

- `MONGODB_PASSWORD`: Your MongoDB password (e.g., `mysecurepassword`).
- `MONGODB_USERNAME`: Your MongoDB username (e.g., `admin`).
- `MONGODB_HOST`: Your MongoDB host (e.g., `cluster0.mongodb.net`).
- `DATABASE_NAME`: The name of the database (default: `streamlit-magic-link`).
- `COLLECTION_NAME_USERS`: The name of the users collection (default: `users`).
- `COLLECTION_NAME_MAGIC_LINKS`: The name of the magic links collection (default: `magic-links`).
- `MAILJET_API_KEY`: Your Mailjet API key.
- `MAILJET_API_SECRET`: Your Mailjet API secret.
- `FROM_EMAIL`: The email address used to send magic links.

## TODO

Here are some planned improvements and features for the Streamlit Magic Link package:

- **Package Distribution**: Prepare the package for distribution on PyPI, including creating a `setup.py` or `pyproject.toml` file and adding metadata.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request on the [GitHub repository](https://github.com/your-repo/streamlit-magic-link).

Before submitting a pull request, ensure that your code meets the following quality and testing standards:

```bash
pip install uv
uv sync --dev
uv run mypy .
uv run ruff check
uv run pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please reach out to [your-email@example.com](mailto:your-email@example.com).
