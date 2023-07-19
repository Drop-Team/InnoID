import { API } from "@/lib/api";
import { useApiCall } from "@/lib/api-call";
import { APIAuth } from "@/lib/api/auth";

export default function UserInfo(): JSX.Element {
  const { data, error, loading } = useApiCall((api: APIAuth) => api.getUserInfo());
    if (loading) {
        return <div>Loading...</div>;
    }
    if (error) {
        return <div>Error</div>;
    }
    if (data) {
        const user = data.user;
        return (
            <div>
                {user.email}, {user.user_id}
            </div>
        );
    }
    return <></>;
}
