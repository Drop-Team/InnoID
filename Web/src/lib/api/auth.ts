import { APIBase, RequestMethod } from "./_api";
import { User, Tokens, LoginContext } from "@/lib/objects";

const WEB_ROOT_URL = "http://localhost:3000";
const SSO_REDIRECT_URI = WEB_ROOT_URL + "/login-handle/sso";

interface AuthWithSSOResponse {
  tokens: Tokens;
  loginContext: LoginContext;
}

interface getSSOLoginURLResponse {
  loginURL: string;
}

export class APIAuth extends APIBase {
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
  
    async getCurrentUser(): Promise<getCurrentUserResponse> {
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
  }
  