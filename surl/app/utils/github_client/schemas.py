from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    scope: str
    token_type: str


class UserPlan(BaseModel):
    name: Optional[str]
    space: Optional[int]
    private_repos: Optional[int]
    collaborators: Optional[int]


class User(BaseModel):
    login: Optional[str]
    id: Optional[int]
    node_id: Optional[str]
    avatar_url: Optional[str]
    gravatar_id: Optional[str]
    url: Optional[str]
    html_url: Optional[str]
    followers_url: Optional[str]
    following_url: Optional[str]
    gists_url: Optional[str]
    starred_url: Optional[str]
    subscriptions_url: Optional[str]
    organizations_url: Optional[str]
    repos_url: Optional[str]
    events_url: Optional[str]
    received_events_url: Optional[str]
    type: Optional[str]
    site_admin: Optional[bool]
    name: Optional[str]
    company: Optional[str]
    blog: Optional[str]
    location: Optional[str]
    email: Optional[str]
    hireable: Optional[bool]
    bio: Optional[str]
    twitter_username: Optional[str]
    public_repos: Optional[int]
    public_gists: Optional[int]
    followers: Optional[int]
    following: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
    private_gists: Optional[int]
    total_private_repos: Optional[int]
    owned_private_repos: Optional[int]
    disk_usage: Optional[int]
    collaborators: Optional[int]
    two_factor_authentication: Optional[bool]
    plan: Optional[UserPlan]


class UserEmail(BaseModel):
    email: Optional[str]
    verified: Optional[bool]
    primary: Optional[bool]
    visibility: Optional[str]
