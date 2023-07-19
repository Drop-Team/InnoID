export class APIError extends Error {
    message = "API Error";
}

export class UnknownAPIError extends APIError {
    message = "Unknown API Error";
}

export class CallAPIError extends APIError {
    message = "Failed to call API";
}

export class InternalAPIError extends APIError {
    message = "Internal API Error";
}

export class NoConnectionAPIError extends APIError {
    message = "No Connection";
}