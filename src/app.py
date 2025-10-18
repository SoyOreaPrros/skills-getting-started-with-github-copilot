"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
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


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Prevent duplicate signups
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Add student to the activity
    activity["participants"].append(email)

    # Ensure additional activities exist (2 sports, 2 artistic, 2 intellectual)
    additional_activities = {
        "Soccer Team": {
            "description": "Competitive soccer matches and training",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Basketball Club": {
            "description": "Shoot hoops and scrimmages for all skill levels",
            "schedule": "Wednesdays and Fridays, 4:30 PM - 6:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Art Club": {
            "description": "Painting, drawing, and mixed media projects",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Drama Club": {
            "description": "Acting, stagecraft, and school productions",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": []
        },
        "Science Olympiad": {
            "description": "Hands-on science challenges and competitions",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": []
        },
        "Debate Team": {
            "description": "Practice debates and public speaking competitions",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        }
    }

    for name, info in additional_activities.items():
        activities.setdefault(name, info)

    # Add 2 more sports, 2 more artistic, and 2 more intellectual activities
    extra_activities = {
        "Volleyball Team": {
            "description": "Indoor and beach volleyball practice and matches",
            "schedule": "Mondays and Thursdays, 5:00 PM - 7:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Swim Team": {
            "description": "Competitive swim training and meets",
            "schedule": "Tuesdays and Fridays, 5:30 PM - 7:00 PM",
            "max_participants": 22,
            "participants": []
        },
        "Music Ensemble": {
            "description": "Instrumental and vocal ensemble rehearsals and performances",
            "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": []
        },
        "Photography Club": {
            "description": "Digital and film photography projects and exhibitions",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": []
        },
        "Math Club": {
            "description": "Problem solving, competitions, and math enrichment",
            "schedule": "Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": []
        },
        "Robotics Club": {
            "description": "Design and build robots for challenges and competitions",
            "schedule": "Tuesdays and Thursdays, 5:00 PM - 7:00 PM",
            "max_participants": 16,
            "participants": []
        }
    }

    for name, info in extra_activities.items():
        activities.setdefault(name, info)

    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if student is registered
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student not registered for this activity")

    # Remove student from activity
    activity["participants"].remove(email)

    return {"message": f"Unregistered {email} from {activity_name}"}
