import * as vscode from 'vscode';
import { fetchSuggestions, logSuggestionDecision } from './api';

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

    // Used for logging to see how long it takes to accept a suggestion
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
    const prompt = document.getText(new vscode.Range(position.with(undefined, 0), position));
    const suggestions = await fetchSuggestions(prompt);
    return suggestions.map(suggestion => new vscode.InlineCompletionItem(suggestion));
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
