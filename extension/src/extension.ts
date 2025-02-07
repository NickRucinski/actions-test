import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log("AI Extension Activated");

    // Register an Inline Completion Provider
    const provider: vscode.InlineCompletionItemProvider = {
        async provideInlineCompletionItems(document, position, context, token) {
            const prompt = document.getText(new vscode.Range(position.with(undefined, 0), position));

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
                    return {
                        items: [new vscode.InlineCompletionItem(data.suggestions[0])],
                    };
                }
            } catch (error) {
                console.error("Error fetching AI suggestion", error);
            }
        }
    };

    context.subscriptions.push(
        // Currently only for JavaScript files. Need to look into how to support other languages
        vscode.languages.registerInlineCompletionItemProvider(
            { 
                scheme: 'file',
                language: 'javascript'
            },
            provider
        )
    );
}

export function deactivate() {
    console.log("AI Extension Deactivated");
}
