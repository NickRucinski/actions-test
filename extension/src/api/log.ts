import { LogData, LogEvent } from "../types/event";

/** Endpoint for logging information */
const LOG_ENDPOINT: string = "https://ai.nickrucinski.com/logs";

/**
 * Logs the user's decision on an AI-generated suggestion.
 *
 * @param {LogData} logData - The data being logged.
 */
export function trackEvent(logData: LogData): void {
    const body = JSON.stringify(logData);

    console.log("Logging event...", logData.event);

    fetch(LOG_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body,
    }).catch(err => console.error("Failed to log data:", err));
}
