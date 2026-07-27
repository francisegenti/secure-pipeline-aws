import os
import json
import boto3
from flask import Flask, jsonify, request

app = Flask(__name__)

REGION = os.getenv("AWS_REGION", "us-east-1")

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for container monitoring."""
    return jsonify({"status": "healthy", "service": "user-management-api"}), 200

@app.route("/api/v1/users", methods=["GET"])
def get_users():
    """Sample endpoint returning user data."""
    users = [
        {"id": "1", "name": "Alice Dev", "role": "DevOps Engineer"},
        {"id": "2", "name": "Bob Sec", "role": "Security Analyst"}
    ]
    return jsonify({"success": True, "data": users}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)