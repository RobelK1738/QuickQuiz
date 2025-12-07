from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
import os, json, firebase_admin
from firebase_admin import auth as firebase_auth, credentials

from app.core.database import SessionLocal
from app.models.models import User


# ---------------------------------------------------------------------------
#  Firebase Admin Initialization (LOCAL + PRODUCTION)
# ---------------------------------------------------------------------------

if not firebase_admin._apps:
    service_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS")

    try:
        if service_key_path and os.path.exists(service_key_path):
            # load from local file path
            cred = credentials.Certificate(service_key_path)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized using GOOGLE_APPLICATION_CREDENTIALS file")

        elif firebase_creds_json:
            # load from env string
            cred_dict = json.loads(firebase_creds_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized using FIREBASE_CREDENTIALS json")

        else:
            raise Exception(
                "No Firebase service credential found. "
                "Set GOOGLE_APPLICATION_CREDENTIALS to a JSON file path, "
                "or FIREBASE_CREDENTIALS to the JSON string."
            )

    except Exception as e:
        print("🔥 Firebase initialization error:", e)
        # DO NOT fallback to ApplicationDefault for local dev
        raise e


# ---------------------------------------------------------------------------
# Security setup
# ---------------------------------------------------------------------------

security = HTTPBearer(auto_error=False)


# ---------------------------------------------------------------------------
# DB Dependency
# ---------------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _get_or_create_user(db: Session, uid: str, email: str = None, name: str = "", picture: str = None) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            firebase_uid=uid,
            email=email or f"{uid}@unknown.local",
            display_name=name,
            picture=picture,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


# ---------------------------------------------------------------------------
# Required Auth
# ---------------------------------------------------------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
        )

    token = credentials.credentials
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name", "")
        picture = decoded_token.get("picture")

        if not uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Firebase token",
            )

        return _get_or_create_user(db, uid, email, name, picture)

    except Exception as e:
        print("Auth error:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# ---------------------------------------------------------------------------
# Optional Auth
# ---------------------------------------------------------------------------

def get_optional_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    if creds is None or not creds.credentials:
        return None

    try:
        decoded = firebase_auth.verify_id_token(creds.credentials)
        uid = decoded.get("uid")
        email = decoded.get("email")
        name = decoded.get("name", "")
        picture = decoded.get("picture")

        if not uid:
            return None

        return _get_or_create_user(db, uid, email, name, picture)

    except Exception:
        return None
