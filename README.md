# Flask MCP Server

A Model Context Protocol server that connects Claude AI to Flask applications and AWS infrastructure.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/flask-mcp-server.git
cd flask-mcp-server

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Flask app path

# Run the MCP server
python flask_app_mcp.py
```

## 🛠️ Features

- **Flask App Management**: Start, stop, monitor Flask applications
- **Health Monitoring**: Check app status and endpoints
- **Route Discovery**: Automatically find Flask routes
- **AWS Integration**: Connect to AWS services
- **Claude AI Integration**: Natural language Flask app control

## 📋 Available Tools

| Tool | Description |
|------|-------------|
| `start-flask-app` | Start your Flask application |
| `stop-flask-app` | Stop the Flask application |
| `check-flask-status` | Check if Flask is running |
| `list-flask-routes` | Show all Flask routes |
| `test-flask-endpoint` | Test specific endpoints |
| `get-flask-logs` | View application logs |
| `deploy-to-aws` | Deploy to AWS |
| `check-aws-resources` | Check AWS resources |

## ⚙️ Configuration

Edit the `.env` file:

```env
FLASK_APP_PATH=/path/to/your/flask/app
AWS_REGION=us-west-2
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

## 🔧 Claude Desktop Setup

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "flask-mcp-server": {
      "command": "python",
      "args": ["/full/path/to/flask_app_mcp.py"],
      "env": {
        "AWS_REGION": "us-west-2"
      }
    }
  }
}
```

## 📝 License

MIT License