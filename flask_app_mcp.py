#!/usr/bin/env python3
"""Flask App MCP Server

Tools so an AI assistant can start/stop a Flask app and ask a few AWS questions.
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from pydantic import AnyUrl
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("flask-app-mcp")

server = Server("flask-app-mcp")

# Flask app configuration
FLASK_APP_PATH = os.getenv('FLASK_APP_PATH', '../Cloud-Infrastructure-Flask-App/app')
FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = os.getenv('FLASK_PORT', '5000')

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available Flask and AWS tools"""
    return [
        Tool(
            name="start-flask-app",
            description="Start the Flask application server",
            inputSchema={
                "type": "object",
                "properties": {
                    "port": {
                        "type": "integer",
                        "description": "Port to run the Flask app on (default: 5000)",
                        "default": 5000
                    },
                    "host": {
                        "type": "string",
                        "description": "Host to bind the Flask app to (default: 127.0.0.1)",
                        "default": "127.0.0.1"
                    },
                    "debug": {
                        "type": "boolean",
                        "description": "Run Flask in debug mode",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="stop-flask-app",
            description="Stop the Flask application server",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="check-flask-status",
            description="Check if the Flask application is running",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get-flask-logs",
            description="Get recent Flask application logs",
            inputSchema={
                "type": "object",
                "properties": {
                    "lines": {
                        "type": "integer",
                        "description": "Number of log lines to retrieve (default: 50)",
                        "default": 50
                    }
                }
            }
        ),
        Tool(
            name="list-flask-routes",
            description="List all available Flask routes",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="test-flask-endpoint",
            description="Test a specific Flask endpoint",
            inputSchema={
                "type": "object",
                "properties": {
                    "endpoint": {
                        "type": "string",
                        "description": "The endpoint to test (e.g., '/api/health')",
                        "default": "/"
                    },
                    "method": {
                        "type": "string",
                        "description": "HTTP method to use",
                        "enum": ["GET", "POST", "PUT", "DELETE"],
                        "default": "GET"
                    }
                }
            }
        ),
        Tool(
            name="deploy-to-aws",
            description="Deploy Flask app to AWS (requires AWS credentials)",
            inputSchema={
                "type": "object",
                "properties": {
                    "environment": {
                        "type": "string",
                        "description": "Deployment environment",
                        "enum": ["dev", "staging", "prod"],
                        "default": "dev"
                    }
                }
            }
        ),
        Tool(
            name="check-aws-resources",
            description="Check AWS resources related to the Flask app",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls for Flask and AWS operations"""
    
    try:
        if name == "start-flask-app":
            return await start_flask_app(arguments)
        elif name == "stop-flask-app":
            return await stop_flask_app(arguments)
        elif name == "check-flask-status":
            return await check_flask_status(arguments)
        elif name == "get-flask-logs":
            return await get_flask_logs(arguments)
        elif name == "list-flask-routes":
            return await list_flask_routes(arguments)
        elif name == "test-flask-endpoint":
            return await test_flask_endpoint(arguments)
        elif name == "deploy-to-aws":
            return await deploy_to_aws(arguments)
        elif name == "check-aws-resources":
            return await check_aws_resources(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"❌ Unknown tool: {name}"
            )]
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(
            type="text",
            text=f"❌ Error executing {name}: {str(e)}"
        )]

async def start_flask_app(arguments: Dict[str, Any]) -> List[TextContent]:
    """Start the Flask application"""
    try:
        port = arguments.get('port', 5000)
        host = arguments.get('host', '127.0.0.1')
        debug = arguments.get('debug', False)
        
        flask_app_path = Path(FLASK_APP_PATH)
        if not flask_app_path.exists():
            return [TextContent(
                type="text",
                text=f"❌ Flask app path not found: {flask_app_path}"
            )]
        
        # Check if Flask app is already running
        status_result = await check_flask_status({})
        if "running" in status_result[0].text.lower():
            return [TextContent(
                type="text",
                text="⚠️ Flask app is already running. Use stop-flask-app first."
            )]
        
        # Start Flask app
        cmd = [
            sys.executable, "-m", "flask", "run",
            "--host", str(host),
            "--port", str(port)
        ]
        
        if debug:
            cmd.extend(["--debug"])
        
        env = os.environ.copy()
        env['FLASK_APP'] = str(flask_app_path / 'app.py')
        
        # Start the process in the background
        process = subprocess.Popen(
            cmd,
            cwd=flask_app_path,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Store process ID for later reference
        with open('.flask_pid', 'w') as f:
            f.write(str(process.pid))
        
        return [TextContent(
            type="text",
            text=f"🚀 Starting Flask app on {host}:{port}\n"
                 f"Debug mode: {debug}\n"
                 f"Process ID: {process.pid}\n"
                 f"App path: {flask_app_path}"
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error starting Flask app: {str(e)}"
        )]

async def stop_flask_app(arguments: Dict[str, Any]) -> List[TextContent]:
    """Stop the Flask application"""
    try:
        pid_file = Path('.flask_pid')
        if not pid_file.exists():
            return [TextContent(
                type="text",
                text="❌ No Flask process ID found. App may not be running."
            )]
        
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        # Try to terminate the process
        try:
            import psutil
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=10)
            pid_file.unlink()
            
            return [TextContent(
                type="text",
                text=f"✅ Flask app stopped successfully (PID: {pid})"
            )]
        except ImportError:
            # Fallback for systems without psutil
            import signal
            os.kill(pid, signal.SIGTERM)
            pid_file.unlink()
            
            return [TextContent(
                type="text",
                text=f"✅ Flask app stop signal sent (PID: {pid})"
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error stopping Flask app: {str(e)}"
        )]

async def check_flask_status(arguments: Dict[str, Any]) -> List[TextContent]:
    """Check Flask application status"""
    try:
        import requests
        
        url = f"http://{FLASK_HOST}:{FLASK_PORT}"
        
        try:
            response = requests.get(url, timeout=5)
            status = "🟢 Running" if response.status_code == 200 else f"🟡 Running (Status: {response.status_code})"
        except requests.exceptions.ConnectionError:
            status = "🔴 Not running"
        except requests.exceptions.Timeout:
            status = "🟡 Running but slow to respond"
        
        # Check process
        pid_file = Path('.flask_pid')
        process_info = ""
        if pid_file.exists():
            with open(pid_file, 'r') as f:
                pid = f.read().strip()
            try:
                import psutil
                process = psutil.Process(int(pid))
                if process.is_running():
                    process_info = f"\nProcess ID: {pid} (Running)"
                else:
                    process_info = f"\nProcess ID: {pid} (Not running)"
            except (ImportError, Exception):
                process_info = f"\nProcess ID: {pid} (Status unknown)"
        
        return [TextContent(
            type="text",
            text=f"Flask App Status: {status}\nURL: {url}{process_info}"
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error checking Flask status: {str(e)}"
        )]

async def get_flask_logs(arguments: Dict[str, Any]) -> List[TextContent]:
    """Get Flask application logs"""
    try:
        lines = arguments.get('lines', 50)
        
        # This is a placeholder - in a real implementation, you'd read from actual log files
        log_content = f"📋 Flask App Logs (last {lines} lines):\n\n"
        log_content += "=== Recent Activity ===\n"
        log_content += "[INFO] Flask app starting...\n"
        log_content += "[INFO] Routes registered successfully\n"
        log_content += "[INFO] Database connection established\n"
        log_content += "[DEBUG] Processing request...\n"
        log_content += "\n💡 Note: Configure proper logging to see real-time logs"
        
        return [TextContent(
            type="text",
            text=log_content
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error getting Flask logs: {str(e)}"
        )]

async def list_flask_routes(arguments: Dict[str, Any]) -> List[TextContent]:
    """List Flask application routes"""
    try:
        flask_app_path = Path(FLASK_APP_PATH)
        app_file = flask_app_path / 'app.py'
        
        if not app_file.exists():
            return [TextContent(
                type="text",
                text=f"❌ Flask app file not found: {app_file}"
            )]
        
        # Read the app.py file to extract routes
        with open(app_file, 'r') as f:
            content = f.read()
        
        # Simple route extraction (this could be made more sophisticated)
        routes = []
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '@app.route(' in line:
                route_line = line.strip()
                # Try to get the function name from the next few lines
                func_name = "Unknown"
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].startswith('def '):
                        func_name = lines[j].split('def ')[1].split('(')[0]
                        break
                routes.append(f"• {route_line} → {func_name}()")
        
        if not routes:
            routes = ["No routes found in app.py"]
        
        result = "🛣️ **Flask Routes:**\n\n" + "\n".join(routes)
        
        return [TextContent(
            type="text",
            text=result
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error listing Flask routes: {str(e)}"
        )]

async def test_flask_endpoint(arguments: Dict[str, Any]) -> List[TextContent]:
    """Test a Flask endpoint"""
    try:
        import requests
        
        endpoint = arguments.get('endpoint', '/')
        method = arguments.get('method', 'GET').upper()
        
        url = f"http://{FLASK_HOST}:{FLASK_PORT}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, timeout=10)
            elif method == 'POST':
                response = requests.post(url, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, timeout=10)
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ Unsupported HTTP method: {method}"
                )]
            
            result = f"🧪 **Endpoint Test Results**\n\n"
            result += f"URL: {url}\n"
            result += f"Method: {method}\n"
            result += f"Status Code: {response.status_code}\n"
            result += f"Response Time: {response.elapsed.total_seconds():.3f}s\n"
            result += f"Content Length: {len(response.content)} bytes\n\n"
            
            if response.status_code == 200:
                result += "✅ Request successful\n"
            elif 400 <= response.status_code < 500:
                result += "⚠️ Client error\n"
            elif response.status_code >= 500:
                result += "❌ Server error\n"
            
            # Show first 500 chars of response
            content = response.text[:500]
            if len(response.text) > 500:
                content += "... (truncated)"
            
            result += f"\n**Response Preview:**\n```\n{content}\n```"
            
            return [TextContent(
                type="text",
                text=result
            )]
        
        except requests.exceptions.ConnectionError:
            return [TextContent(
                type="text",
                text=f"❌ Could not connect to {url}. Is the Flask app running?"
            )]
        except requests.exceptions.Timeout:
            return [TextContent(
                type="text",
                text=f"⏱️ Request to {url} timed out"
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error testing endpoint: {str(e)}"
        )]

async def deploy_to_aws(arguments: Dict[str, Any]) -> List[TextContent]:
    """Deploy Flask app to AWS"""
    try:
        environment = arguments.get('environment', 'dev')
        
        # This is a placeholder for AWS deployment logic
        result = f"🚀 **AWS Deployment ({environment})**\n\n"
        result += "Deployment steps:\n"
        result += "1. ✅ Validating AWS credentials\n"
        result += "2. ✅ Building application package\n"
        result += "3. 🔄 Uploading to S3...\n"
        result += "4. 🔄 Updating Elastic Beanstalk environment...\n"
        result += "5. ⏳ Waiting for deployment to complete...\n\n"
        result += "💡 Note: This is a simulation. Implement actual deployment logic."
        
        return [TextContent(
            type="text",
            text=result
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error deploying to AWS: {str(e)}"
        )]

async def check_aws_resources(arguments: Dict[str, Any]) -> List[TextContent]:
    """Check AWS resources related to the Flask app"""
    try:
        # Initialize AWS session
        try:
            session = boto3.Session()
            ec2 = session.client('ec2')
            
            # Check EC2 instances
            response = ec2.describe_instances()
            instance_count = sum(len(r['Instances']) for r in response['Reservations'])
            
            result = "☁️ **AWS Resources Overview**\n\n"
            result += f"EC2 Instances: {instance_count}\n"
            result += "S3 Buckets: [Check in progress...]\n"
            result += "Load Balancers: [Check in progress...]\n"
            result += "RDS Instances: [Check in progress...]\n\n"
            result += "💡 Full AWS integration requires proper credentials and permissions."
            
        except NoCredentialsError:
            result = "❌ **AWS Credentials Not Found**\n\n"
            result += "Please configure AWS credentials:\n"
            result += "1. Use `aws configure`\n"
            result += "2. Set environment variables\n"
            result += "3. Use IAM roles (if on EC2)\n"
        
        return [TextContent(
            type="text",
            text=result
        )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ Error checking AWS resources: {str(e)}"
        )]

async def main():
    """Main entry point for the MCP server"""
    # Import here to avoid issues with event loop
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting Flask App MCP Server")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="flask-app-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())