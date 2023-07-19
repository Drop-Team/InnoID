import { User, Tokens, LoginContext } from "@/lib/objects";
import { LocalStorage } from "@/lib/storage";
import {
  APIError,
  CallAPIError as CallAPIError,
  InternalAPIError,
} from "@/lib/errors";
import { WEB_ROOT_URL, API_URL } from "@/lib/config";

const SSO_REDIRECT_URI = WEB_ROOT_URL + "/login-handle/sso";

interface AuthWithSSOResponse {
  tokens: Tokens;
  loginContext: LoginContext;
}

interface getSSOLoginURLResponse {
  loginURL: string;
}

interface getUserInfoResponse {
  user: User;
}

interface getUserTelegramConnectionResponse {
  telegram_id: string;
  created: Date;
}

interface createIdCodeResponse {
  code: number;
}

enum RequestMethod {
  GET = "GET",
  POST = "POST",
  PUT = "PUT",
  PATCH = "PATCH",
  DELETE = "DELETE",
}

export class API {
  private storage: LocalStorage;

  constructor(storage: LocalStorage) {
    this.storage = storage;
  }

  private async makeAPIRequest<ResponseSchema>(
    resourceLocation: string,
    method: RequestMethod,
    body: object | undefined = undefined
  ): Promise<ResponseSchema> {
    let response = null;
    const access_token = this.storage.getAccessToken();
    try {
      response = await fetch(`${API_URL}${resourceLocation}`, {
        method: method,
        headers: {
          "Content-Type": "application/json",
          ...(access_token && { Authorization: `Bearer ${access_token}` }),
        },
        body: body ? JSON.stringify(body) : body,
      });
    } catch (e) {
      throw new CallAPIError();
    }
    if (response.status == 500) {
      throw new InternalAPIError();
    }
    const data = response.json();
    if () {
    }
    return data;
  }

  async getSSOLoginURL(): Promise<getSSOLoginURLResponse> {
    interface APIResponse {
      uri: string;
    }

    const data = await this.makeAPIRequest<APIResponse>(
      "/auth/sso/uri",
      RequestMethod.POST,
      {
        redirect_uri: SSO_REDIRECT_URI,
        context: {},
      }
    );
    return {
      loginURL: data.uri,
    };
  }

  async authWithSSO(
    authorization_code: string,
    state: string
  ): Promise<AuthWithSSOResponse> {
    interface APIResponse {
      tokens: Tokens;
      context: LoginContext;
    }

    const data = await this.makeAPIRequest<APIResponse>(
      "/auth/sso/login",
      RequestMethod.POST,
      {
        authorization_code: authorization_code,
        redirect_uri: SSO_REDIRECT_URI,
        state: state,
      }
    );
    this.storage.setAccessToken(data.tokens.access_token);
    this.storage.setRefreshToken(data.tokens.refresh_token);
    return { tokens: data.tokens, loginContext: data.context };
  }

  async getUserInfo(): Promise<getUserInfoResponse> {
    interface APIResponse {
      user_id: string;
      email: string;
    }

    const data = await this.makeAPIRequest<APIResponse>(
      "/profile",
      RequestMethod.GET
    );
    return {
      user: {
        user_id: data.user_id,
        email: data.email,
      },
    };
  }

  async getUserTelegramConnection(): Promise<getUserTelegramConnectionResponse> {
    interface APIResponse {
      telegram_id: string;
      created: Date;
    }

    const data = await this.makeAPIRequest<APIResponse>(
      "/profile/connections/telegram",
      RequestMethod.GET
    );
    return {
      telegram_id: data.telegram_id,
      created: new Date(data.created),
    };
  }

  async createIdCode(): Promise<createIdCodeResponse> {
    interface APIResponse {
      code: number;
    }

    const data = await this.makeAPIRequest<APIResponse>(
      "/profile/id_code",
      RequestMethod.POST
    );
    console.log(data);
    return {
      code: data.code,
    };
  }
}
