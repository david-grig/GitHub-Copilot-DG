import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Original activities data for reset
ORIGINAL_ACTIVITIES = {
    "Tennis Club": {
        "description": "Learn tennis skills and participate in matches",
        "schedule": "Wednesdays and Saturdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["james@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team with regular games",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater production and acting workshops",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["ethan@mergington.edu", "ava@mergington.edu"]
    },
    "Debate Team": {
        "description": "Competitive debate and public speaking",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 14,
        "participants": ["noah@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and scientific exploration",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["grace@mergington.edu", "lucas@mergington.edu"]
    },
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

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities dictionary before each test"""
    activities.clear()
    activities.update(ORIGINAL_ACTIVITIES)

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data
    assert "Basketball Team" in data
    # Check structure of one activity
    tennis = data["Tennis Club"]
    assert "description" in tennis
    assert "schedule" in tennis
    assert "max_participants" in tennis
    assert "participants" in tennis
    assert tennis["max_participants"] == 16
    assert "james@mergington.edu" in tennis["participants"]

def test_signup_success():
    response = client.post("/activities/Tennis Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    data = response.json()
    assert "Signed up newstudent@mergington.edu for Tennis Club" == data["message"]
    # Verify added
    response = client.get("/activities")
    tennis = response.json()["Tennis Club"]
    assert "newstudent@mergington.edu" in tennis["participants"]

def test_signup_activity_not_found():
    response = client.post("/activities/NonExistent Activity/signup", params={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Tennis Club/signup", params={"email": "duplicate@mergington.edu"})
    # Second signup
    response = client.post("/activities/Tennis Club/signup", params={"email": "duplicate@mergington.edu"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"

def test_unregister_success():
    # First signup
    client.post("/activities/Tennis Club/signup", params={"email": "removeme@mergington.edu"})
    # Then unregister
    response = client.delete("/activities/Tennis Club/unregister", params={"email": "removeme@mergington.edu"})
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered removeme@mergington.edu from Tennis Club" == data["message"]
    # Verify removed
    response = client.get("/activities")
    tennis = response.json()["Tennis Club"]
    assert "removeme@mergington.edu" not in tennis["participants"]

def test_unregister_activity_not_found():
    response = client.delete("/activities/NonExistent Activity/unregister", params={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_unregister_not_signed_up():
    response = client.delete("/activities/Tennis Club/unregister", params={"email": "notsignedup@mergington.edu"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not signed up for this activity"