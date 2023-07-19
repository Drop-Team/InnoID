import { APIBase, RequestMethod } from "./_api";
import { User, Tokens, LoginContext } from "@/lib/objects";

interface getCurrentUserResponse {
  user: User;
}

export class APIAuth extends APIBase {
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
