import os
import time
from typing import List, Optional
from fastapi import Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
ALGORITHMS = os.getenv("ALGORITHMS", "RS256").split(",")

http_bearer = HTTPBearer()

class TokenData:
    def __init__(self, sub: str, roles: List[str]):
        self.sub = sub
        self.roles = roles

_jwks = None
_jwks_uri = None

def _get_jwks():
    global _jwks, _jwks_uri
    if _jwks is None:
        if not AUTH0_DOMAIN:
            raise RuntimeError("AUTH0_DOMAIN not configured")
        _jwks_uri = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        r = requests.get(_jwks_uri)
        r.raise_for_status()
        _jwks = r.json()
    return _jwks


def verify_jwt(token: str) -> dict:
    jwks = _get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks.get("keys", []):
        if key["kid"] == unverified_header.get("kid"):
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key.get("use"),
                "n": key.get("n"),
                "e": key.get("e"),
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/",
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token_expired")
        except jwt.JWTClaimsError:
            raise HTTPException(status_code=401, detail="invalid_claims")
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    raise HTTPException(status_code=401, detail="Unable to find appropriate key")


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(http_bearer)) -> TokenData:
    token = credentials.credentials
    payload = verify_jwt(token)
    sub = payload.get("sub")
    # roles may be in 'roles' claim or under a custom namespace; adapt as needed
    roles = payload.get("roles") or payload.get("https://example.com/roles") or []
    if isinstance(roles, str):
        roles = [roles]
    return TokenData(sub=sub, roles=roles)


def has_role(token: TokenData, allowed_roles: List[str]) -> bool:
    if not token:
        return False
    for r in token.roles:
        if r.upper() in [ar.upper() for ar in allowed_roles]:
            return True
    return False
