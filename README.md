[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17850502)
<div align="center">

# Github Copilot Clone
## Team 2
[![Report Issue on Jira](https://img.shields.io/badge/Report%20Issues-Jira-0052CC?style=flat&logo=jira-software)](https://temple-cis-projects-in-cs.atlassian.net/jira/software/c/projects/GCCB/issues)
[![Deploy Docs](https://github.com/ApplebaumIan/tu-cis-4398-docs-template/actions/workflows/deploy.yml/badge.svg)](https://github.com/Capstone-Projects-2025-Spring/project-copilot-clone-2/actions/workflows/deploy.yml)
[![Documentation Website Link](https://img.shields.io/badge/-Documentation%20Website-brightgreen)](https://capstone-projects-2025-spring.github.io/project-copilot-clone-2/)


</div>


## Keywords
Section 001
GitHub Copilot Clone, generative AI, AI coding assistants, Education Technology, VS Code Extension, early programmers

## Project Abstract

This project aims to develop an AI-powered code assistant similar to GitHub Copilot but with an educational focus. Unlike existing solutions, our system integrates rich logging and mistake recognition to track user behavior, promote critical reflection, and reduce over-reliance on AI-generated code. By monitoring how users interact with suggestions, and providing real-time interventions, the system will serve as both a coding assistant and a learning tool for novice programmers. Additionally, a statistics portal will allow users to review their coding habits, helping them improve over time. The system will be designed for seamless integration into an IDE, ensuring minimal disruption to the coding workflow while maintaining a fast response time.

## High Level Requirement

The Copilot extension for beginner programmers provides real-time inline coding suggestions as users type, offering both correct and incorrect options to encourage critical thinking. Users can ask questions inline or in a chat about specific code snippets or general programming concepts, and the system responds with explanations while tracking engagement and learning patterns. The extension also logs user interactions, including response time, correctness, and frequently asked questions, allowing instructors to monitor student progress through a dashboard, identify common mistakes, and assign targeted interventions to improve learning outcomes. 🚀

## Conceptual Design
This project will leverage an AI model and API, such as Github's Copilot or OpenAI's Chat GPT, to provide inline code suggestions from a Visual Studio Code extension. The extension will record various statistics for how the suggestions are used and send them to a server. Using our backend we will then be able to display the statistics in a dashboard for the user to be able to track how they are doing.

## Background
AI-powered code assistants like OpenAI's Chat GPT and Github's Copilot have revolutionized software development, enabling programmers to write code faster and with fewer errors. However, they have also hindered the abilities of more novice programmers. These programmers will accept the solution they are given often times without fully understanding the concepts and in some cases without reading the solution. This can lead to a lot of poor programming practices. Our project is trying to address this by implementing a system the provides these intelligent code suggestions but requires the user to fully understand the code they are getting suggested before it is placed in their project. With this approach we hope that AI coding assistance can still be used by newer programmers while still promoting learning and good programming habits.

## Required Resources
**Users will need**:
- An internet connection
- An IDE with support for plugins

**Code Maintenance and Documentation:**
- Git and Github for version control
- Docusaurus for documentation

## Collaborators

[//]: # ( readme: collaborators -start )
<table>
<tr>
    <td align="center">
        <a href="https://github.com/jaimenguyen168">
            <img src="https://avatars.githubusercontent.com/u/77992599?v=4" width="100;" alt="Jamie"/>
            <br />
            <sub><b>Jaime</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/AntonioMongeluzi">
            <img src="https://avatars.githubusercontent.com/u/93612712?v=4" width="100;" alt="Antonio"/>
            <br />
            <sub><b>Antonio</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/sophiem18">
            <img src="https://avatars.githubusercontent.com/u/125143591?v=4" width="100;" alt="Sophie"/>
            <br />
            <sub><b>Sophie</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/NickRucinski">
            <img src="https://avatars.githubusercontent.com/u/143641881?s=96&v=4" width="100;" alt="Nick"/>
            <br />
            <sub><b>Nick</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/tus40499">
            <img src="https://avatars.githubusercontent.com/u/157192065?v=4" width="100;" alt="Jack"/>
            <br />
            <sub><b>Jack</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/ApplebaumIan">
            <img src="https://avatars.githubusercontent.com/u/9451941?v=4" width="100;" alt="ApplebaumIan"/>
            <br />
            <sub><b>Ian Tyler Applebaum</b></sub>
        </a>
    </td>
</tr>
</table>

[//]: # ( readme: collaborators -end )
