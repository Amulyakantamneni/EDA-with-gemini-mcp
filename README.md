# EDA-with-gemini-mcp

## Overview
The EDA MCP Server is a powerful tool for performing exploratory data analysis (EDA) with the help of an MCP server and AI-driven insights. It supports:

- Uploading datasets (CSV format).
- Generating schema-aware visualizations.
- Explaining charts using AI (Gemini API).
- Interactive dashboards for data exploration.

## Features
- **MCP Server Integration**: Connects to an MCP server for chart generation.
- **AI-Powered Insights**: Uses the Gemini API to provide explanations for generated charts.
- **Streamlit Dashboard**: Interactive UI for uploading datasets, generating charts, and exploring insights.

## Prerequisites
- Python 3.8+
- Node.js (for MCP server)
- Required Python packages (see `requirements.txt`)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd EDA-MCP-Server
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Node.js is installed:
   ```bash
   node -v
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your Gemini API key:
     ```env
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage
1. Start the MCP server:
   ```bash
   node server.js
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open the app in your browser and upload a dataset to begin.

## File Structure
```
EDA MCP Server/
├── app.py                # Main Streamlit app
├── server1.py            # MCP server script
├── handlers/             # Contains dataset and chart handlers
├── utils/                # Utility scripts
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── README.md             # Project documentation
```

## Troubleshooting
- **No Running Event Loop**: Ensure the event loop is properly initialized in the app.
- **Chart Generation Fails**: Verify the MCP server is running and accessible.
- **Gemini API Errors**: Check your API key and usage limits.

## License
This project is licensed under the MIT License.
