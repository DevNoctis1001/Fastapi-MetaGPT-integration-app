# ProjectX: The Future of AI-Driven Development

Run: uvicorn app.main:app --reload

## Overview

ProjectX stands at the forefront of innovation, seamlessly blending artificial intelligence with software development. This application is not just a tool; it's a revolution in how we approach coding and project management. By integrating directly with GitHub, it offers a unique platform where AI becomes your development partner, capable of generating code, managing your repositories, and automating your development cycles.

## Key Features

- **GitHub Integration**: Start by connecting your GitHub account. Select or create repositories right from the dashboard.
- **AI-Powered Development Cycles**: Engage with an AI agent that understands your needs, asks the right questions, and provides suggestions, including an option to automatically follow the AI's recommendations.
- **Intelligent Code Generation**: The AI agent plans and executes coding tasks, pushing updates directly to your GitHub repositories.
- **Iterative Development and Feedback**: Review the AI's work, provide feedback, and iterate, harnessing the power of AI to refine your projects continuously.

## Technology Stack

- FastAPI for robust backend functionality.
- OAuth 2.0 for secure GitHub authentication.
- MongoDB for efficient data management, powered by Motor for asynchronous operations.
- Octokit.py for seamless GitHub API interactions.

## Getting Started

**Prerequisites**

- Python 3.8 or higher.
- MongoDB installed and running.
- GitHub account for OAuth authentication.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://your-repository-url.git
   cd your-repository-directory
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**:
   - Create a `.env` file.
   - Add necessary configurations like `DATABASE_URL`, `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, etc.

### Running the Application

- Start the server:
  ```bash
  uvicorn app.main:app --reload
  ```
- Access the application at `http://localhost:8000`.

## How ProjectX Works

### User Journey & Workflow

1. **Login and Dashboard**: 
   - Login using your GitHub account.
   - The dashboard allows you to select an existing repository or create a new one.
   - Initiate a new development cycle on the chosen codebase.
   - The dashboard provides a sidebar with repositories and displays code to clone the repo along with the last cycle branches and commits made by ProjectX.

2. **AI Consultation**:
   - Engage in a consultation with an AI agent through an AI agent chat window.
   - The AI will ask pertinent questions about your development goals and offer easy button suggestions to guide your choices, including an option to follow the AI's recommendation directly.

3. **AI-Driven Planning and Execution**:
   - Upon your approval of the AI's plan, the AI starts working on coding tasks for the codebase.
   - The AI initiates a backend development cycle, pushing updates and progress to you.

4. **Review and Feedback**:
   - After the AI completes its tasks, the code is pushed to an appropriately named branch.
   - You can review the AI's work, provide feedback, and either start another cycle with or without the feedback or move towards deploying your app.

### Iterative Development Cycle

This process facilitates an iterative development cycle, enabling continuous improvement and efficient project progression, powered by AI and automated GitHub interactions.


## Remaining Flows

1. **User Authentication Flow**:
   - ✅ Completed.

2. **Repository Management Flow**:
   - [ ] Endpoints for repository interaction.
   - [ ] Database storage for repository details.

3. **AI Consultation and Planning Flow**:
   - [ ] AI agent interaction for project planning.
   - [ ] Database storage for session data.

4. **Task Execution and Code Management Flow**:
   - [ ] AI logic for code execution.
   - [ ] Database updates for task progress.

5. **Development Cycle Management Flow**:
   - [ ] Endpoints for cycle tracking.
   - [ ] Database interactions for project status.

6. **Feedback and Iteration Flow**:
   - [ ] User feedback mechanisms.
   - [ ] Database storage for feedback data.

7. **GitHub Integration Flow**:
   - [ ] Code update logic and branch management.
   - [ ] Database synchronization with GitHub.


## Testing and Scripts

### Testing

- Run the complete test suite:
  ```
  pytest
  ```
- Run an individual test file:
  ```
  pytest tests/test_file_name.py
  ```
- Creating new test cases:
  - Add new test functions in the `tests` directory.
  - Use the FastAPI TestClient for endpoint testing.
  - Mock external services as needed.

### Scripts

- Usage of existing scripts:
  - Follow script-specific instructions in the script files.
  - Run scripts from the command line for tasks like database initialization or cleanup.
- Creating new scripts:
  - Add new Python script files in the `scripts` directory.
  - Include necessary imports and a main function.
  - Document the purpose and usage at the top of each script.


  
## MongoDB TLDR

### MongoDB Server Commands (macOS with Homebrew)

```bash

### Installation and Service Management
```bash
# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB as a background service
brew services start mongodb-community

# Stop MongoDB service
brew services stop mongodb-community

# Restart MongoDB service
brew services restart mongodb-community

# Check MongoDB service status
brew services list

```

### Basic MongoDB Shell Commands

```bash
# Show all databases
show dbs

# Use/create a specific database
use <database_name>

# Show all collections in current database
show collections

# Find all documents in a collection
db.<collection_name>.find()

# Find specific documents in a collection
db.<collection_name>.find({<query>})

# Insert a new document into a collection
db.<collection_name>.insert({<document_data>})

# Update a document in a collection
db.<collection_name>.update({<query>}, {<update_data>})

# Delete a document from a collection
db.<collection_name>.remove({<query>})

# Count documents in a collection
db.<collection_name>.count()

# Create an index on a collection
db.<collection_name>.createIndex({<field>: 1})

# Aggregate data
db.<collection_name>.aggregate([{$group: {_id: "$<field>", total: {$sum: 1}}}])

# Drop a collection
db.<collection_name>.drop()

# View current database stats
db.stats()

```

### More MongoDB Server Commands
``` bash

# Run MongoDB without Homebrew service
mongod --config /usr/local/etc/mongod.conf

# Open MongoDB Shell (MongoDB must be running)
mongo

# View MongoDB version
mongod --version

# Check MongoDB server status
db.serverStatus()

# View MongoDB log file
cat /usr/local/var/log/mongodb/mongo.log

# Repair MongoDB
mongod --repair

# Change DB path (requires updating mongod.conf)
mongod --dbpath /path/to/new/db

# Enable MongoDB authentication
mongod --auth

# Shutdown MongoDB from within MongoDB shell
use admin
db.shutdownServer()

# Export data from MongoDB to a JSON/CSV file
mongoexport --db=db_name --collection=collection_name --out=filename.json

```