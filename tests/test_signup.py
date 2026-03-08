"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup)
"""
import pytest


class TestSignupEndpoint:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_student_success(self, client):
        """
        Test successful signup for a new student

        Arrange: Prepare activity name and new student email
        Act: Make POST request to signup endpoint with new email
        Assert: Verify 200 status, success message, and email added to participants
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert new_email in response.json()["message"]

        # Verify student was actually added by checking activity
        verify_response = client.get("/activities")
        activities = verify_response.json()
        assert new_email in activities[activity_name]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Test signup to non-existent activity returns 404

        Arrange: Prepare non-existent activity name and valid email
        Act: Make POST request to signup with invalid activity
        Assert: Verify 404 status and "Activity not found" message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_already_registered_student_returns_400(self, client):
        """
        Test signup fails when student already registered for activity

        Arrange: Get an activity with existing participants
        Act: Attempt to signup with an already-registered email
        Assert: Verify 400 status and "already signed up" message
        """
        # Arrange
        activity_name = "Chess Club"
        # Michael is already in Chess Club from app.py initialization
        existing_email = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_missing_email_parameter(self, client):
        """
        Test signup without email parameter fails

        Arrange: Prepare activity name without email parameter
        Act: Make POST request missing email query parameter
        Assert: Verify request fails with 422 validation error
        """
        # Arrange
        activity_name = "Programming Class"

        # Act
        response = client.post(f"/activities/{activity_name}/signup")

        # Assert
        assert response.status_code == 422

    def test_signup_multiple_activities_for_same_student(self, client):
        """
        Test that a student can signup for multiple different activities

        Arrange: Prepare a new student email and multiple activities
        Act: Signup same student to different activities
        Assert: Verify student appears in participants of both activities
        """
        # Arrange
        student_email = "multiactivity@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"

        # Act - Signup for first activity
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": student_email}
        )
        assert response1.status_code == 200

        # Act - Signup for second activity
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": student_email}
        )
        assert response2.status_code == 200

        # Assert - Verify in both activities
        verify_response = client.get("/activities")
        activities = verify_response.json()
        assert student_email in activities[activity1]["participants"]
        assert student_email in activities[activity2]["participants"]
