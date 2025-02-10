---
sidebar_position: 5
---

# Use-case descriptions

![usecase-diagram drawio](https://github.com/user-attachments/assets/86431fe1-9930-4664-9f82-1886c0415d87)

**Figure 1.** UML Use Case Diagram of the *Github Copilot Clone* application.

## Actors
Our project has multiple actors, meaning that different use cases are needed to describe how each actor interacts with the system. 

* **User (beginner programmers)**: Student learning to program, interacting with our Copilot VS Code Extension for code suggestions and asking questions about concepts. 
* **AI Model**: The AI model running on our system that will create code suggestions, answer concept questions, and generate quizzes. 
* **Administrator**: An instructor that wants to monitor students' progress and review logged data from the system to identify concepts that should be reviewed. 

## Use Cases

### Use Case 1: Receiving Context-Aware Code Suggestions

Actors: User, AI Model

**The user wants to get inline code suggestions to assist with a coding assignment and determine if it is correct or incorrect.**

1. **User** begins typing code.
2. **AI model** analyzes the context of the code and creates a code suggestion (incorrect or correct).
3. System displays the **AI model** suggestion.  
4. **User** reviews the suggestion and determines if it is correct or not. 
5. **User** selects “Accept” if they think the code is right or “Reject” if they believe it is wrong.
6. System logs the user’s choice, time it took for the user to make a decision, and whether or not it was correct. 
7. *If the user accepts an incorrect suggestion, the **AI model** gives an explanation of the mistake.*

### Use Case 2: Asking Inline Questions about Code

Actors: User

**The user wants to ask a question about a specific piece of code inline while coding.**

1. **User** highlights a portion of their code.
2. **User** clicks on "ask Copilot" to type a question. 
3. **AI model** provides an explanation for the question. 
4. **User** reviews the response.
5. System logs the user’s question and whether the user requested further clarification. 

### Use Case 3: Asking Questions in the Copilot chat

Actors: User, AI Model

**The user wants to ask a general programming question about a coding concept.**

1. **User** opens ai model chat. 
2. **User** types a question (e.g. "How do for loops work in Java?")
3. **AI model** processes the question and returns an answer.
4. **User** reviews the response.
5. System logs the user’s question and whether the user requested further clarification. 

### Use Case 4: Logging Decision Time for Code Suggestions

Actors: User, AI Model

**The system has to track how long a user takes to accept or reject a suggestion to ensure the user is actually engaging with the code.**

1. System begins a timer when it suggests code to the user.  
2. **User** reviews the suggestion (as quickly or slowly as they want).
3. **User** accepts or rejects the suggestion. 
4. System stops the timer and logs the response time.
5. *If the user consistently makes quick and random wrong selections, the system flags them for potential disengagement or lack of knowledge on the subject matter.*


### Use Case 5: Receiving Feedback After Selecting a Suggestion. 

Actors: User

**The user wants to receive feedback on whether they correctly identified a suggestion as right or wrong.**

1. **User** accepts or rejects a suggestion.   
2. System determines if the user's choice was correct. 
3. *If the **user** chooses correctly, system provides confirmation.*
4. *If the **user** chooses incorrectly, system provides an explanation of the mistake.* 
5. System logs the mistake for admin review. 

### Use Case 6: Tracking and Logging User Decisions

**The system has to track user engagement, correctness, and common errors.**

1. System logs each accepted or rejected code suggestion. 
2. System tracks if the choice was correct or incorrect.
3. System records how long the user took to decide on accepting or rejecting. 
4. *If user frequently accepts incorrect suggestions, system logs recurring mistakes for admin review.*
5. *If multiple users make the same mistakes, system flags the concept as a struggle area.*

### Use Case 7: Identifying Common Student Mistakes
Actors: AI Model

**The AI model will identify patterns that the system has logged based on incorrect suggestions and user struggles.** 

1. System records incorrect suggestions that user accepts. 
2. The **AI model** analyzes repeated mistakes, and extracts the concepts that need work. 
3. The concept extracted by the model will be flagged by the system to be reviewed by the administrator.

### Use Case 8: Identifying Common Student Mistakes 

Actors: AI Model

**System identifies patterns in incorrect suggestions and concepts the user struggles with.** 

1. **AI Model** keeps logs of its own suggestions.  
2. **AI Model** tracks key points in the suggested code that the user continuously mistakes as correct.  
3. **AI Model** suggests similar code to the user that builds knowledge for the concepts that are struggled with.  
4. If the incorrect suggestion is chosen again, the pattern will be updated based on the user's response.  
5. New suggestions will be made that will allow the user to learn from their mistakes.  

### Use Case 9: Generating Learning Reports for Administrators

Actors: AI Model, Administrator

**System compiles the user data into a detailed report for instructors.** 

1. **AI Model** will keep track of the users selections on different code prompts.  
2. The user's performance data will be placed into a formatted report for the instructor.  
3. Report will show percentages for the users answers to the code suggestions that were either correct or incorrect.  
4. The administrator can see which areas of learning need more focus for the user (student).  

### Use Case 10: Monitoring User’s (Student) Progress

Actors: Administrator, AI Model 

**Administrator wants to track students’ learning and figure out concepts that might need extra review.**

1. **AI Model** will show the users weekly or monthly progress from the detailed report.  
2. **AI Model** will show a breakdown of computer science topics that the user has been struggling with the most.  
3. The **Administrator** can view different students' progress on a weekly basis and see if areas that need improvement are getting better, plateauing, or declining.  
4. If multiple students are making similar errors in the same areas of their code, extra review on these topics can be implemented.  

### Use Case 11: AI Generated Quiz Based off Previous Topics

Actors: User, AI Model

**The AI Model will supply the user with a weekly quiz on topics that were in the code suggestions the week prior.**  

1. **AI Model** will log topics that are discussed throughout each week.  
2. **AI Model** will determine which areas students need most improvement in based off of their learning reports.  
3. **AI Model** generates the quiz and makes it available to the users.  
4. The User takes a new quiz every week.  
5. **AI Model** tracks correct and incorrect quiz responses and makes results available to both the user and the administrator.  
6. The **User** can view their results as well as a review on why they answered incorrectly on some questions if necessary.  

