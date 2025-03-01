---
sidebar_position: 4
---

# Features and Requirements

## Functional Requirements

### Logging
The system must log user interactions to gather insights on how suggestions are used. Logged data includes:
 - Whether a code suggestion was accepted or rejected
 - How often code suggestions are given to a user
 - How long it takes for a user to accept or reject a suggestion from its generation
### Code Suggestions
- The system must provide **context-aware** code suggestions based on user code
- The system must provide suggestions **inline** in the editor
- The system must be able to **generate correct and incorrect** suggestions
- The system must notify users when they accept an incorrect suggestion.
### User Interaction
- The system allows users to write code as usual within the IDE.
- The system must allow users to manually **mark** a suggestion as correct or incorrect.
### Limitations & Safeguards
The system should encourage **thoughtful code acceptance** by implementing safeguards:
- Users may be temporarily locked out from suggestions after **three incorrect acceptances**.
- A warning message should appear before locking a user out.
- A cooldown period should be implemented before resuming suggestions.

## Nonfunctional Requirements
### Performance
- The system must generate code suggestions **within 5 seconds**, comparable to GitHub Copilot.
### Statistics & Insights
- A **portal/dashboard** should allow users and administrators to access logged statistics, including:
  - User acceptance/rejection rates.
  - Average response time to suggestions.
### Education & Learning
- The system should promote critical reflection in programmers who are still learning
### User Experience
- The system should integrate **seamlessly** into the coding workflow without unnecessary interruptions.
### Maintainability
- The codebase should be **modular and well-documented** to allow easy feature additions and maintenance.