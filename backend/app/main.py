from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.routers import books, users, notifications
from app.database import Base, engine, get_db
from app import crud, schemas

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Library Management System",
    description="Backend for the Library Management System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System API"}

@app.on_event("startup")
def startup_event():
    db: Session = next(get_db())
    # Add initial books
    initial_books = [
        schemas.BookCreate(title="Book A", author="Author A", isbn="12345"),
        schemas.BookCreate(title="Book B", author="Author B", isbn="67890"),
    ]
    for book in initial_books:
        if not db.query(crud.models.Book).filter(crud.models.Book.isbn == book.isbn).first():
            crud.create_book(db, book)
    
    # Add initial users
    initial_users = [
        schemas.UserCreate(name="User A"),
        schemas.UserCreate(name="User B"),
    ]
    for user in initial_users:
        if not db.query(crud.models.User).filter(crud.models.User.name == user.name).first():
            crud.create_user(db, user)