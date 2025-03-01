import * as vscode from 'vscode';
import { createClient, SupabaseClient } from '@supabase/supabase-js';

/**
 * Retrieves stored Supabase credentials from VS Code's secret storage and initializes a Supabase client.
 *
 * @param {vscode.ExtensionContext} context - The VS Code extension context.
 * @returns {Promise<SupabaseClient | null>} The initialized Supabase client, or null if credentials are missing.
 */
export async function getSupabaseClient(context: vscode.ExtensionContext): Promise<SupabaseClient | null> {
    const secretStorage = context.secrets;

    // Retrieve stored credentials
    const supabaseUrl = await secretStorage.get("SUPABASE_URL");
    const supabaseAnonKey = await secretStorage.get("SUPABASE_ANON_KEY");

    if (!supabaseUrl || !supabaseAnonKey) {
        vscode.window.showErrorMessage("Supabase credentials missing. Please restart VS Code.");
        return null;
    }

    // Return Supabase client instance
    return createClient(supabaseUrl, supabaseAnonKey);
}
