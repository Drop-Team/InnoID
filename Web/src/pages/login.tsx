import { useEffect } from "react";
import { API } from "@/lib/api";
import { useApiCall } from "@/lib/api-call";

// interface LoginProps {
//   loginSSOURL: string;
// }

export default function Login(): JSX.Element {
  const { data, error, loading } = useApiCall((api: API) =>
    api.getSSOLoginURL()
  );

  useEffect(() => {
    if (data) {
      window.location.href = data.loginURL;
    }
  });

  if (loading) {
    return <div>Loading...</div>;
  }

  if (data) {
    return <div>Redirecting...</div>;
  }

  return <div>Error...</div>;
}

// export async function getServerSideProps() {
//   const api = new API();
//   const loginSSOURL = await api.getSSOLoginURL();

//   return {
//     props: {
//       loginSSOURL: loginSSOURL,
//     },
//   };
// }
