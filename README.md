# Project Log: JudicialFlow - Automated Court Scheduling System

## 1. Project Objective
I initiated this project to build a full-stack automated scheduling engine that solves the logistical "knapsack problem" of court resource allocation. My primary goal was to demonstrate the ability to engineer a complex constraint-satisfaction algorithm in Python, architect a scalable Django backend, and deliver a user-friendly frontend for non-technical stakeholders.

## 2. Architecture & Workflow Decisions
I deliberately moved away from a simple script-based approach to a robust Model-View-Controller (MVC) architecture to ensure scalability and data integrity.

* **Schema Separation:** I isolated the "Business Entities" from "System Users."
    * `Supervisor`: Handles authentication and system access.
    * `Agent`: Represents the staff workforce. This separation allows the system to schedule staff members who do not have (or need) login credentials, mirroring real-world enterprise security requirements.
* **Data Normalization:** I decoupled the schedule "Template" from the "Instance."
    * `RecurringCourtSlot`: Defines the static pattern (e.g., Judge Garcia sits on Mondays).
    * `MonthlyAssignment`: Represents the generated record. This allows for date-specific modifications (e.g., sick leave) without corrupting the master schedule.

## 3. Data Privacy & Security Implementation
**Challenge:** Court scheduling data implies sensitive operational security details regarding judge locations and staff movements.

**Solution:**
* **Environment Isolation:** I configured `.gitignore` to strictly exclude local database files (`db.sqlite3`) and environment configuration files.
* **Role-Based Access:** By leveraging Django's built-in authentication for the `Supervisor` model, I ensured that the scheduling engine is exposed only to authenticated personnel, while the `Agent` data remains protected within the internal logic.

## 4. Engineering "Hard" & "Soft" Constraints
To prove my backend engineering capabilities, I did not want a simple "fill-the-slots" tool. I engineered specific conflicting constraints to simulate the chaos of real-world operations:

* **Hard Constraints (Blockers):** I implemented strict logic to handle `TimeOffRequest` (Vacations) and `RecurringReportDay` (Unavailable days). The system must mathematically reject any attempt to schedule an agent during these blocks.
* **Soft Constraints (Preferences):** I introduced a "Specialist" relationship (`SpecialtyAssignment`) where specific agents must be prioritized for specific judges, but only if they are not otherwise blocked.
* **Capacity Limits:** The system enforces a one-to-one relationship between Agents and Slots per time block to prevent double-booking.

## 5. Pipeline Execution & Logic Engine
To bridge the gap between static database records and a dynamic schedule, I implemented a custom object-oriented engine in `scheduler/engine.py`.

* **The "Waterfall" Algorithm:** I rejected a brute-force approach in favor of a deterministic multi-pass algorithm:
    * **Pass 0 (The Filter):** Pre-calculates a "Blocker Matrix" for the entire month, filtering out unavailability before assignment begins.
    * **Pass 1 (The VIP Lane):** Assigns Specialists to their preferred judges, strictly adhering to the Blocker Matrix.
    * **Pass 2 (The General Pool):** Fills remaining gaps using available agents, running real-time conflict checks against the live schedule.
* **Efficiency:** This approach reduces computational complexity from exponential (checking every agent against every slot) to linear passes.

## 6. Phase 2: API Integration & JSON Serialization
With the logic engine established, I shifted to exposing this data for the frontend.

* **RESTful Architecture:** I integrated the Django REST Framework (DRF) to serialize complex relational data (Agents, Judges, Assignments) into clean JSON endpoints.
* **Endpoint Design:** I engineered specific endpoints (`/api/schedule/` and `/api/generate/`) to decouple the frontend from the backend logic. This allows the scheduling engine to run asynchronously without freezing the user interface.

## 7. Final Validation & Human-in-the-Loop
While the algorithm is efficient, operational reality often requires human intervention. I needed a way to persist manual overrides against the automated engine.

* **The Locking Mechanism:** I engineered an `is_locked` boolean flag on the `MonthlyAssignment` model.
* **Logic Adaptation:** I updated the `scheduler/engine.py` logic to respect this flag. Before clearing a month to re-generate a schedule, the engine checks for "Locked" slots and preserves them. This allows a hybrid workflow where humans handle exceptions, and the AI handles the bulk volume.

## 8. Phase 3: Visualization & Dashboarding
**Status:** Complete
**Tooling:** HTML5, CSS3, Vanilla JavaScript (Fetch API)

To finalize the pipeline, I built an interactive dashboard to present the schedule to management.

* **Asynchronous Data Fetching:** I utilized JavaScript `async/await` patterns to fetch JSON data from the API, ensuring a responsive UI that loads large datasets without page reloads.
* **Visual Status Indicators:** I implemented dynamic CSS styling to visually distinguish between "AUTO" generated assignments and "LOCKED" manual overrides, providing immediate visual feedback on the schedule's integrity.
* **Control Interface:** The dashboard includes direct controls to trigger the Python Logic Engine via API calls, giving the user "One-Click" scheduling power.

### Final Dashboard Artifact
*(Placeholder for Dashboard Screenshot)*

## 9. Tools & Technologies Used
* **Languages:** Python 3.13, JavaScript (ES6+), SQL.
* **Frameworks:** Django 6.0, Django REST Framework.
* **Database:** SQLite (Dev), PostgreSQL (Prod Ready).
* **Frontend:** HTML5, CSS3.

## 10. Project Conclusion
This portfolio project successfully demonstrates a full-stack engineering capability:
* **Architected** a normalized relational database schema to handle complex workforce relationships.
* **Engineered** a multi-pass Python algorithm to solve constraint-satisfaction problems.
* **Integrated** a RESTful API to serve data to a reactive frontend.
* **Delivered** a production-ready dashboard that balances automation with human control.