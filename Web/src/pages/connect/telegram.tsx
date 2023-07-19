import { useSearchParams } from "next/navigation";
import { API } from "@/lib/api";
import { LoginContext, Tokens } from "@/lib/objects";
import { useEffect } from "react";
import { GetServerSidePropsContext } from "next";
import { useApiCall } from "@/lib/api-call";
import { redirect } from "next/navigation";
import { TELEGRAM_BOT_URL } from "@/lib/config";

export default function LoginHandleSSO(): JSX.Element {
  const { data, error, loading } = useApiCall((api: API) => api.createIdCode());

  useEffect(() => {
    if (data) {
      window.location.href = `${TELEGRAM_BOT_URL}?start=${data.code}`;
    }
  }, [data]);

  if (loading) {
    return <div>Loading...</div>;
  }
  if (error) {
    return <div>Error</div>;
  }

  return <div>Success! Redirecting... </div>;
}
