import * as vscode from 'vscode';

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

async function fetchSuggestions(prompt: string): Promise<string[]> {
    try {
        const response = await fetch("https://ai.nickrucinski.com/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt })
        });

        if (!response.ok) {
            throw new Error("HTTP ERROR: " + response.statusText);
        }

        const data = await response.json() as { suggestions: string[] };
        if (data.suggestions && data.suggestions.length > 0) {
            return data.suggestions;
        }
    } catch (error) {
        console.error("Error fetching AI suggestion", error);
    }
    return [];
}

export function deactivate() {
    console.log("AI Extension Deactivated");
}
