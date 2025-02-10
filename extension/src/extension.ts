import * as vscode from 'vscode';
import { fetchSuggestions } from './api';

export function activate(context: vscode.ExtensionContext) {
    console.log("AI Extension Activated");

    context.subscriptions.push(
        vscode.languages.registerInlineCompletionItemProvider(
            { scheme: 'file' },
            {
                provideInlineCompletionItems
            }
        )
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

export function deactivate() {
    console.log("AI Extension Deactivated");
}
