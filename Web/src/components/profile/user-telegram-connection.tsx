import { API } from "@/lib/api";
import { useApiCall } from "@/lib/api-call";

export default function UserTelegramConnection(): JSX.Element {
  const { data, error, loading } = useApiCall((api: API) => api.getUserTelegramConnection());
    if (loading) {
        return <div>Loading...</div>;
    }
    if (error) {
        return <div>Error</div>;
    }
    if (data) {
        return (
            <div>
                {data.telegram_id}, {data.created.toISOString()}
            </div>
        );
    }
    return <></>;
}
