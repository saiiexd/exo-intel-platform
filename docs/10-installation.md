# Installation

## Local Installation Guide
This document outlines the requisite steps for deploying the complete ExoIntel platform within a localized development environment. 

### Prerequisites
Ensure the target system includes the following foundational dependencies:
*   **Python:** version 3.9 or higher
*   **Node.js:** version 16.x or higher (for the React interface)
*   **PostgreSQL:** version 13 or higher (or compatible relational database)
*   **Git:** for version control access.

### Step 1: Repository Cloning
Begin by cloning the designated repository from the version control host.

```bash
git clone https://github.com/<organization>/exo-intel-platform.git
cd exo-intel-platform
```

### Step 2: Python Environment Configuration
Initialize a secure Python virtual environment to isolate the specific scientific dependencies required by the data pipeline and machine learning models.

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3: PostgreSQL Database Setup
The architecture strictly requires a localized or networked PostgreSQL database to operate.
1. Access your PostgreSQL installation and create a dedicated administrative database.
```sql
CREATE DATABASE exointel_db;
```
2. Note the connection URI schema (`postgresql://username:password@localhost:5432/exointel_db`) for environment configuration. The platform's Object Relational Mapper (ORM) will handle schema generation automatically upon initial execution.

### Step 4: Environment Variable Configuration
The system depends on specific environment parameters. Copy the provided sample environment file to establish local overrides.

```bash
cp .env.example .env
```
Update the `.env` file explicitly defining the database connection string (`DATABASE_URL`) and any necessary API keys for data derivation.

### Step 5: Frontend Initialization
Navigate to the independent React application directory to install dedicated web dependencies.

```bash
cd frontend
npm install
```

The system is now fully prepared for execution.
