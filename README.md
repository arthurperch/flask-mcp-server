# Flask MCP server

A small MCP server so an AI assistant can start/stop a Flask app and ask a few AWS questions.

This is a learning project. It is not an enterprise platform.

There is also a Flask dashboard under `aws-cost-optimizer/` that lists AWS resources and estimated spend. Those numbers come from the account it is pointed at. Do not treat the screenshot as a product claim.

## What it can do

| Tool | What it does |
|---|---|
| `start-flask-app` | Start the Flask app |
| `stop-flask-app` | Stop it |
| `check-flask-status` | Is it running? |
| `list-flask-routes` | List Flask routes |
| `test-flask-endpoint` | Hit one endpoint |
| `get-flask-logs` | Show logs |
| `check-aws-resources` | List a few AWS resources |

## Setup

Copy `.env.example` to `.env` and fill in:

```
FLASK_APP_PATH=/path/to/your/flask/app
AWS_REGION=us-west-2
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

Point Claude Desktop (or any MCP client) at `flask_app_mcp.py`:

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

## Layout

```
flask_app_mcp.py          MCP server
start_flask.py            helper
aws-cost-optimizer/       Flask dashboard
```

MIT License
