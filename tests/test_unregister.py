"""
Tests for the unregister endpoint (DELETE /activities/{activity_name}/participants)
"""
import pytest


class TestUnregisterEndpoint:
    """Test suite for DELETE /activities/{activity_name}/participants endpoint"""

    def test_unregister_registered_student_success(self, client):
        """
        Test successful unregistration of a registered student

        Arrange: Get activity with existing participant (Emma in Programming Class)
        Act: Make DELETE request to unregister existing student
        Assert: Verify 200 status, success message, and email removed from participants
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Emma is in Programming Class from app.py

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email in response.json()["message"]

        # Verify student was actually removed
        verify_response = client.get("/activities")
        activities = verify_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """
        Test unregister from non-existent activity returns 404

        Arrange: Prepare non-existent activity name and valid email
        Act: Make DELETE request with invalid activity
        Assert: Verify 404 status and "Activity not found" message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_unregistered_student_returns_400(self, client):
        """
        Test unregister fails when student is not registered

        Arrange: Prepare activity and email that's not in participants
        Act: Make DELETE request for non-participant
        Assert: Verify 400 status and "not signed up" message
        """
        # Arrange
        activity_name = "Robotics Club"
        email = "notstudent@mergington.edu"  # This email is not in Robotics Club

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_missing_email_parameter(self, client):
        """
        Test unregister without email parameter fails

        Arrange: Prepare activity name without email parameter
        Act: Make DELETE request missing email query parameter
        Assert: Verify request fails with 422 validation error
        """
        # Arrange
        activity_name = "Tennis Club"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants")

        # Assert
        assert response.status_code == 422

    def test_unregister_then_signup_again(self, client):
        """
        Test that a student can unregister and re-signup for same activity

        Arrange: Get activity with existing participant
        Act: Unregister student, then signup again
        Assert: Verify student successfully re-registered
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Michael is in Chess Club

        # Act - Unregister
        response_delete = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        assert response_delete.status_code == 200

        # Verify removed
        verify_removed = client.get("/activities")
        activities_after_delete = verify_removed.json()
        assert email not in activities_after_delete[activity_name]["participants"]

        # Act - Sign up again
        response_signup = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response_signup.status_code == 200

        # Assert - Verify re-registered
        verify_readded = client.get("/activities")
        activities_after_signup = verify_readded.json()
        assert email in activities_after_signup[activity_name]["participants"]
