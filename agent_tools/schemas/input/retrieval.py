from pydantic import BaseModel


class SqlQueryInput(BaseModel):
    query: str


class PolicyQueryInput(BaseModel):
    query: str