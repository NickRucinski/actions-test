---
sidebar_position: 1
---

# System Overview

## Project Abstract
This project aims to develop an AI-powered code assistant similar to GitHub Copilot but with an educational focus. Unlike existing solutions, our system integrates rich logging and mistake recognition to track user behavior, promote critical reflection, and reduce over-reliance on AI-generated code. By monitoring how users interact with suggestions, and providing real-time interventions, the system will serve as both a coding assistant and a learning tool for novice programmers. Additionally, a statistics portal will allow users to review their coding habits, helping them improve over time. The system will be designed for seamless integration into an IDE, ensuring minimal disruption to the coding workflow while maintaining a fast response time.

## Conceptual Design
This project will leverage an AI model and API, such as Github's Copilot or OpenAI's Chat GPT, to provide inline code suggestions from a Visual Studio Code extension. The extension will record various statistics for how the suggestions are used and send them to a server. Using our backend we will then be able to display the statistics in a dashboard for the user to be able to track how they are doing.

## Background
AI-powered code assistants like OpenAI's Chat GPT and Github's Copilot have revolutionized software development, enabling programmers to write code faster and with fewer errors. However, they have also hindered the abilities of more novice programmers. These programmers will accept the solution they are given often times without fully understanding the concepts and in some cases without reading the solution. This can lead to a lot of poor programming practices. Our project is trying to address this by implementing a system the provides these intelligent code suggestions but requires the user to fully understand the code they are getting suggested before it is placed in their project. With this approach we hope that AI coding assistance can still be used by newer programmers while still promoting learning and good programming habits.
