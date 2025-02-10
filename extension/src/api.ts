

const AI_ENDPOINT: string = "https://ai.nickrucinski.com/generate";

export async function fetchSuggestions(prompt: string): Promise<string[]> {
    try {
        const response = await fetch(AI_ENDPOINT, {
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