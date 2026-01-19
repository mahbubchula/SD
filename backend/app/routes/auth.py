"""
Authentication Routes
User registration, login, and token management with SQLite persistence
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.database import User as DBUser, Session as DBSession, ActivityLog

router = APIRouter()
security = HTTPBearer()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# In-memory active sessions cache (for fast lookups)
active_sessions_cache = {}


# Pydantic Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


class User(BaseModel):
    email: str
    full_name: str
    created_at: datetime


# Helper Functions
def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> dict:
    """Verify JWT token and update session activity"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        # Update last activity in database
        session = db.query(DBSession).filter(DBSession.email == email, DBSession.token == token).first()
        if session:
            session.last_activity = datetime.utcnow()
            db.commit()
            
        # Update cache
        active_sessions_cache[email] = datetime.utcnow()

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


# Routes
@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register new user"""

    # Check if user already exists
    existing_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    hashed_password = hash_password(user.password)
    
    new_user = DBUser(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    # Create session
    session = DBSession(
        email=user.email,
        token=access_token,
        login_time=datetime.utcnow(),
        last_activity=datetime.utcnow()
    )
    db.add(session)
    
    # Log activity
    activity = ActivityLog(
        email=user.email,
        full_name=user.full_name,
        action="register",
        timestamp=datetime.utcnow()
    )
    db.add(activity)
    db.commit()
    
    print(f"✅ NEW USER REGISTERED: {user.full_name} ({user.email})")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": new_user.email,
            "full_name": new_user.full_name,
            "created_at": new_user.created_at.isoformat()
        }
    }


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """Login user"""

    # Get user from database
    user = db.query(DBUser).filter(DBUser.email == user_login.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Verify password
    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token = create_access_token(data={"sub": user_login.email})

    # Create session
    login_time = datetime.utcnow()
    session = DBSession(
        email=user_login.email,
        token=access_token,
        login_time=login_time,
        last_activity=login_time
    )
    db.add(session)
    
    # Log activity
    activity = ActivityLog(
        email=user_login.email,
        full_name=user.full_name,
        action="login",
        timestamp=login_time
    )
    db.add(activity)
    db.commit()
    
    # Update cache
    active_sessions_cache[user_login.email] = login_time
    
    print(f"✅ USER LOGIN: {user.full_name} ({user_login.email}) at {login_time.strftime('%Y-%m-%d %H:%M:%S')}")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "full_name": user.full_name,
            "created_at": user.created_at.isoformat()
        }
    }


@router.get("/me", response_model=User)
async def get_current_user(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Get current user information"""

    email = payload.get("sub")
    user = db.query(DBUser).filter(DBUser.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "email": user.email,
        "full_name": user.full_name,
        "created_at": user.created_at
    }


@router.post("/logout")
async def logout(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Logout user (remove session)"""
    email = payload.get("sub")
    
    # Get user info
    user = db.query(DBUser).filter(DBUser.email == email).first()
    
    # Delete session
    db.query(DBSession).filter(DBSession.email == email).delete()
    
    # Log activity
    if user:
        activity = ActivityLog(
            email=email,
            full_name=user.full_name,
            action="logout",
            timestamp=datetime.utcnow()
        )
        db.add(activity)
        db.commit()
        print(f"👋 USER LOGOUT: {user.full_name} ({email})")
    
    # Remove from cache
    if email in active_sessions_cache:
        del active_sessions_cache[email]
    
    return {"message": "Successfully logged out"}


@router.get("/admin/active-users")
async def get_active_users(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Get list of currently active users (last activity within 30 minutes)"""
    current_time = datetime.utcnow()
    active_users = []
    
    # Get all sessions
    sessions = db.query(DBSession).all()
    
    for session in sessions:
        # Consider active if last activity within 30 minutes
        time_diff = (current_time - session.last_activity).total_seconds() / 60
        
        if time_diff <= 30:
            user = db.query(DBUser).filter(DBUser.email == session.email).first()
            if user:
                active_users.append({
                    "email": session.email,
                    "full_name": user.full_name,
                    "login_time": session.login_time.isoformat(),
                    "last_activity": session.last_activity.isoformat(),
                    "minutes_since_activity": round(time_diff, 1),
                    "status": "active" if time_diff <= 5 else "idle"
                })
    
    return {
        "active_users": active_users,
        "total_active": len(active_users),
        "timestamp": current_time.isoformat()
    }


@router.get("/admin/activity-log")
async def get_activity_log(payload: dict = Depends(verify_token), db: Session = Depends(get_db), limit: int = 50):
    """Get recent user activity log (login/logout/register events)"""
    # Get recent activities
    activities = db.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).limit(limit).all()
    
    # Format timestamps
    formatted_activities = []
    for activity in activities:
        formatted_activities.append({
            "email": activity.email,
            "full_name": activity.full_name,
            "action": activity.action,
            "timestamp": activity.timestamp.isoformat(),
            "time_ago": _time_ago(activity.timestamp),
            "details": activity.details
        })
    
    total_count = db.query(ActivityLog).count()
    
    return {
        "activities": formatted_activities,
        "total_events": total_count,
        "showing": len(formatted_activities)
    }


@router.get("/admin/all-users")
async def get_all_users(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Get list of all registered users"""
    users = db.query(DBUser).all()
    all_users = []
    
    for user in users:
        # Check if currently active
        session = db.query(DBSession).filter(DBSession.email == user.email).first()
        is_active = False
        last_activity = None
        
        if session:
            time_diff = (datetime.utcnow() - session.last_activity).total_seconds() / 60
            is_active = time_diff <= 30
            last_activity = session.last_activity.isoformat()
        
        all_users.append({
            "email": user.email,
            "full_name": user.full_name,
            "created_at": user.created_at.isoformat(),
            "is_active": is_active,
            "last_activity": last_activity
        })
    
    return {
        "users": all_users,
        "total_users": len(all_users),
        "active_now": sum(1 for u in all_users if u["is_active"])
    }


def _time_ago(timestamp: datetime) -> str:
    """Convert timestamp to human-readable 'time ago' format"""
    diff = datetime.utcnow() - timestamp
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes ago"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours ago"
    else:
        return f"{int(seconds / 86400)} days ago"
