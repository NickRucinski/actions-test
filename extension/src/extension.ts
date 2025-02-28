import * as vscode from 'vscode';
import { fetchSuggestions, logSuggestionDecision } from './api';

/** Timeout handler for debouncing text changes */
let timeout: NodeJS.Timeout | undefined;

/** Stores the last used prompt to prevent redundant requests */
let lastPrompt = "";

/** Maps a unique suggestion ID to its timestamp for tracking elapsed time */
let suggestionStartTime = new Map<string, number>();

/**
 * Activates the VS Code extension.
 *
 * @param {vscode.ExtensionContext} context - The extension context provided by VS Code.
 */
export function activate(context: vscode.ExtensionContext) {
    console.log("AI Extension Activated");

    // Debug command to force a fetch using input from the user.
    let disposable = vscode.commands.registerCommand('copilotClone.testFetch', async () => {
        const userInput = await vscode.window.showInputBox({
            prompt: 'Enter text for suggestions',
        });
        console.log("Test Fetch: \"" + userInput + "\"");

        if (userInput) {
            try {
                const endpoint = vscode.workspace.getConfiguration("copilot-clone").get<string>("debug.AIEndpoint");
                const result = await fetchSuggestions(userInput, endpoint);
                if (result.success) {
                    vscode.window.showInformationMessage(`Suggestions: ${result.data.join(", ")}`);
                } else {
                    vscode.window.showErrorMessage(`Error: ${result.error}`);
                }
            } catch (error) {
                vscode.window.showErrorMessage(`Error fetching suggestions: Unknown Error`);
            }
        }
    });

    // Inline completion provider
    context.subscriptions.push(
        vscode.languages.registerInlineCompletionItemProvider(
            { scheme: 'file' },
            {
                provideInlineCompletionItems
            }
        )
    );

    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(handleTextChange)
    );
}

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
async function provideInlineCompletionItems(
    document: vscode.TextDocument,
    position: vscode.Position,
    context: vscode.InlineCompletionContext,
    token: vscode.CancellationToken
): Promise<vscode.InlineCompletionList | vscode.InlineCompletionItem[]> {
    const prompt = getPromptText(document, position);

    if (!shouldFetchSuggestion(prompt)) {
        return [];
    }

    lastPrompt = prompt;

    const result = await fetchSuggestions(prompt);
    let suggestions: string[] = [];

    if (result.success && result.data) {
        const suggestionId = `${document.uri.toString()}-${position.line}-${position.character}`;
        suggestionStartTime.set(suggestionId, Date.now());

        suggestions = result.data;
    }

    return suggestions.map(suggestion => new vscode.InlineCompletionItem(suggestion));
}

/**
 * Extracts the text from the beginning of the line to the current cursor position.
 *
 * @param {vscode.TextDocument} document - The active text document.
 * @param {vscode.Position} position - The current cursor position.
 * @returns {string} The extracted prompt text.
 */
function getPromptText(document: vscode.TextDocument, position: vscode.Position): string {
    return document.getText(new vscode.Range(position.with(undefined, 0), position));
}

/**
 * Determines whether a suggestion should be fetched based on the prompt.
 *
 * @param {string} prompt - The current prompt text.
 * @returns {boolean} True if a suggestion should be fetched, otherwise false.
 */
function shouldFetchSuggestion(prompt: string): boolean {
    if (!/\s$/.test(prompt)) { return false; } // Fetch only after a space or punctuation
    //if (prompt === lastPrompt) { return false; } // Avoid redundant requests
    return true;
}


/**
 * Handles text document changes and logs whether an AI suggestion was accepted or rejected.
 *
 * @param {vscode.TextDocumentChangeEvent} event - The text document change event.
 */
function handleTextChange(event: vscode.TextDocumentChangeEvent) {
    event.contentChanges.forEach(change => {
        const suggestionId = `${event.document.uri.toString()}-${change.range.start.line}-${change.range.start.character}`;

        if (suggestionStartTime.has(suggestionId)) {
            const startTime = suggestionStartTime.get(suggestionId) || 0;
            const elapsedTime = Date.now() - startTime;
            
            console.log(`Suggestion accepted/rejected after ${elapsedTime}ms`);

            logSuggestionDecision(change.text, elapsedTime);

            suggestionStartTime.delete(suggestionId);
        }
    });
}

/**
 * Deactivates the extension.
 */
export function deactivate() {
    console.log("AI Extension Deactivated");
}
