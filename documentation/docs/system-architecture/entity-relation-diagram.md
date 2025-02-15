---
sidebar_position: 3
---

# Entity Relation Diagram

This **database schema** represents an **AI-assisted code suggestion** and **user progress tracking system**. It consists of entities for **users**, **admins**, **AI models**, **code suggestions**, and **progress tracking**. 

- The **AI-MODEL** generates **CODE-GENERATION** entries that lead to **CODE-SUGGESTION** records, which users interact with.
- Users respond to suggestions, marking them as correct or modifying them, and these interactions are recorded in **CODE-RESPONSE**.
- **ADMIN** oversees user progress, tracking warnings and limitations in the **PROGRESS** table, which stores levels and statuses based on user activity.
- The **PROGRESS-RESPONSE** table links progress tracking to specific code suggestions.

This schema enables monitoring of **user engagement** with AI-generated code suggestions while maintaining administrative oversight.
