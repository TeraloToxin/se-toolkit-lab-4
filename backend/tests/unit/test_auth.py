"""Unit tests for authentication edge cases."""

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.auth import verify_api_key


class TestVerifyApiKey:
    """Tests for the verify_api_key function."""

    def test_valid_api_key_returns_token(self) -> None:
        """Test that a valid API key returns the token string."""
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials="test"
        )
        result = verify_api_key(credentials)
        assert result == "test"

    def test_invalid_api_key_raises_401(self) -> None:
        """Test that an invalid API key raises HTTPException with 401 status."""
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials="wrong_key"
        )
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(credentials)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid API key"

    def test_empty_api_key_raises_401(self) -> None:
        """Test that an empty API key raises HTTPException with 401 status."""
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials=""
        )
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(credentials)
        assert exc_info.value.status_code == 401

    def test_whitespace_only_api_key_raises_401(self) -> None:
        """Test that a whitespace-only API key raises HTTPException with 401 status."""
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials="   "
        )
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(credentials)
        assert exc_info.value.status_code == 401

    def test_api_key_with_leading_trailing_spaces_raises_401(self) -> None:
        """Test that API key with leading/trailing spaces is treated as invalid."""
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials=" test "
        )
        with pytest.raises(HTTPException) as exc_info:
            verify_api_key(credentials)
        assert exc_info.value.status_code == 401
