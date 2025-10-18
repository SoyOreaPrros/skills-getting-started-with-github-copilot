"""
Test suite for the Mergington High School Activities API
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app
import json


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    from src.app import activities
    
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Reset activities to original state
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Clean up after test (reset again)
    activities.clear()
    activities.update(original_activities)


class TestRootEndpoint:
    """Test the root endpoint"""
    
    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    """Test the activities endpoint"""
    
    def test_get_activities_success(self, client, reset_activities):
        """Test successful retrieval of activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 3  # Initial activities
        
        # Check that all expected activities are present
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        for activity in expected_activities:
            assert activity in data
            
        # Check structure of each activity
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
    
    def test_get_activities_returns_correct_data(self, client, reset_activities):
        """Test that activities endpoint returns correct initial data"""
        response = client.get("/activities")
        data = response.json()
        
        # Test Chess Club data
        chess_club = data["Chess Club"]
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupEndpoint:
    """Test the signup endpoint"""
    
    def test_signup_success(self, client, reset_activities):
        """Test successful signup for an activity"""
        email = "test@mergington.edu"
        activity = "Chess Club"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity}"
        
        # Verify the student was added to the activity
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity]["participants"]
    
    def test_signup_duplicate_student(self, client, reset_activities):
        """Test signup fails when student already registered"""
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 400
        assert "Student already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity(self, client, reset_activities):
        """Test signup fails for nonexistent activity"""
        email = "test@mergington.edu"
        activity = "Nonexistent Club"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_adds_additional_activities(self, client, reset_activities):
        """Test that signing up adds additional activities to the system"""
        email = "test@mergington.edu"
        activity = "Chess Club"
        
        # Initially should have 3 activities
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json())
        assert initial_count == 3
        
        # Sign up for an activity
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Should now have more activities
        final_response = client.get("/activities")
        final_count = len(final_response.json())
        assert final_count > initial_count
        
        # Check that some of the expected additional activities are present
        activities_data = final_response.json()
        additional_activities = ["Soccer Team", "Basketball Club", "Art Club", "Drama Club"]
        for additional_activity in additional_activities:
            assert additional_activity in activities_data
    
    def test_signup_with_url_encoded_activity_name(self, client, reset_activities):
        """Test signup works with URL-encoded activity names"""
        email = "test@mergington.edu"
        activity = "Programming Class"
        encoded_activity = "Programming%20Class"
        
        response = client.post(f"/activities/{encoded_activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify the student was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity]["participants"]


class TestUnregisterEndpoint:
    """Test the unregister endpoint"""
    
    def test_unregister_success(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        
        # Verify student is initially registered
        activities_response = client.get("/activities")
        initial_data = activities_response.json()
        assert email in initial_data[activity]["participants"]
        
        # Unregister the student
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == f"Unregistered {email} from {activity}"
        
        # Verify the student was removed
        activities_response = client.get("/activities")
        final_data = activities_response.json()
        assert email not in final_data[activity]["participants"]
    
    def test_unregister_student_not_registered(self, client, reset_activities):
        """Test unregister fails when student not registered"""
        email = "notregistered@mergington.edu"
        activity = "Chess Club"
        
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response.status_code == 400
        assert "Student not registered for this activity" in response.json()["detail"]
    
    def test_unregister_nonexistent_activity(self, client, reset_activities):
        """Test unregister fails for nonexistent activity"""
        email = "michael@mergington.edu"
        activity = "Nonexistent Club"
        
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_with_url_encoded_activity_name(self, client, reset_activities):
        """Test unregister works with URL-encoded activity names"""
        email = "emma@mergington.edu"  # Already in Programming Class
        activity = "Programming Class"
        encoded_activity = "Programming%20Class"
        
        response = client.delete(f"/activities/{encoded_activity}/unregister?email={email}")
        assert response.status_code == 200
        
        # Verify the student was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity]["participants"]


class TestIntegrationScenarios:
    """Test complete user scenarios"""
    
    def test_signup_and_unregister_flow(self, client, reset_activities):
        """Test complete flow: signup -> verify -> unregister -> verify"""
        email = "integration@mergington.edu"
        activity = "Gym Class"
        
        # Initial state - student not registered
        activities_response = client.get("/activities")
        initial_data = activities_response.json()
        assert email not in initial_data[activity]["participants"]
        
        # Sign up
        signup_response = client.post(f"/activities/{activity}/signup?email={email}")
        assert signup_response.status_code == 200
        
        # Verify signup
        activities_response = client.get("/activities")
        after_signup_data = activities_response.json()
        assert email in after_signup_data[activity]["participants"]
        
        # Unregister
        unregister_response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert unregister_response.status_code == 200
        
        # Verify unregistration
        activities_response = client.get("/activities")
        after_unregister_data = activities_response.json()
        assert email not in after_unregister_data[activity]["participants"]
    
    def test_multiple_students_same_activity(self, client, reset_activities):
        """Test multiple students can sign up for the same activity"""
        activity = "Chess Club"
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        
        # Sign up multiple students
        for email in emails:
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all students are registered
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        for email in emails:
            assert email in activities_data[activity]["participants"]
    
    def test_student_signup_multiple_activities(self, client, reset_activities):
        """Test one student can sign up for multiple activities"""
        email = "multisport@mergington.edu"
        activities_to_join = ["Chess Club", "Programming Class", "Gym Class"]
        
        # Sign up for multiple activities
        for activity in activities_to_join:
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify student is in all activities
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        for activity in activities_to_join:
            assert email in activities_data[activity]["participants"]


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_missing_email_parameter(self, client, reset_activities):
        """Test signup without email parameter"""
        activity = "Chess Club"
        
        response = client.post(f"/activities/{activity}/signup")
        assert response.status_code == 422  # Validation error
    
    def test_empty_email_parameter(self, client, reset_activities):
        """Test signup with empty email"""
        activity = "Chess Club"
        
        response = client.post(f"/activities/{activity}/signup?email=")
        assert response.status_code == 200  # Currently allows empty email
        
        # This might be a bug to fix in the future
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "" in activities_data[activity]["participants"]
    
    def test_special_characters_in_activity_name(self, client, reset_activities):
        """Test handling of special characters in activity names"""
        email = "test@mergington.edu"
        
        # Test with activity name that has special characters
        response = client.post("/activities/Test%20%26%20Special%20Activity/signup?email=test@mergington.edu")
        assert response.status_code == 404  # Activity doesn't exist
    
    def test_case_sensitivity_activity_names(self, client, reset_activities):
        """Test that activity names are case sensitive"""
        email = "test@mergington.edu"
        
        # Try with wrong case
        response = client.post("/activities/chess%20club/signup?email=test@mergington.edu")
        assert response.status_code == 404  # Case sensitive, should fail
        
        # Try with correct case
        response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
        assert response.status_code == 200  # Should succeed


if __name__ == "__main__":
    pytest.main([__file__])