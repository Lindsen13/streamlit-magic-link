# Streamlit Magic Link

Streamlit Magic Link is a Python package that simplifies the process of creating secure, single-use magic links for authentication in Streamlit applications.

## Features

- ✨ **Magic Link Authentication**: Generate secure, time-limited links for user authentication.
- 🤝 **Easy Integration**: Seamlessly integrate with your Streamlit app.
- ⚙️ **Customizable**: Configure expiration times, email templates, and more.
- 🔒 **Secure**: Built with security best practices to ensure safe authentication.

## Installation

Install the package using pip:

```bash
pip install streamlit-magic-link
```

## Usage

Here’s a quick example of how to use Streamlit Magic Link:

```python
import streamlit as st
from streamlit_magic_link import MagicLink

# Initialize MagicLink
magic_link = MagicLink()

# Log a user in based on url parameters
magic_link.sign_in()

# Send a magic link to the user
magic_link.authenticate(email)
```

## Configuration

You can customize the behavior of the package by passing configuration options:

    todo

## TODO

Here are some planned improvements and features for the Streamlit Magic Link package:

- **Sending Emails**: Integrate email-sending functionality using services like Mailgun, SendGrid, or AWS SES to deliver magic links directly to users.
- **Add Documentation**: Expand the documentation with detailed examples, API references, and a troubleshooting guide.
- **Package Distribution**: Prepare the package for distribution on PyPI, including creating a `setup.py` or `pyproject.toml` file and adding metadata.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request on the [GitHub repository](https://github.com/your-repo/streamlit-magic-link).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please reach out to [your-email@example.com](mailto:your-email@example.com).
