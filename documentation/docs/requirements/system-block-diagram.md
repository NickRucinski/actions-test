---
sidebar_position: 2
---

# System Block Diagram

![block-diagram drawio](https://github.com/user-attachments/assets/10f36440-005d-4542-b76f-d8fd2720e426)

## Description

Our system architecture is designed to function as a GitHub Copilot-style AI coding assistant, providing real-time inline code suggestions while monitoring user engagement and learning patterns. It consists of three main components: the Client, Server, and AI Model, working together to analyze user input and deliver intelligent code completions.

The Client integrates directly into the user's IDE, continuously analyzing their typing patterns to determine when to send prompts to the AI Model for inline code suggestions. Users can accept, reject, or modify these suggestions, and these interactions are logged to track their progress. A web interface is also available for instructors to review user engagement, helping assess how learners interact with the AI-generated recommendations.

The Server manages request processing, and activity logging. It forwards user input to the AI Model and returns the generated suggestions. The system is designed to intentionally introduce minor errors in some suggestions, encouraging users to critically evaluate and refine their code. If a user consistently accepts incorrect suggestions, the system dynamically adjusts the response speed, slowing down code completions to encourage more thoughtful engagement. This behavior is driven by analyzing historical interaction logs stored in the Database, which tracks user actions, accepted or rejected suggestions, and overall accuracy trends.
