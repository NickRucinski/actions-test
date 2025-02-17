---
sidebar_position: 2
---

# Sequence Diagrams for Our Use Cases

## Use Case 1: Recieving Context-Aware Code Suggestions

```mermaid
    sequenceDiagram
    actor User as User
    participant System as System
    actor AI Model as AI Model
    User ->> System: Begins typing code
    System ->> AI Model: Sends code context
    AI Model -->> System: Returns code suggestion
    System -->> User: Displays AI model suggestion
    User ->> System: Reviews and accepts/rejects suggestion
    System ->> System: Logs user’s choice, decision time, correctness
    alt User accepts incorrect suggestion
    System ->> AI Model: Request explanation of mistake
    AI Model -->> System: Provides explanation
    System -->> User: Displays explanation
    end
```
## Use Case 2: Asking Inline Questions about Code

```mermaid
sequenceDiagram
 actor User as User
 participant System as System
 actor AI Model as AI Model
   User->>System: Highlights code and clicks "ask Copilot"
   User->>System: Types question
   System->>AI Model: Sends question
   AI Model-->>System: Provides explanation
   System-->>User: Displays response
   alt User requests clarification
       User->>System: Requests further clarification
       System->>AI Model: Sends clarification request
       AI Model-->>System: Provides detailed clarification
       System-->>User: Displays detailed clarification
   end
   System->>System: Logs user’s question and clarification request

```


## Use Case 3: Asking Questions in the Copilot Chat 

```mermaid
sequenceDiagram
 actor User as User
 participant System as System
 actor AI Model as AI Model
   User->>System: Opens AI model chat
   User->>System: Types question
   System->>AI Model: Sends question
   AI Model-->>System: Returns answer
   System-->>User: Displays response
   alt User requests clarification
       User->>System: Requests further clarification
       System->>AI Model: Sends clarification request
       AI Model-->>System: Provides detailed clarification
       System-->>User: Displays detailed clarification
   end
   System->>System: Logs question and clarification request
```


## Use Case 4: Logging Decision Time for Code Suggestions

```mermaid
sequenceDiagram
 actor User as User
 participant System as System


   System->>System: Starts timer with code suggestion
   User->>System: Reviews suggestion
   User->>System: Accepts or rejects suggestion
   System->>System: Stops timer and logs response time
   alt User makes quick, random wrong selections
       System->>System: Flags user for disengagement
   end
```


## Use Case 5: Recieving Feedback After Selecting a Suggestion

```mermaid
sequenceDiagram
    actor User as User
    participant System as System
   User->>System: Accepts/rejects suggestion
   System->>System: Determines correctness
   alt User chooses correctly
       System-->>User: Provides confirmation
   else User chooses incorrectly
       System-->>User: Provides explanation of mistake
   end
   System->>System: Logs mistake or correctness for admin review
```

## Use Case 6: Tracking and Logging User Decisions
```mermaid 
sequenceDiagram
   participant System
   participant Database

   System->>Database: Logs accepted/rejected suggestions
   System->>Database: Tracks correctness
   System->>Database: Records decision time
   alt Frequent incorrect suggestions
       System->>Database: Logs recurring mistakes for admin review
   end
   alt Multiple users with same mistakes
       System->>Database: Flags concept as struggle area
   end
```

## Use Case 7: Identifying Common Student Mistakes
```mermaid
sequenceDiagram
    actor AI model
    participant Database
    participant System
    participant Administrator

    System->>Database: Records incorrect suggestions
    System->>AI Model: Sends data for analysis
    AI Model-->>System: Extracts concepts needing work
    System->>Database: Stores flagged concept for the user
    System-->>Administrator: Flags concepts for review
```
## Use Case 8: Generating Learning Reports for Administrators
```mermaid
sequenceDiagram
   participant User
   participant AI Model
   participant Administrator


   User->>AI Model: Makes selections from AI suggestions
   AI Model->>AI Model: Keeps track of user selection data
   AI Model->>AI Model: Calculates percentages of correct and incorrect responses
   alt User makes a correct selection
       AI Model->>AI Model: Tracks this data in a 'correct' category
   else User makes an incorrect selection 
       AI Model->>AI Model: Tracks this data in an 'incorrect' category
   end
   AI Model->>AI Model: Puts user data into a formatted performance report table/page
   Administrator->>Administrator: Review the report

```
## Use Case 9: Monitoring User's Progress
```mermaid
sequenceDiagram
   participant Administrator
   participant AI Model


   Administrator->>AI Model: Views the students weekly or monthly progress report
   AI Model->>Administrator: Displays report of user data
   alt User is struggling with a certain topic
       AI Model->>Administrator: Provides a breakdown of the user's struggled topics
   else User is progressing with new topics
       AI Model->>Administrator: Provides a confirmation of good progress
   end
   alt Multiple students are making similar errors
       AI Model->>Administrator: Generates extra review for these topics
   else The class is grasping new concepts
       AI Model->>Administrator: Confirms successful class progress
   end

```
## Use Case 10: AI Generated Quiz Based off of Previous Topics
```mermaid
sequenceDiagram
   participant User
   participant AI Model
   participant Administrator


   AI Model->>AI Model: Logs topics that were discussed throughout the week
   AI Model->>AI Model: Analyze the users progress reports
   AI Model->> AI Model: Determine which areas need the most improvement
   AI Model->>User: Generates quiz and makes it available to the user
   User->>AI Model: Take the quiz
   AI Model->>AI Model: Grades and logs quiz results


   alt User answered question incorrectly
       AI Model->>User: Provides feedback and correction for the question
   else User answers question correctly
       AI Model->>User: Mark question as correct
   end
   AI Model->>Administrator: Makes quiz results viewable
   Administrator->>User: Distribute results
   User->>User: Review their grades and use AI suggestions to study
```

