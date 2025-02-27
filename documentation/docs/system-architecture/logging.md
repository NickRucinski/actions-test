---
sidebar_position: 8
---

# Logging

# Logging for GitHub Copilot Clone

Logging is critical for understanding user behavior and system performance for this project. Logs are used to track user interactions, AI model behavior, and system events. All logs are stored in a **Supabase** database for analysis.

---

## Table of Contents
1. [Introduction to Logging](#1-introduction-to-logging)
2. [Logging Events](#2-logging-events)
3. [Log Format](#3-log-format)
4. [Analysis Scenarios](#4-analysis-scenarios)
5. [Supabase Integration](#5-supabase-integration)
6. [Analyzing Logs](#6-analyzing-logs)
7. [Best Practices](#7-best-practices)

---

## 1. Introduction to Logging

In this project, we log the following events:
- **User Actions**: When a user accepts or rejects a suggestion.
- **AI Model Behavior**: When the AI generates a suggestion or introduces a bug.

All logs are stored in a **Supabase** database for easy querying and analysis.

---

## 2. Logging Events

### 👤 **User Actions**

Tracking user interactions (`accept` and `reject`) provides critical insights into how users respond to AI-generated code.

| Event   | Purpose                                                            | Insights Gained |
|---------|--------------------------------------------------------------------|----------------|
| `accept` | User accepts a suggestion, indicating it may meet their expectations. `Tab` | Helps determine if users are accepting buggy suggestions without noticing. |
| `reject` | User rejects a suggestion, signaling an issue with its quality or relevance. `Backspace` | Indicates users’ ability to identify incorrect or suboptimal code. |

### 🤖 **AI Model Behavior**

Logging AI behavior ensures we understand how often AI introduces bugs.

| Event          | Purpose                                         | Insights Gained |
|---------------|-------------------------------------------------|----------------|
| `generate`    | AI generates a new suggestion.                  | Helps track the amount of generated suggestions. |
| `introduce_bug` | AI intentionally introduces a bug into the suggestion. | Allows tracking whether users detect and reject the introduced bug. |

## 3. Log Format

All logs are structured in JSON format and each log entry contains structured data to facilitate precise analysis:

| Field         | Purpose                                                 | Insights Gained |
|--------------|---------------------------------------------------------|----------------|
| `event_type`  | Identifies the interaction or AI event (e.g., `accept`, `reject`, `generate`). | Enables categorization of user behavior and AI performance. |
| `timestamp`   | Records when the event occurred in ISO 8601 format.   | Allows for time-based trend analysis. |
| `time_lapse`  | Captures the time taken by the user to act on the suggestion (in ms). | Helps measure how long users review suggestions before deciding, or how fast the AI responds |
| `metadata`    | Provides additional context such as user ID, suggestion ID, and bug status. | Supports user-specific or suggestion-specific analysis. |

### Why It’s Important?
- **`time_lapse` Analysis**: If users spend very little time reviewing code but accept most suggestions, they might not be checking thoroughly.
- **Bug Tracking (`bug_introduced`)**: Helps compare the acceptance rates of buggy vs. correct suggestions.
- **Metadata for User Patterns**: By analyzing patterns across multiple users, we can determine who is more or less attentive.

### Example Log Entry
```json
{
  "event_type": "accept",
  "timestamp": "2025-02-21T20:40:52.709Z",
  "time_lapse": 1200,
  "metadata": {
    "user_id": "12345",
    "suggestion_id": "67890",
    "bug_introduced": false
  }
}
```

## 4. Analysis Scenarios

### 🧑‍💻 A user frequently accepts buggy code
- If logs show that a user accepts buggy suggestions within very short `time_lapse`, they may not be reviewing code thoroughly.
- If the user later rejects suggestions more frequently after being exposed to buggy code, they may be learning from past mistakes.

### 🧑‍💻 Users take different amounts of time to decide
- A user who spends more time (`time_lapse`) before accepting a suggestion is likely analyzing it carefully.
- If a user quickly rejects most suggestions, they might have a higher standard or a preference for writing their own code.

### 🧑‍💻 AI generates too many rejected suggestions
- If a high percentage of generated suggestions are rejected, the AI might need improvement in suggestion quality.
- Tracking `introduce_bug` events can help determine whether AI-introduced bugs are too obvious or too subtle.

## 5. Supabase Integration

### 1. **Set Up Supabase**
- Create a Supabase project at [Supabase](https://supabase.com/).
- Create a table named `logs` with the following schema:

```sql
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    time_lapse INTERGER,
    metadata JSONB
);
```

### 2. **Logging to Supabase**
Use the Supabase client to insert logs into the `logs` table.

#### Example: Logging in Python (Flask Backend)
    ```python
    from supabase import create_client, Client
    import json
    from datetime import datetime

    # Initialize Supabase client
    SUPABASE_URL: str = os.getenv('SUPABASE_URL')
    SUPABASE_KEY: str = os.getenv('SUPABASE_KEY')
    client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def log_event(event_type, start_time, metadata=None):
        end_time = datetime.utcnow()
        time_lapse = int((end_time - start_time).total_seconds() * 1000)

        log_entry = {
            "event_type": event_type,
            "timestamp": end_time.isoformat(),
            "time_lapse": time_lapse,
            "metadata": metadata
        }
        
        response = supabase.table("logs").insert(log_entry).execute()
        print("Logged event:", response)
    ```

---

## 6. Analyzing Logs

### Querying Logs in Supabase
Use Supabase's SQL interface or client libraries to query logs.

#### 💡 Query All Logs
    ```python
    def get_all_logs():
        return supabase.table("logs")
    ```

#### 💡 Query Users Frequently Accepting Buggy Code
    ```python
    def get_frequent_bug_acceptors(user_id):
        response = supabase.table("logs")
            .select("metadata->>user_id, time_lapse")
            .eq("event_type", "accept")
            .eq("metadata->>bug_introduced", "true")
            .eq("metadata->>user_id", user_id)
            .execute()
    return response.data
    ```

#### 💡 Query Average Amount of Time to Decide
    ```python
    def get_avg_decision_time(user_id):
        response = supabase.table("logs")
            .select("metadata->>user_id, time_lapse, event_type")
            .eq("metadata->>user_id", user_id)
            .in_("event_type", ["accept", "reject"]) 
            .execute()

        total_time = sum(log["time_lapse"] for log in response.data)
        total_actions = len(response.data)

        avg_time = total_time / total_actions if total_actions > 0 else 0
        return avg_time
    ```

#### 💡 Query AI Rejection Percentage Due to Bugs
    ```python
    def get_ai_rejection_percentage():
        response = supabase.table("logs")
            .select("event_type, metadata->>bug_introduced")
            .in_("event_type", ["accept", "reject"])
            .execute()

        total_actions = len(response.data)
        total_rejections = sum(1 for log in response.data if log["event_type"] == "reject")
        rejection_percentage = (total_rejections / total_actions) * 100 if total_actions > 0 else 0

        return rejection_percentage
    ```
---

## 7. Best Practices

- **Structured Logging**: Always log in JSON format for easy parsing.
- **Avoid Sensitive Data**: Avoid logging sensitive information like API keys or passwords.


