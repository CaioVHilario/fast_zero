from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import (
    creat_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])
OAuth2PasswordRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm,
    session: Session,
):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = creat_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
async def get_refresh_token(user: CurrentUser):
    new_access_toke = creat_access_token(data={'sub': user.email})

    return {'access_token': new_access_toke, 'token_type': 'Bearer'}
