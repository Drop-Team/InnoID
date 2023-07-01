import base64
import json
from dataclasses import dataclass
from urllib.parse import quote_plus

import requests

from config import Config


@dataclass
class SsoIdentityUserResult:
    context: dict
    email: str
    name: str
    surname: str
    display_name: str
    job: str


class SsoLoginError(Exception):
    pass


def get_uri(redirect_uri: str, context: dict) -> str:
    context_str = json.dumps(context)
    context_b64 = base64.b64encode(context_str.encode('utf-8')).decode('utf-8')
    uri = "https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize" \
          "?client_id={client_id}" \
          "&response_type=code" \
          "&redirect_uri={redirect_uri}" \
          "&domain_hint={domain_hint}" \
          "&response_mode=query&" \
          "scope=User.ReadBasic.All" \
          "&state={state}" \
        .format(client_id=Config.MS_AD_CLIENT_ID,
                redirect_uri=quote_plus(redirect_uri),
                domain_hint=quote_plus(Config.MS_AD_DOMAIN_HINT),
                state=quote_plus(context_b64))
    return uri


def get_user_info(code: str, state: str, redirect_uri: str) -> SsoIdentityUserResult:
    context_str = base64.b64decode(state).decode('utf-8')
    context = json.loads(context_str)

    res = requests.post(
        "https://login.microsoftonline.com/organizations/oauth2/v2.0/token",
        data={
            "client_id": Config.MS_AD_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
            "client_secret": Config.MS_AD_CLIENT_SECRET,
            "code": code
        }
    )
    res_data = res.json()
    access_token = res_data.get("access_token", None)
    if not access_token:
        raise SsoLoginError("Error during fetching access token")

    res = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    res_data = res.json()

    return SsoIdentityUserResult(
        context=context,
        email=res_data.get("mail", None),
        name=res_data.get("givenName", None),
        surname=res_data.get("surname", None),
        display_name=res_data.get("displayName", None),
        job=res_data.get("jobTitle", None)
    )
