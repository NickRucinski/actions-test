---
sidebar_position: 7
---

# Version Control

## Overview

The project is managed using **Git** and **GitHub**. The Git repository serves as a **monorepo** that integrates the following key components:

- **Docusaurus Documentation** 📚 – Project documentation
- **Extension** 🛠 – Frontend & logic handling
- **WebServer** 🌐 – Backend operations

## Branching Strategy

### Main Branch (`main`)

- The `main` branch holds the most **stable and up-to-date** version of the project.
- No direct commits are allowed—changes are merged via **pull requests**.

### Sprint Branch (`GCCB-SP#-main`)

- At the start of each **Sprint**, a new **working branch** from `main` is created in the format: `GCCB-SP#-main` (e.g., `GCCB-SP3-main` for Sprint 3)
- This branch **accumulates all changes and features** during the sprint.
- It ensures `main` remains clean while providing a dedicated branch for sprint development.

### Feature Branches (`GCCB-[#]-`)

- Feature branches are created from the current `GCCB-SP[#]-main` branch through **Jira**.
- Naming convention: `GCCB-#-` where `#` is the Jira issue number.
- These branches are task-specific and linked to Jira issues.

### **End of Sprint Merging**

- At the end of each sprint, the final stage of `GCCB-SP#-main` will be reviewed and merged back into `main`.
- Ensures all changes are stable before reaching production.

## Branch Protection Rules

Rules are strictly enforced to maintain code quality and security:

| Branch          | Approval Required | Direct Pushes  |
| --------------- | ----------------- | -------------- |
| `main`          | 2 approvals       | ❌ Not allowed |
| `GCCB-SP#-main` | 1 approval        | ❌ Not allowed |

## Pull Request Process

1. **Create a Feature Branch** (`BP-#`) from the sprint branch.
2. **Push changes** and open a PR for review.
3. **Review & Approvals:**

- Feature branches: **1 approval** (Sprint Branch)
- Sprint branches: **2 approvals** (`main`)
