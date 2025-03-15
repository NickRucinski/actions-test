import * as vscode from 'vscode';
import { trackEvent } from '../api/log';
import { LogData, LogEvent } from '../types/event';
import { fetchSuggestions } from '../api/suggestion';

/** 
 * Tracks contextual information for a suggestion, including its unique ID, 
 * whether it contains a bug, and the start time of the suggestion process. 
 */
let suggestionContext = {
    suggestionId: "",
    hasBug: false,
    startTime: 0
};

/** Timeout handler for debouncing text changes */
let debounceTimer: NodeJS.Timeout | null = null;
const TYPING_PAUSE_THRESHOLD = 2000;
let lastRequest: { document: vscode.TextDocument; position: vscode.Position; context: vscode.InlineCompletionContext; token: vscode.CancellationToken } | null = null;

/**
 * Provides inline completion items based on AI-generated suggestions.
 *
 * @param {vscode.TextDocument} document - The active text document.
 * @param {vscode.Position} position - The current cursor position.
 * @param {vscode.InlineCompletionContext} context - The inline completion context.
 * @param {vscode.CancellationToken} token - A cancellation token.
 * @returns {Promise<vscode.InlineCompletionList | vscode.InlineCompletionItem[]>} 
 * A list of inline completion items.
 */
export async function provideInlineCompletionItems(
    document: vscode.TextDocument,
    position: vscode.Position,
    context: vscode.InlineCompletionContext,
    token: vscode.CancellationToken
): Promise<vscode.InlineCompletionList | vscode.InlineCompletionItem[]> {
    return new Promise((resolve) => {
        if (debounceTimer) {
            clearTimeout(debounceTimer); // Clear the previous timer
        }

        // Store the latest request
        lastRequest = { document, position, context, token };

        // Set a new timer
        debounceTimer = setTimeout(async () => {
            if (lastRequest) {
                const { document, position, context, token } = lastRequest;
                const prompt = getPromptText(document, position);

                const result = await fetchSuggestions(prompt);

                if (result.success && result.data) {
                    const { suggestions, suggestionId, hasBug } = result.data;

                    suggestionContext = { 
                        suggestionId, 
                        hasBug,
                        startTime: Date.now()
                    };

                    // Create InlineCompletionItems
                    const completionItems = suggestions.map(suggestion => new vscode.InlineCompletionItem(suggestion));

                    resolve(completionItems);
                } else {
                    resolve([]); // Resolve with an empty array if no suggestions are available
                }
            }
        }, TYPING_PAUSE_THRESHOLD); // Debounce delay of 300ms
    });
}

/**
 * Extracts the text from the beginning of the current line to the cursor position.
 * This is used to generate a prompt for inline suggestions.
 *
 * @param {vscode.TextDocument} document - The active text document.
 * @param {vscode.Position} position - The current cursor position.
 * @returns {string} The text from the start of the line to the cursor position.
 */
const getPromptText = (document: vscode.TextDocument, position: vscode.Position): string => {
    return document.getText(new vscode.Range(position.with(undefined, 0), position));
};

/**
 * Registers a command to accept the current inline suggestion.
 * Commits the inline suggestion and logs the acceptance event.
 */
export const acceptSuggestion = vscode.commands.registerCommand(
    'copilotClone.acceptInlineSuggestion',
    async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {return;}

        await vscode.commands.executeCommand('editor.action.inlineSuggest.commit');

        logSuggestionEvent(true);
    }
);

/**
 * Registers a command to reject the current inline suggestion.
 * Hides the inline suggestion and logs the rejection event.
 */
export const rejectSuggestion = vscode.commands.registerCommand(
    'copilotClone.rejectInlineSuggestion', 
    async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {return;}

        await vscode.commands.executeCommand('editor.action.inlineSuggest.hide');
        await vscode.commands.executeCommand('hideSuggestWidget');

        logSuggestionEvent(false);
    }
);

/**
 * Logs an event when a suggestion is either accepted or rejected.
 * Tracks the elapsed time, suggestion ID, and whether the suggestion was accepted.
 * Resets the suggestion context after logging.
 *
 * @param {boolean} accepted - Whether the suggestion was accepted (true) or rejected (false).
 */
const logSuggestionEvent = (accepted: boolean) => {
    const { suggestionId, hasBug, startTime } = suggestionContext;
    const elapsedTime = Date.now() - startTime;

    const logEventType = accepted ? LogEvent.USER_ACCEPT : LogEvent.USER_REJECT;
    const logData: LogData = {
        event: logEventType,
        time_lapse: elapsedTime,
        metadata: { userId: "12345", suggestionId, hasBug: false }
    };

    trackEvent(logData);
    suggestionContext = { suggestionId: "", hasBug: false, startTime: 0 }; // Reset context
};