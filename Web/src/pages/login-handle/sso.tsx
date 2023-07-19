import { useSearchParams } from "next/navigation";
import { API } from "@/lib/api";
import { LoginContext, Tokens } from "@/lib/objects";
import { useEffect } from "react";
import { GetServerSidePropsContext } from "next";
import { useApiCall } from "@/lib/api-call";
import { redirect } from 'next/navigation';

interface LoginHandleSSOProps {
  code: string;
  state: string;
}
export default function LoginHandleSSO({
  code,
  state,
}: LoginHandleSSOProps): JSX.Element {
  const { data, error, loading } = useApiCall((api: API) =>
    api.authWithSSO(code, state)
  );

  useEffect(() => {
    if (data) {
      window.location.href = "/profile";
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

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const { code, state } = context.query;
  return {
    props: {
      code: code,
      state: state,
    },
  };
}
