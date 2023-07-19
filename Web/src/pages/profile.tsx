import { useEffect } from "react";
import { API } from "@/lib/api";
import { useApiCall } from "@/lib/api-call";
import UserInfo from "@/components/profile/user-info";
import UserTelegramConnection from "@/components/profile/user-telegram-connection";

// interface LoginProps {
//   loginSSOURL: string;
// }

export default function Profile(): JSX.Element {
  // const { data, error, loading } = useApiCall((api: API) =>
  //   api.getUserInfo()
  // );
  // let userInfo = <div>Loading...</div>
  // if (error || !data) {
  //   userInfo = <div>Error...</div>;
  // }
  // if (data) {
  //   const user = data.user;
  //   userInfo = <div>{user.email}, {user.user_id}</div>;
  // }
  
  // const { data, error, loading } = useApiCall((api: API) =>
  //   api.getUserTelegramConnection()
  // );
  // let connectionInfo = <div>Loading...</div>
  // if (error || !data) {
  //   userInfo = <div>Error...</div>;
  // }
  // if (data) {
  //   const user = data.user;
  //   userInfo = <div>{user.email}, {user.user_id}</div>;
  // }

  return (
    <div>
      <h1>Profile</h1>
      <UserInfo></UserInfo>
      <h2>Connections</h2>
      <UserTelegramConnection></UserTelegramConnection>
    </div>
  );
}
