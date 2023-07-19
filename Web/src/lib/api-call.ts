import { useEffect, useState } from "react";
import { API } from "./api";
import { LocalStorage } from "./storage";
import { APIError, UnknownAPIError } from "./errors";
import { APIBase } from "./api/_api";

export function useApiCall<ResponseSchema>(
  callback: (api: APIBase) => Promise<ResponseSchema>
) {
  const storage = new LocalStorage();
  const api = new API(storage);

  const [data, setData] = useState<ResponseSchema | null>(null);
  const [error, setError] = useState<APIError | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    callback(api)
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((error: unknown) => {
        if (!(error instanceof APIError)) {
          error = new UnknownAPIError();
        }
        setError(error);
        setLoading(false);
      });
  }, []);

  return { data, error, loading };
}
