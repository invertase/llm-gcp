from firebase_admin import auth

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


def verify_user(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
):
    """Verify Firebase user token and return decoded token."""
    try:
        decoded_token = auth.verify_id_token(cred.credentials, check_revoked=True)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    return decoded_token
