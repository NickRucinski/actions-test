---
sidebar_position: 2
---

# Backend API 

## FlaskBackend  

Component used to handle code suggestions, user requests and the flow of suggestions.  

### Methods:

#### `processCodeRequests()`
- Takes incoming user made coding requests generated from the AI tool.  
- **Returns:** `CodeSuggestion`  
    - The AI-generated code response. 

#### `trackUserProgress()`
- Handles the user's suggestion choices.  
- Correct and incorrect modifications and choices are stored and used to track progression or decline while using the copilot tool.  
- Progress data fields are updated with corresponding tracking data.
- **Returns:** `boolean`  
    - `true` if tracking is successful.   

#### `controlSuggestionFlow()`
- Control the frequency of coding suggestions presented to the user.  
- Control where within the user's code the suggestions will be made.
- **Returns:** `void` 

---

## OllamaAI

AI Component that will be used to monitor progress and generate coding suggestions and intentional errors to help the user learn new coding concepts.  

### Data fields

- `modelId: integer`: Classifies which OllamaAI model is being used.  
- `modelName: string`: The name of the AI model that is being used.  
- `price: float`: The price of the AI service.  Monthly or yearly subscription for access to the service and its features.  

### Methods

#### `generateContextAwareSuggestions()`
- Creates an AI generated, correct or incorrect coding suggestion to the user.  
- User's action taken on the suggestions is logged.  
- **Returns:** `CodeSuggestion`  
    - AI-generated code snippet. 

#### `introduceMistakes()`
- Presents the user intentionally incorrct code.  
- Code is generated with what the user is working on in their codespace, requiring careful analysis to determine that it is an error.
- **Returns:** `CodeSuggestion`  
    - Buggy AI-generated code snippet.    

### `adaptToUserProgress()`
- Monitor correct and incorrect suggestion choices and use the AI model to update level and difficulty.  
- Calls the trackUserProgress function.  
- Returns coding suggestions based off of the user's progression.
- **Returns:** `void`  

---

## SupaBase

Component that will provide backend storage and authentification.  

### Methods

#### `authenticateUser()`
- Calls a person's credential information. 
- Confirms information with that in the database to allow for access to an account.
- **Returns:** `boolean`  
    - `true` if authentication is successful.  

### `logUserActivity()`
- Track a user's suggestion choices.  
- Create logs in order to update difficulty of prompts and adapt to progress. 
- Update suggestion settings for different users based off their progress.
- **Returns:** `boolean`  
    - `true` if logging is successful.


