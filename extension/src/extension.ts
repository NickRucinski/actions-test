import * as vscode from 'vscode';
import { fetchSuggestions, logSuggestionDecision } from './api';

let timeout: NodeJS.Timeout | undefined;
let lastPrompt = "";
let suggestionStartTime = new Map<string, number>();

export function activate(context: vscode.ExtensionContext) {
    console.log("AI Extension Activated");

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

    const suggestions = await fetchSuggestions(prompt);

    if (suggestions.length > 0) {
        const suggestionId = `${document.uri.toString()}-${position.line}-${position.character}`;
        suggestionStartTime.set(suggestionId, Date.now());
    }

    return suggestions.map(suggestion => new vscode.InlineCompletionItem(suggestion));
}

function getPromptText(document: vscode.TextDocument, position: vscode.Position): string {
    return document.getText(new vscode.Range(position.with(undefined, 0), position));
}

function shouldFetchSuggestion(prompt: string): boolean {
    if (!/\s$/.test(prompt)) { return false; } // Fetch only after a space or punctuation
    //if (prompt === lastPrompt) { return false; } // Avoid redundant requests
    return true;
}

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


export function deactivate() {
    console.log("AI Extension Deactivated");
}
