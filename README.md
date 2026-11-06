# Autonomous IT Support Agent

An AI-powered IT infrastructure monitoring and incident investigation system built with Python and the DeepSeek AI Model (`deepseek-chat`).

## Project Overview

The Autonomous IT Support Agent investigates simulated IT infrastructure incidents by analysing server health metrics and application logs.

The system combines Python-based rule-driven investigation with Generative AI to identify potential issues, interpret incident evidence, and recommend troubleshooting actions.

It uses the DeepSeek AI Model (`deepseek-chat`) to provide structured incident analysis while maintaining a clear separation between automated Python investigation logic and AI-generated recommendations.

**Note:** AI provides analysis and recommendations. Service restarts and engineer escalations are simulated Python actions and are not independently executed by DeepSeek.

## Key Features

- **Server Health Monitoring:** Reads CPU, memory, and server status information from JSON files.
- **JSON Schema Validation:** Validates input data against predefined JSON Schemas before processing.
- **Automated Health Classification:** Classifies servers based on health status and resource utilization.
- **Log Investigation:** Analyses server logs to identify errors and potential infrastructure issues.
- **Rule-Based Actions:** Simulates service restarts, engineer escalations, error investigations, and memory investigations.
- **DeepSeek AI Analysis:** Sends incident evidence to the DeepSeek AI Model (`deepseek-chat`) for analysis and troubleshooting recommendations.
- **Error Handling:** Handles schema validation failures and AI API failures without unnecessarily stopping investigations of other servers.
- **Infrastructure Reporting:** Generates a structured text report containing server investigations, AI analysis, and a final summary.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development and automation logic |
| DeepSeek AI Model (`deepseek-chat`) | Generative AI-based incident analysis |
| OpenAI Python SDK | API communication with the DeepSeek service |
| JSON | Storage of server health metrics and application logs |
| JSON Schema | Validation of input JSON data |
| python-dotenv | Loading API credentials from environment variables |
| jsonschema | Python library for JSON Schema validation |
| VS Code | Development environment |

## Project Architecture

The application follows a modular architecture:

- **main.py:** Application entry point. Coordinates server investigation, classification, AI analysis, and report generation.
- **agent/tools.py:** Contains reusable Python functions for loading data, validating schemas, investigating logs, and simulating IT support actions.
- **agent/brain.py:** Handles communication with the DeepSeek AI Model and manages system instructions and AI analysis.
- **data/:** Stores simulated server health information and application logs.
- **schemas/:** Contains JSON Schema definitions for validating input data.
- **reports/:** Stores the generated infrastructure investigation report.
- **.env:** Stores the user's private API key and is excluded from Git tracking.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Autonomous_IT_Support_Agent
```

### 2. Create a Virtual Environment

```bash
py -m venv .venv
```

### 3. Activate the Virtual Environment (Windows PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the DeepSeek API Key

Create a `.env` file in the project root directory.

Copy the contents of `.env.example` into `.env` and replace the placeholder with your own DeepSeek API key:

```text
DEEPSEEK_API_KEY=your_actual_deepseek_api_key
```

**Important:** Never upload your `.env` file or expose your API key publicly.

### 6. Run the Application

```bash
py main.py
```

The application investigates the simulated server data, generates AI-based incident analysis, and saves the results to:

```text
reports/infrastructure_report.txt
```

## Current Limitations

- The project uses simulated server health metrics and application logs rather than monitoring live infrastructure.
- Service restarts and engineer escalations are simulated Python actions.
- The DeepSeek AI Model provides analysis and recommendations but does not directly execute infrastructure changes.
- The application currently processes predefined JSON datasets.

## Future Enhancements

- Integrate with real infrastructure monitoring platforms.
- Implement secure, controlled service restart mechanisms.
- Integrate ticketing systems for automated incident management.
- Add human approval workflows before executing critical actions.
- Develop a web-based monitoring dashboard.
- Introduce persistent incident history and reporting.

## Sample Execution Summary

The application was tested against five simulated servers.

| Metric | Result |
|---|---:|
| Total Servers Investigated | 5 |
| Healthy Servers | 2 |
| Critical Servers | 3 |
| Warning Servers | 0 |
| Successful DeepSeek AI Analyses | 3 |
| Failed DeepSeek AI Analyses | 0 |

The application successfully validated both JSON datasets, investigated server logs, generated AI-based incident analysis, and produced a consolidated infrastructure report.

*These results represent one successful test run using the current simulated datasets.*

## Author

**Aziz Ahmed Mudgal**

GitHub: https://github.com/azizmudgal26-del