#!/usr/bin/env python3
"""
Simple test script for the Flask MCP Server
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import mcp
        print("✅ MCP imported successfully")
        
        import boto3
        print("✅ Boto3 imported successfully")
        
        import requests
        print("✅ Requests imported successfully")
        
        import psutil
        print("✅ Psutil imported successfully")
        
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_env_file():
    """Test that .env file exists and can be loaded"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        flask_app_path = os.getenv('FLASK_APP_PATH')
        aws_region = os.getenv('AWS_REGION')
        
        print(f"✅ .env file loaded successfully")
        print(f"   FLASK_APP_PATH: {flask_app_path}")
        print(f"   AWS_REGION: {aws_region}")
        
        return True
    except Exception as e:
        print(f"❌ .env file error: {e}")
        return False

def test_flask_app_path():
    """Test that Flask app path exists"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        flask_app_path = os.getenv('FLASK_APP_PATH')
        if flask_app_path and os.path.exists(flask_app_path):
            print(f"✅ Flask app path exists: {flask_app_path}")
            
            # Check if app.py exists
            app_py = os.path.join(flask_app_path, 'app.py')
            if os.path.exists(app_py):
                print(f"✅ Flask app.py found: {app_py}")
            else:
                print(f"⚠️  Flask app.py not found at: {app_py}")
            
            return True
        else:
            print(f"❌ Flask app path does not exist: {flask_app_path}")
            return False
    except Exception as e:
        print(f"❌ Flask app path error: {e}")
        return False

def test_mcp_server_structure():
    """Test that MCP server file has correct structure"""
    try:
        # Import the MCP server module
        import flask_app_mcp
        
        print("✅ MCP server module imported successfully")
        
        # Check if server object exists
        if hasattr(flask_app_mcp, 'server'):
            print("✅ MCP server object found")
        else:
            print("❌ MCP server object not found")
            return False
        
        return True
    except Exception as e:
        print(f"❌ MCP server structure error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Flask MCP Server Setup\n")
    
    tests = [
        ("Package Imports", test_imports),
        ("Environment File", test_env_file),
        ("Flask App Path", test_flask_app_path),
        ("MCP Server Structure", test_mcp_server_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}:")
        print("-" * 40)
        result = test_func()
        results.append((test_name, result))
    
    print("\n🏁 Test Results Summary:")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! MCP server is ready to use.")
        print("\nNext steps:")
        print("1. Configure Claude Desktop with the MCP server")
        print("2. Test the server with Claude")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before proceeding.")

if __name__ == "__main__":
    main()