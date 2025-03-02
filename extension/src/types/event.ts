export enum LogEvent {
    USER_ACCEPT = "USER_ACCEPT",
    USER_REJECT = "USER_REJECT",
    MODEL_GENERATE = "MODEL_GENERATE",
    MODEL_ERROR = "MODEL_ERROR",
}

export interface LogData {
    event: LogEvent;
    time_lapse: number;
    metadata: Record<string, any>;
}