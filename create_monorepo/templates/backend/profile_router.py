PROFILE_ROUTER = """from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.config import sb_client

router = APIRouter(prefix="/auth", tags=["auth"])


class Profile(BaseModel):
    user_id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UpdateProfile(BaseModel):
    user_id: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@router.post("/create-profile")
async def create_profile(
    profile: Profile,
) -> JSONResponse:
    try:
        response = sb_client.table("profiles").insert(profile.model_dump()).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error creating profile: {str(e)}")

    if response.data:
        return JSONResponse(content={"status": "success"})
    else:
        return JSONResponse(
            content={"status": "error", "message": "profile creation failed"}
        )


@router.get("/get-profile")
async def get_profile(
    user_id: str = Query(..., description="The user ID to get the profile for"),
) -> JSONResponse:
    try:
        response = (
            sb_client.table("profiles").select("*").eq("user_id", user_id).execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error getting profile: {str(e)}")

    if response.data and len(response.data) > 0:
        first_name = response.data[0].get("first_name")
        last_name = response.data[0].get("last_name")
    else:
        first_name, last_name = None, None

    return JSONResponse(
        content={
            "status": "success",
            "first_name": first_name,
            "last_name": last_name,
        }
    )


@router.post("/update-profile")
async def update_profile(
    profile: UpdateProfile,
) -> JSONResponse:
    if not (profile.email or profile.first_name or profile.last_name):
        raise HTTPException(status_code=400, detail="No fields to update")

    to_update = {
        "email": profile.email,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
    }
    to_update = {k: v for k, v in to_update.items() if v != "" and v is not None}

    if profile.email:
        try:
            response = sb_client.auth.admin.update_user_by_id(
                profile.user_id, {"email": profile.email}
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"error updating email: {str(e)}"
            )

    try:
        response = (
            sb_client.table("profiles")
            .update(to_update)
            .eq("user_id", profile.user_id)
            .execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error updating profile: {str(e)}")

    if response.data:
        return JSONResponse(content={"status": "success"})
    else:
        return JSONResponse(
            content={"status": "error", "message": "profile update failed"}
        )

"""
