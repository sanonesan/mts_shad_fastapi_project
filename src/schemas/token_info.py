from pydantic import BaseModel

__all__ = ["TokenInfo"]


class TokenInfo(BaseModel):
    """
    Class with token info
    """

    access_token: str
    token_type: str
