Project Log: JudicialFlow - Automated Court Staffing Engine

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-green?style=flat&logo=django)
![React](https://img.shields.io/badge/React-18-blue?style=flat&logo=react)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=flat&logo=postgresql)
![Status](https://img.shields.io/badge/Status-In_Development-orange)

1. Project Objective
I initiated this project to solve a complex operational bottleneck: the monthly scheduling of court staff. Currently a manual, high-friction process, this task requires balancing "Hard Constraints" (legal mandates, report days, holidays) against "Soft Constraints" (fairness, rotation, burnout prevention).

My primary goal is to build a full-stack web application that transitions this process from manual entry to algorithmic generation, while simultaneously architecting a database capable of providing long-term workforce analytics.

2. Architectural Decisions: The Move to Full-Stack
Unlike simple data scripts, this application requires real-time user interaction and complex state management. I deliberately chose a decoupled Client-Server Architecture:

Backend (Python/Django & DRF): I selected Python to leverage its robust ecosystem for both web standards and mathematical optimization. Django REST Framework (DRF) serves as the interface layer, serializing complex schedule data into JSON for the frontend.

Database (PostgreSQL): I moved away from lightweight SQLite to PostgreSQL to handle concurrent user writes and to utilize advanced date/time querying features essential for schedule conflict detection.

Frontend (React.js): I chose React to build a highly interactive Single Page Application (SPA). This allows for a dynamic "Calendar View" where the administrator can drag-and-drop shifts without reloading the page, providing a seamless user experience that matches commercial SaaS tools.

3. Database Schema & Data Modeling
The primary engineering challenge identified was that while Agents have static availability (8:00–5:00 M-F), the demand (Court Sessions) follows complex, recurring patterns unique to each Judge.

I normalized the database into three conceptual modules:

A. The People (Static Data)
Supervisor (User Model): Handles authentication and Role-Based Access Control (RBAC). Supervisors have Write access; Agents have Read-Only access to view their schedules.

Agent:

Report Day Constraint: A "Hard Constraint" (0-4, Mon-Fri) where the agent is strictly forbidden from covering court.

Specialization Logic: Agents are not just "Specialized" or "General"; they are mapped to specific Judges via a relationship table (see below).

Judge:

Location Ownership: Since Judges "own" their courtrooms, location data is denormalized into the Judge entity to reduce complexity.

B. The Logic Entities (Pattern Generation)
RecurringCourtSlot: Defines the standard monthly requirements (e.g., "Judge Smith sits every Tuesday at 9:00 AM"). This allows the scheduler to generate a "Skeleton Schedule" automatically without manual input every month.

SpecialtyAssignment: A relational mapping table that handles the complex specialization rules:

Type 1 (Hybrid): Agent covers a specific Judge's court but remains in the general rotation pool for other times.

Type 2 (Exclusive): Agent covers a specific Judge's court and is removed from the general rotation pool entirely.

C. The Operations (Transactional Data)
MonthlyAssignment: The final, generated shift. It links an Agent to a Judge for a specific Date and Time.

TimeOffRequest: Tracks non-routine unavailability (Vacation, Sick, Training).

4. The "Waterfall" Scheduling Algorithm
The core innovation of this application is the scheduling engine. Instead of a brute-force approach, the algorithm runs in three prioritized passes:

Pass 0: The "Blocker" Layer (Hard Constraints)
Before assigning anyone, the system identifies where agents CANNOT be.

Fetch Constraints: Retrieve all TimeOffRequests and ReportDays.

Result: A matrix of valid/invalid slots for every agent.

Pass 1: The "Specialist" Layer (Priority Assignments)
The system locks in the experts first.

Identify Specialized Slots: Find slots belonging to Judges with linked SpecialtyAssignments.

Assign & Lock:

If Type 2 (Exclusive): The agent is assigned to the judge and marked UNAVAILABLE for the rest of the month's general pool.

If Type 1 (Hybrid): The agent is assigned to the judge but remains available for other slots on different days.

Pass 2: The "General Rotation" Layer (Weighted Optimization)
The system fills the remaining holes using a fairness score.

Scoring Loop: For each empty slot, calculate a "Suitability Score" for every available agent:

Base Score: 100

Fairness Penalty: -10 points for every shift already assigned this month (distributes workload).

Variety Penalty: -20 points if assigned to this specific Judge in the last 30 days (forces rotation).

Consecutive Penalty: -50 points if the agent is already working the morning shift (prevents burnout).

Selection: The Agent with the highest score wins the slot.

5. Data Privacy & "Unofficial" Tooling Strategy
Challenge: As this tool is designed for actual workplace use, it will eventually process real employee names, which cannot be exposed in a public portfolio.

Solution:

Environment Configuration: All sensitive configuration (Secret Keys, DB Passwords) is loaded via .env files, strictly excluded via .gitignore.

Mock Seeding Protocol: I created a management command script (seed_mock_data.py) that populates the database with fictitious Agents and Judges. This allows recruiters to clone and run the full application logic without accessing production data.

6. Future Roadmap: Analytics
Beyond scheduling, the system is designed to answer: "Are our assignments fair?" The normalized schema allows for SQL Window Functions (e.g., PARTITION BY agent_id) to calculate rolling averages of workload distribution, which will populate an "Admin Dashboard" in future versions.