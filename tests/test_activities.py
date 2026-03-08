"""
Tests for the /activities endpoint (GET /activities)
"""
import pytest


class TestActivitiesEndpoint:
    """Test suite for GET /activities endpoint"""

    def test_get_all_activities_returns_dict(self, client):
        """
        Test that GET /activities returns all activities

        Arrange: Test client is ready
        Act: Make GET request to /activities
        Assert: Verify response status 200 and returns activity dict
        """
        # Arrange
        # (client fixture provided by conftest.py)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_all_activities_includes_hardcoded_activities(self, client):
        """
        Test that all 9 hardcoded activities are returned

        Arrange: Test client is ready, know the expected activity names
        Act: Make GET request to /activities
        Assert: Verify all expected activities are present in response
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Ensemble",
            "Debate Team",
            "Robotics Club"
        ]

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        assert len(activities_data) == 9
        for activity_name in expected_activities:
            assert activity_name in activities_data

    def test_activity_has_required_fields(self, client):
        """
        Test that each activity has required fields

        Arrange: Test client is ready, define required fields
        Act: Make GET request to /activities
        Assert: Verify each activity contains description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        for activity_name, activity_info in activities_data.items():
            for field in required_fields:
                assert field in activity_info, \
                    f"Activity '{activity_name}' missing required field '{field}'"

    def test_activities_have_participants_list(self, client):
        """
        Test that each activity has a participants list

        Arrange: Test client is ready
        Act: Make GET request to /activities
        Assert: Verify participants field is a list for each activity
        """
        # Arrange
        # (client fixture provided by conftest.py)

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_info["participants"], list), \
                f"Activity '{activity_name}' participants should be a list"
