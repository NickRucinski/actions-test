---
sidebar_position: 2
---

# System Block Diagram

![block-diagram drawio (1)](https://github.com/user-attachments/assets/a063644b-e397-4151-8204-62cafcb27d37)
**Figure 1.** Architecture design of the *Github Copilot Clone* application.

## Description

The system architecture is designed to function as a GitHub Copilot-style AI coding assistant, providing real-time inline code suggestions while monitoring user engagement and learning patterns. It consists of three main components: the Client, Server, and AI Model, working together to analyze user input and deliver intelligent code completions.

The Client integrates directly into the user's IDE, continuously analyzing their typing patterns to determine when to send prompts to the AI Model for inline code suggestions. Users can accept, reject, or modify these suggestions, and these interactions are logged to track their progress. A web interface is also available for administrators (typically instructors) to review user engagement, helping assess how learners interact with the AI-generated recommendations.

The Server manages request processing, and activity logging. It forwards user input to the AI Model and returns the generated suggestions. The system is designed to intentionally introduce minor errors in some suggestions, encouraging users to critically evaluate and refine their code. If a user consistently accepts incorrect suggestions, the system dynamically adjusts the response speed, slowing down code completions to encourage more thoughtful engagement. This behavior is driven by analyzing historical interaction logs stored in the Database, which tracks user actions, accepted or rejected suggestions, and overall accuracy trends.
