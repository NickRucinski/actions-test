---
title: Backend Documentation
sidebar_label: Backend Documentation
---

# **FlaskBackend**  

Component used to handle code suggestions, user requests and the flow of suggestions.  

## **Data Fields**

- No data fields.

## **Methods**

### `processCodeRequests()`
- Takes incoming user made coding requests generated from the AI tool.  
- Returns a response from the database to the user after handling the request.   

### `trackUserProgress()`
- Handles the user's suggestion choices.  
- Correct and incorrect modifications and choices are stored and used to track progression or decline while using the copilot tool.  
- Progress data fields are updated with corresponding tracking data.  

### `controlSuggestionFlow()`
- Control the frequency of coding suggestions presented to the user.  
- Control where within the user's code the suggestions will be made.  
---

# **OllamaAI**

AI Component that will be used to monitor progress and generate coding suggestions and intentional errors to help the user learn new coding concepts.  

## **Data fields**

- modelId, integer: Classifies which OllamaAI model is being used.  
- modelName, string: The name of the AI model that is being used.  
- price, float: The price of the AI service.  Monthly or yearly subscription for access to the service and its features.  

## **Methods**

### `generateContextAwareSuggestions()`
- Creates an AI generated, correct or incorrect coding suggestion to the user.  
- User's action taken on the suggestions is logged.  

### `introduceMistakes()`
- Presents the user intentionally incorrct code.  
- Code is generated with what the user is working on in their codespace, requiring careful analysis to determine that it is an error.  

### `adaptToUserProgress()`
- Monitor correct and incorrect suggestion choices and use the AI model to update level and difficulty.  
- Calls the trackUserProgress function.  
- Returns coding suggestions based off of the user's progression.  
---

# **SupaBase**

Component that will provide backend storage and authentification.  

## **Data fields**

- No data fields

## **Methods**

### `authenticateUser()`
- Calls a person's credential information. 
- Confirms information with that in the database to allow for access to an account.  

### `logUserActivity()`
- Track a user's suggestion choices.  
- Create logs in order to update difficulty of prompts and adapt to progress. 
- Update suggestion settings for different users based off their progress.  
---

# **CodeSuggestion**

Component used to establish the data fields that will be used by the AI model for the education tool.  

## **Data fields**
- suggestionId, String: Identifier to simplify keeping track of AI generated code suggestions.  
- codeSnippet, String: Holder for the AI suggestion.  
- hasBug, Boolean: Specifies if intentional bugs are present.  
- correction, String: Corrected code suggestion.  
- isAccepted, Boolean: Used to identify user's accept response to code suggestions.  
- isCorrectResponse, Boolean: Used to track if the user's accepted response is correct.  
- timeSpent, Float: The amount of time the user takes when responding to code suggestions.  
- dateCreated: dateTime: The date when suggestion prompts were generated.  
- language, String: Indicates what language the user code is being written in so that the suggestions are generated in the same language.  

## **Methods**

- No methods
---
