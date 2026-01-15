# Project Log: JudicialFlow - Automated Court Scheduling System

## 1. Project Objective

The Goal: I initiated this project to build a full-stack automated scheduling engine. The Challenge: In computer science, this is known as the "knapsack problem"—a complex challenge of optimizing limited resources (staff) against specific requirements (court slots). The Outcome: My primary goal was to demonstrate two capabilities simultaneously:

For Engineering: The ability to code a complex "constraint-satisfaction" algorithm in Python and architect a scalable Django backend.

For Operations: The ability to deliver a user-friendly frontend tool that simplifies daily logistics for non-technical stakeholders.

## 2. Architecture & Workflow Decisions

The Strategy: Instead of writing a simple script that might break as data grows, I built this using a robust Model-View-Controller (MVC) architecture. This ensures the software is stable, scalable, and organized.

Separating System Access from Staff Data (Schema Separation):

Technical: I isolated "Business Entities" from "System Users."

Operational: I created a Supervisor model for people who need to log in to the system, and a separate Agent model for the workforce being scheduled.

Why it matters: This mirrors real-world security needs. It allows us to schedule court reporters or staff members without forcing every single employee to have a software login account.

Master Schedule vs. Daily Reality (Data Normalization):

Technical: I decoupled the schedule "Template" from the "Instance."

Operational: The system uses RecurringCourtSlot to define the static pattern (e.g., "Judge Garcia always sits on Mondays"). It uses MonthlyAssignment to track the actual generated record for a specific date.

Why it matters: This allows a manager to handle one-off changes—like a judge being sick next Tuesday—without breaking the permanent "Master Schedule" for the rest of the year.

## 3. Data Privacy & Security Implementation

Challenge: Court scheduling data inherently reveals sensitive operational details, such as judge locations and staff movements.

Solution:

Environment Isolation: Technically, I configured .gitignore to strictly exclude local database files (db.sqlite3) and configuration keys. In layman's terms, this ensures that sensitive internal data is never accidentally uploaded to public code repositories.

Role-Based Access: I leveraged Django’s built-in authentication for the Supervisor model. This ensures the scheduling engine is exposed only to authorized personnel who have logged in, while the underlying Agent data remains protected deep within the system logic.

## 4. Engineering "Hard" & "Soft" Constraints

To prove my backend engineering capabilities, I avoided building a simple "fill-the-slots" tool. I engineered the system to handle the chaos of real-world operations by enforcing specific rules:

Hard Constraints (The "Non-Negotiables"): I implemented strict logic for TimeOffRequest (Vacations) and RecurringReportDay (Unavailable days). The system mathematically rejects any attempt to schedule an agent during these times—preventing human error before it happens.

Soft Constraints (The "Preferences"): I introduced a "Specialist" relationship (SpecialtyAssignment). This tells the AI to prioritize specific agents for specific judges (e.g., a reporter who knows a judge's specific workflow), but only if that agent isn't on vacation.

Capacity Limits: The system enforces a strict one-to-one relationship. An agent cannot be in two courtrooms at once.

## 5. Pipeline Execution & Logic Engine

To bridge the gap between static database records and a dynamic schedule, I wrote a custom engine (scheduler/engine.py) that "thinks" through the schedule.

The "Waterfall" Algorithm: Instead of a brute-force approach (randomly trying combinations), I used a deterministic, multi-pass method:

Pass 0 (The Filter): The system pre-scans the entire month to build a "Blocker Matrix," filtering out anyone who is unavailable before it even starts assigning work.

Pass 1 (The VIP Lane): The system assigns "Specialists" to their preferred judges first, strictly adhering to the unavailability filter.

Pass 2 (The General Pool): The system fills any remaining gaps using available agents, checking for conflicts in real-time.

Efficiency: This approach reduces computational complexity from "exponential" (slow and heavy) to "linear" (fast and lightweight), meaning the schedule generates in seconds, not minutes.

## 6. Phase 2: API Integration & JSON Serialization

With the logic engine working, I needed to make the data visible and usable on the screen.

The Translator (RESTful Architecture): I used the Django REST Framework (DRF). This acts as a translator, converting complex database relationships (Agents, Judges, Assignments) into clean JSON data that the web browser can understand.

Traffic Control (Endpoint Design): I engineered specific "Endpoints" (/api/schedule/ and /api/generate/). This separates the visible dashboard from the heavy lifting in the background. Practically, this allows the scheduling engine to run asynchronously—meaning the user interface doesn't freeze or crash while the schedule is being built.

## 7. Final Validation & Human-in-the-Loop

Algorithms are efficient, but operational reality often requires human judgment. I needed a way to let human managers override the AI.

The "Locking" Mechanism: I engineered an is_locked flag on the MonthlyAssignment records.

Logic Adaptation: I updated the logic engine to respect this flag. Before the system wipes a month to re-generate a schedule, it checks for "Locked" slots and preserves them.

Why it matters: This creates a Hybrid Workflow. A manager can manually set specific days (human handling exceptions), lock them, and then hit "Auto-Schedule" to fill the rest (AI handling the volume).

## 8. Phase 3: Visualization & Dashboarding

Status: Complete Tools: HTML5, CSS3, Vanilla JavaScript (Fetch API)

To finalize the pipeline, I built an interactive dashboard so management can see and control the schedule easily.

Fast Loading (Asynchronous Fetching): I used JavaScript async/await patterns to pull data from the system. This ensures a responsive interface that loads large datasets instantly without reloading the entire page.

Visual Status Indicators: I implemented dynamic color-coding (CSS) to visually distinguish between "AUTO" generated assignments and "LOCKED" manual overrides. This gives the user immediate visual feedback on which parts of the schedule are automated vs. manual.

Control Interface: The dashboard includes simple, direct controls to trigger the Python Logic Engine via API calls, giving the user "One-Click" scheduling power.

### Final Dashboard Artifact

(Placeholder for Dashboard Screenshot)

## 9. Tools & Technologies Used

Languages: Python 3.13, JavaScript (ES6+), SQL.

Frameworks: Django 6.0, Django REST Framework.

Database: SQLite (Development), PostgreSQL (Production Ready).

Frontend: HTML5, CSS3.

## 10. Project Conclusion

This portfolio project successfully demonstrates a full-stack engineering capability that serves real operational needs:

Architected a database structure that handles complex workforce relationships securely.

Engineered a multi-pass Python algorithm to solve the difficult math of scheduling.

Integrated a professional API to connect the data to the user.

Delivered a production-ready dashboard that perfectly balances automation with human control.