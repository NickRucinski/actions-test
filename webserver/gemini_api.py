import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="learnlm-1.5-pro-experimental",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[]
)

def get_code_suggestions(prompt: str) -> list[str]:
    """
    Sends the prompt to the model and returns an array of two code snippets:
    one correct and one with a small logic error.

    Args:
        prompt (str): The code snippet to complete (e.g., "function add").

    Returns:
        list[str]: An array containing two code snippets.
    """
    # Combine the predefined instructions with the user's prompt
    full_prompt = f"You are an AI that suggests code snippets in an array, one correct and one with a small logic error, without any explanations, comments, or markdown formatting. Only return the missing part, and do not repeat existing code. The snippets should not generate syntax errors.\n\n{prompt}"

    # Send the prompt to the model
    response = chat_session.send_message(full_prompt)

    # Process the response to ensure it's in the correct format
    suggestions = response.text.strip().split("\n\n")  # Split into correct and incorrect snippets

    # Ensure the response is an array with exactly two elements
    if len(suggestions) == 2:
        return suggestions
    else:
        raise ValueError("Error: The response did not return exactly two snippets.")