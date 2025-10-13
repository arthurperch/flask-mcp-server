# Flask MCP Server with AWS Cost Optimizer

## Executive Summary

Enterprise Flask application suite featuring Model Context Protocol (MCP) server integration and a comprehensive AWS cost optimization platform. Designed for production environments with scalable architecture and business-grade reporting capabilities.

![AWS Cost Optimizer Dashboard](./aws-cost-optimizer/aws-dashboard-screenshot.png)
*Production dashboard showing real-time cost analysis with $147/month tracking and $45 potential savings identification*

## Repository Structure

```
flask-mcp-server/
├── aws-cost-optimizer/          # Primary AWS cost optimization platform
│   ├── app.py                   # Flask web application
│   ├── templates/               # Web dashboard UI
│   ├── static/                  # CSS, JavaScript assets
│   ├── services/                # AWS integration services
│   ├── routes/                  # REST API endpoints  
│   └── mcp/                     # Claude Desktop integration
│
├── flask_app_mcp.py            # Original MCP server implementation
├── start_flask.py              # MCP server utilities
├── test_mcp_server.py          # Testing framework
└── requirements.txt            # Python dependencies
```

## Primary Project: AWS Cost Optimizer

### Business Impact

**Cost Reduction Achieved**: $45/month savings identified (30.6% reduction)
**Resources Monitored**: 6 AWS resources across EC2, S3, EBS services  
**Account Integration**: Live connection to AWS account 611377760416
**Monthly Cost Tracking**: $147.00 with real-time analysis

### Enterprise Features
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