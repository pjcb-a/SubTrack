💳 SubTrack - Subscription Management Simplified

SubTrack is a full-stack dashboard designed to help users take control of their recurring expenses. By centralizing subscription data, it provides clarity on spending habits and ensures you never get surprised by a renewal again.

🚀 The Problem

In the modern digital economy, "subscription fatigue" is real. Users often lose track of:

    Hidden Costs: Small monthly fees that add up to significant annual drains.

    Renewal Surprises: Forgetting when a trial ends or an annual fee is due.

    Waste: Paying for services that are no longer being used because they are "out of sight, out of mind."

💡 The Solution

SubTrack negates these issues by providing a unified command center. It transforms raw subscription data into actionable insights through:

    Dynamic Filtering: Instantly view costs by cycle (Weekly, Monthly, Annual).

    Visual Distribution: See exactly how your budget is split across different payment frequencies.

    Proactive Tracking: A dedicated "Upcoming Payments" list that highlights renewals due in the next 7 days.

🛠️ Technical Necessity (Getting Started)

To run the frontend and interact with the backend features implemented, you need the following setup:
Prerequisites

    Node.js (v16+)

    Python 3.8+ (for the backend API)

Frontend Installation

    Navigate to the root directory.

    Install dependencies:
    Bash

    npm install

    Start the development server:
    Bash

    npm run dev

Backend Installation

    Navigate to the /backend folder.

    Create and activate a virtual environment:
    Bash

    python3 -m venv venv
    source venv/bin/activate

    Install requirements:
    Bash

    pip install -r requirements.txt

    Run the server:
    Bash

    python app.py

📂 Project Navigation

    src/components/dashboard/: Contains the core UI blocks like StatGrid.vue (the main data display) and ControlBar.vue (the action/filter hub).

    src/composables/: Logic for managing state, specifically useSubscriptions.js which syncs data across components.

    src/style.css: The global design system, including the Light and Dark theme variables.

    backend/: The Flask/Python API handling user authentication and subscription storage.

For a more complete localhost/device setup guide with PostgreSQL instructions, see [backend/LOCALHOST_SETUP.md](./backend/LOCALHOST_SETUP.md).
