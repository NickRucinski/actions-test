---
sidebar_position: 2
---

# Frontend API  
============================= 

## VSCodeExtension

Component that will work with the copilot education tool to allow for specific feature integrations and interactions.  

### Methods

#### `generateSuggestions()`
- Generate code based on what the user has written in VSCode.  
- Returns suggestions to the user from the backend database that are created using API service.
- **Returns:** `CodeSuggestion`  
    - An AI-generated code snippet.   

#### `injectBugs()`
- Create bugs in the users VSCode work space.  
- Method takes in bug suggestions from AI extension that are stored in backend database. 
- **Returns:** `CodeSuggestion`  
    - A buggy code snippet.  

#### `logUserResponse()`
- Actions taken within the extension are logged to the database.  
- Verify the user's action as accept, reject, or modify.  
- User responses are passed to backend database.  
- **Returns:** `boolean`  
    - `true` if the response is logged successfully.

#### `adjustDifficulty()`
- Method to intensify or dial back the difficulty of the AI generated suggestions.  
- VSCode extension will process the users progresss through backend data to properly adjust the difficulty of their suggestions.  
- **Returns:** `void`  

---

## Dashboard  

Component that allows the user to view their progress while using the Copilot tool, as well as for the administrator to provide feedback.

### Methods

#### `displayProgress()`
- Displays the user progress based on `userId` and `progressId` (string or int).
- Fetches `Progress` data fields.
- Accesses user suggestion details to display results and feedback.
- **Returns:** `Progress`  
    - User’s current progress.

#### `provideFeedback()`
- Allows the administrator to give users feedback that can be accessed in their dashboard.
- Updates the level data field for different tasks.
- The `lastUpdated` attribute updates when new feedback is entered.
- **Returns:** `boolean`  
    - `true` if feedback is submitted successfully.

---
