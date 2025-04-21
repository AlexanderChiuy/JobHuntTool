from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.clients.async_client import client

security = HTTPBearer() 


async def verify_google_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Token required")
    response = await client.get(f'https://oauth2.googleapis.com/tokeninfo?access_token={token}')
    if not response:
        raise HTTPException(status_code=401, detail="Invalid token")
    return response.json()
