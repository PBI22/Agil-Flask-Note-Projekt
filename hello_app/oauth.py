"""
This module defines the OAuth blueprint for handling GitHub authentication in a Flask application. 
It includes routes for logging in, authorizing, and logging out users. 
The module utilizes the Authlib library to create and manage OAuth clients 
and integrates with GitHub to authenticate users. It also handles session management and token revocation.

Functions:
- register(): Initiates the login process and redirects to GitHub for authorization.
- authorize(): Handles the callback from GitHub, processes the user's information, and manages session data.
- logout(): Logs out the user and revokes the GitHub access token.
- revoke_github_token(): Sends a request to GitHub to revoke an access token.

"""

import os
import secrets
import requests
from flask import Blueprint, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from .dbconnect import dbsession
from .models import Account
from . import app

oauth_bp = Blueprint("oauth", __name__)

oauth = OAuth()
# registrering af github oauth klienten
github = oauth.register(
    name="github",
    client_id=os.environ.get("GH_CLIENT_ID"),
    client_secret=os.environ.get("GH_SECRET_ID"),
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)


@oauth_bp.route("/login")
def register():
    """
    Register function for user login.

    This function is used to handle the "/login" route and initiate the login process using the GitHub OAuth provider.
    It creates a GitHub client using the OAuth instance and generates a redirect URI for the authorization endpoint.
    The function logs the redirect URI and returns a redirect response to the authorization endpoint.

    Returns:
        A redirect response to the GitHub authorization endpoint.

    """
    github_client = oauth.create_client("github")
    redirect_uri = url_for("oauth.authorize", _external=True)
    app.logger.info("Redirecting to: %s", redirect_uri)
    print(f"Redirecting to: {redirect_uri}")
    return github_client.authorize_redirect(redirect_uri)


@oauth_bp.route("/authorize")
def authorize():
    """
    Authorizes the user using the GitHub OAuth provider.

    This function is responsible for authorizing the user by creating a client for the GitHub OAuth provider,
    obtaining an access token, and retrieving the user's profile information. If the user does not exist in the database,
    a new Account object is created and added to the database. The user's information is then stored in the session
    for future use.

    Returns:
        redirect: A redirect response to the home page ("/").

    """
    github_client = oauth.create_client("github")
    token = github_client.authorize_access_token()
    resp = github_client.get("user", token=token)
    profile = resp.json()

    user = dbsession.query(Account).filter_by(username=profile["login"]).first()

    if user is None:
        user = Account(
            username=profile["login"],
            password=secrets.token_urlsafe(32),
            email=profile["email"] or "No Mail",
            roleID=1,
        )
        dbsession.add(user)
        dbsession.commit()
    session["userID"] = user.accountID
    session["user"] = user.username
    session["userEmail"] = user.email
    session["roleID"] = user.roleID
    session["oauth"] = "github"
    session["oauth_id"] = profile["id"]
    session["oauth_token_type"] = token["token_type"]
    session["oauth_token"] = token["access_token"]

    return redirect("/")


@oauth_bp.route("/logout")
def logout():
    """
    Logout the user and revoke the GitHub access token.

    This function revokes the GitHub access token associated with the user's session and clears the session data.
    It also redirects the user to the homepage.

    Parameters:
    - None

    Returns:
    - A redirect response to the homepage ("/").

    Example Usage:
        logout()

    Note:
    - This function assumes that the client_id and client_secret are set up as
    global variables or retrieved from a secure location.

    """
    revoke_github_token(
        session["oauth_token"],
        os.environ.get("GH_CLIENT_ID"),
        os.environ.get("GH_SECRET_ID"),
    )
    session.clear()
    return redirect("/")


def revoke_github_token(access_token, client_id, client_secret):
    """
    Revoke a GitHub access token.

    This function revokes a GitHub access token by sending a DELETE request to the GitHub API.
    The access token, client ID, and client secret are required as parameters.

    Parameters:
        access_token (str): The access token to be revoked.
        client_id (str): The client ID of the GitHub application.
        client_secret (str): The client secret of the GitHub application.

    Returns:
        None

    Raises:
        requests.exceptions.RequestException: If an error occurs while making the API request.

    Example Usage:
        revoke_github_token("access_token", "client_id", "client_secret")

    Note:
        - This function assumes that the access token, client ID, and client secret are valid and provided by the caller.
        - The function uses the requests library to make the API request.
        - The function expects a successful response with a status code of 204 if the token is revoked successfully.

    """
    url = f"https://api.github.com/applications/{client_id}/token"
    response = requests.delete(
        url,
        params={"access_token": access_token},
        auth=(client_id, client_secret),
        timeout=10,
    )
    if response.status_code == 204:
        print("Token successfully revoked.")
    else:
        print("Failed to revoke token.")
