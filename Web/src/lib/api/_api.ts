import { User, Tokens, LoginContext } from "@/lib/objects";
import { LocalStorage } from "@/lib/storage";
import {
  APIError,
  CallAPIError as CallAPIError,
  InternalAPIError,
} from "@/lib/errors";

const API_URL = "http://127.0.0.1:8000/v2";
const WEB_ROOT_URL = "http://localhost:3000";

export enum RequestMethod {
  GET = "GET",
  POST = "POST",
  PUT = "PUT",
  PATCH = "PATCH",
  DELETE = "DELETE",
}

export class APIBase {
  protected storage: LocalStorage;

  constructor(storage: LocalStorage) {
    this.storage = storage;
  }

  protected async makeAPIRequest<ResponseSchema>(
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
    return response.json();
  }
}
