import * as vscode from 'vscode';
import { fetchSuggestions, logSuggestionDecision } from './api';
import { getSupabaseClient } from './supabaseClient';
import * as dotenv from 'dotenv';

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
export async function activate(context: vscode.ExtensionContext) {
    // Load environment variables from .env file
    const secretStorage = context.secrets;

    if (!(await secretStorage.get('SUPABASE_URL'))){
        const supabaseUrl = process.env.SUPABASE_URL;
        const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;

        if (supabaseUrl && supabaseAnonKey) {
            await secretStorage.store('SUPABASE_URL', supabaseUrl);
            await secretStorage.store('SUPABASE_ANON_KEY', supabaseAnonKey);
        } else {
            vscode.window.showErrorMessage('Supabase environment variables are not set.');
        }
    }


    console.log("AI Extension Activated");


    // Sign in with email command 
    context.subscriptions.push(
        vscode.commands.registerCommand('copilotClone.signIn', () => signIn(context))
    );
    
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
 * Handles user sign-in, allowing them to select between email or GitHub authentication.
 *
 * @param {vscode.ExtensionContext} context - The VS Code extension context.
 */
async function signIn(context: vscode.ExtensionContext){
    const signInMethod = await vscode.window.showQuickPick(['Sign in with Email', 'Sign in with GitHub'], { placeHolder: 'Choose a sign-in method' });

    if (signInMethod === 'Sign in with Email') {
        signInOrSignUpEmail(context);
    } else if (signInMethod === 'Sign in with GitHub') {
        signInWithGithub(context);
    }
}

/**
 * Signs in or signs up a user using an email and password.
 *
 * @param {vscode.ExtensionContext} context - The VS Code extension context.
 */
//want to make it to sign up but need to look at database, this works for now 
async function signInOrSignUpEmail(context: vscode.ExtensionContext){
    const supabase = await getSupabaseClient(context);
    const email = await vscode.window.showInputBox({ prompt: 'Enter your email', placeHolder: "sample@gmail.com" });

    if (!email) {return;}

    const password = await vscode.window.showInputBox({ prompt: 'Enter your password', placeHolder: "password", password: true });
    if (!password) {return;}

    if (!supabase) {
        vscode.window.showErrorMessage('Supabase client initialization failed.');
        return;
    }
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
        vscode.window.showErrorMessage(`Sign-in failed: ${error.message}`);
    } 
    else {
            vscode.window.showInformationMessage(`Sign-in successful!YAYYYY `);
    }
}

//needs adjusting 
/**
 * Signs in a user using GitHub OAuth authentication.
 *
 * @param {vscode.ExtensionContext} context - The VS Code extension context.
 */
async function signInWithGithub(context: vscode.ExtensionContext){  
    const supabase = await getSupabaseClient(context);
try {
    // Redirect to GitHub for authentication
        vscode.window.showInformationMessage("Redirecting to GitHub for authentication...");
        if (!supabase) {
            vscode.window.showErrorMessage('Supabase client initialization failed.');
            return;
        }
        const { data, error } = await supabase.auth.signInWithOAuth({
            provider: 'github',
    });

    if (error) {
        vscode.window.showErrorMessage(`GitHub sign-in failed: ${error.message}`);
    } 
    if (data?.url) {
        await vscode.env.openExternal(vscode.Uri.parse(data.url));
    }
    else{
        vscode.window.showErrorMessage(`Failed to get OAuth URL.`);
    }
}
catch (error: any) {
    vscode.window.showErrorMessage(`Unexpected Error: ${error.message}`);
}
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

    const suggestions = await fetchSuggestions(prompt);

    if (suggestions.length > 0) {
        const suggestionId = `${document.uri.toString()}-${position.line}-${position.character}`;
        suggestionStartTime.set(suggestionId, Date.now());
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
