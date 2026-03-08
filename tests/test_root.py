"""
Tests for the root endpoint (GET /)
"""
import pytest


class TestRootEndpoint:
    """Test suite for GET / endpoint"""

    def test_root_redirects_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html

        Arrange: Test client is ready
        Act: Make GET request to /
        Assert: Verify 307 redirect status and location header
        """
        # Arrange
        # (client fixture provided by conftest.py)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"

    def test_root_redirect_follows_to_index(self, client):
        """
        Test that following the redirect returns the index.html content

        Arrange: Test client is ready
        Act: Make GET request to / with follow_redirects=True
        Assert: Verify response contains HTML content
        """
        # Arrange
        # (client fixture provided by conftest.py)

        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
