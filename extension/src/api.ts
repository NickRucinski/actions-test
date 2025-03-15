import * as vscode from "vscode";
import { Result } from "./types/result";
import { LogData, LogEvent } from "./types/event";
import { Suggestion, SuggestionResult } from "./types/suggetsion";

/** Endpoint for creating new AI suggestions */
const AI_ENDPOINT: string = "https://ai.nickrucinski.com/suggestion";

/** Endpoint for logging information */
const LOG_ENDPOINT: string = "https://ai.nickrucinski.com/logs";

const LOG_SUGGESTION_ENDPOINT: string = "http://127.0.0.1:8001/log-suggestion";

/**
 * Fetches AI-generated suggestions based on the given prompt.
 *
 * @param {string} prompt - The input prompt to send to the AI model.
 * @param {string} model - The LLM to be usded for generating suggestions.
 * @param {string} temperature - The temperature value to use for generating the response. Defaulted to 0.2.
 * @param {string} top_k - The Top K value to use for generating the response. Defaulted to 0.
 * @param {string} top_p - The Top P value to use for generating the response. Defaulted to 0.
 * @param {string} max_tokens - The max number of tokens allowed for response length.
 * @returns {Promise<string[]>} A promise that resolves to an array of suggested strings.
 */
export async function fetchSuggestions(
    prompt: string, model = "ollama", 
    temperature = 0.2, 
    top_k = 0, 
    top_p = 1, 
    max_tokens = 256, 
    endpoint=AI_ENDPOINT
): Promise<Result<SuggestionResult>> {
    const startTime = Date.now();

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt, model, temperature, top_k, top_p, max_tokens }),
        });

        const endTime = Date.now(); 
        const elapsedTime = endTime - startTime;
        let hasBug = false;

        if (!response.ok) {
            return { status: response.status, success: false, error: `Error: ${response.status} ${response.statusText}` };
        }

        const data = await response.json() as { suggestions?: string[]; error?: string };

        if (data.suggestions && data.suggestions) {
            const suggestion: Suggestion = {
                id: "",
                prompt,
                suggestionText: data.suggestions.join(", "),
                hasBug,
                model: model
            }

            console.log("AI Suggestions:", data.suggestions);

            const result = await saveSuggestionToDatabase(suggestion);
            let suggestionId = "";

            if (result.success && result.data) {
                suggestionId = result.data.id;
            }

            const logData: LogData = {
                event: LogEvent.MODEL_GENERATE,
                time_lapse: elapsedTime,
                metadata: { suggestion_id: suggestionId, has_bug: hasBug },
            };
    
            trackEvent(logData);

            return { status: response.status, success: true, data: { suggestions: data.suggestions, suggestionId, hasBug } };
        }

        return { status: response.status, success: false, error: data.error || "Unknown error" };
    } catch (error: any) {
        return { status: 500, success: false, error: error.message || "Unknown error" };
    }
}

/**
 * Logs the user's decision on an AI-generated suggestion.
 *
 * @param {LogData} logData - The data being logged.
 */
export function trackEvent(logData: LogData): void {
    const body = JSON.stringify(logData);

    console.log("Logging event...", body);

    fetch(LOG_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body,
    }).catch(err => console.error("Failed to log data:", err));
}

/**
 * Save AI-generated suggestion.
 *
 * @param {Suggestion} suggestion - The suggestion text that was acted upon.
 */
async function saveSuggestionToDatabase(suggestion: Suggestion) : Promise<Result<Suggestion>> {
    const body = JSON.stringify(suggestion);

    console.log("Saving suggestion...", body);

    try {
        const response = await fetch(LOG_SUGGESTION_ENDPOINT, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: body,
        });

        if (!response.ok) {
            return {
                status: response.status,
                success: false,
                error: `Error: ${response.status} ${response.statusText}`,
            };
        }

        const data: Suggestion = await response.json();
        return {
            status: response.status,
            success: true,
            data: data,
        };
    } catch (err) {
        console.error("Failed to save suggestion:", err);
        return {
            status: 500,
            success: false,
            error: "Failed to connect to server.",
        };
    }
}