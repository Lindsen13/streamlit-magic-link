from src.db import get_user_collection, get_magic_link_collection
from unittest import mock


def test_get_user_collection() -> None:
    """
    Test the get_user_collection function.
    """
    mock_database = mock.MagicMock()
    mock_client = mock.MagicMock()
    mock_user_collection = mock.MagicMock()

    mock_client.get_database.return_value = mock_database
    mock_database.get_collection.return_value = mock_user_collection
    result = get_user_collection(mock_client)
    assert result == mock_user_collection

    assert mock_client.get_database.called_once()
    assert mock_database.get_collection.called_once()

def test_get_magic_link_collection() -> None:
    """
    Test the get_magic_link_collection function.
    """
    mock_database = mock.MagicMock()
    mock_client = mock.MagicMock()
    mock_magic_link_collection = mock.MagicMock()

    mock_client.get_database.return_value = mock_database
    mock_database.get_collection.return_value = mock_magic_link_collection
    result = get_magic_link_collection(mock_client)
    assert result == mock_magic_link_collection

    assert mock_client.get_database.called_once()
    assert mock_database.get_collection.called_once()