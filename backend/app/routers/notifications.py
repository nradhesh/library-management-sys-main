from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_notifications():
    # Placeholder for overdue book notifications
    return {"notifications": "Feature under development"}