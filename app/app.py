import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Pipeline - API Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        gray: {
                            800: '#1e293b',
                            900: '#0f172a',
                        }
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-900 text-gray-100 font-sans antialiased">
    <div class="min-h-screen flex flex-col">
        <!-- Navigation -->
        <nav class="bg-gray-800 border-b border-gray-700 shadow-lg">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex items-center justify-between h-16">
                    <div class="flex items-center">
                        <div class="flex-shrink-0">
                            <i class="fa-solid fa-shield-halved text-blue-500 text-2xl"></i>
                        </div>
                        <div class="ml-3">
                            <span class="text-xl font-bold tracking-tight text-white">Secure Pipeline API</span>
                        </div>
                    </div>
                    <div class="flex items-center space-x-4">
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-900/50 text-green-400 border border-green-700">
                            <i class="fa-solid fa-circle-check mr-2"></i> System Online
                        </span>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <main class="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
            
            <!-- Stats Row -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div class="bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-sm">
                    <div class="flex items-center">
                        <div class="p-3 rounded-full bg-blue-900/50 text-blue-400">
                            <i class="fa-solid fa-server text-xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-gray-400">API Status</p>
                            <p class="text-lg font-semibold text-white">HEALTHY</p>
                        </div>
                    </div>
                </div>
                
                <div class="bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-sm">
                    <div class="flex items-center">
                        <div class="p-3 rounded-full bg-purple-900/50 text-purple-400">
                            <i class="fa-brands fa-docker text-xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-gray-400">Environment</p>
                            <p class="text-lg font-semibold text-white">Docker Container</p>
                        </div>
                    </div>
                </div>

                <div class="bg-gray-800 rounded-xl border border-gray-700 p-6 shadow-sm">
                    <div class="flex items-center">
                        <div class="p-3 rounded-full bg-orange-900/50 text-orange-400">
                            <i class="fa-solid fa-users text-xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm font-medium text-gray-400">Active Users</p>
                            <p class="text-lg font-semibold text-white">2</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- User Table -->
            <div class="bg-gray-800 rounded-xl border border-gray-700 shadow-sm overflow-hidden">
                <div class="px-6 py-5 border-b border-gray-700">
                    <h3 class="text-lg font-medium leading-6 text-white">User Management Directory</h3>
                    <p class="mt-1 text-sm text-gray-400">Real-time data retrieved from the /api/v1/users endpoint.</p>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-700">
                        <thead class="bg-gray-900/50">
                            <tr>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">ID</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">User</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Role</th>
                                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Access Level</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-700 bg-gray-800">
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">1</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center">
                                        <div class="h-8 w-8 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold text-xs">AD</div>
                                        <div class="ml-3">
                                            <p class="text-sm font-medium text-white">Alice Dev</p>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">DevOps Engineer</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-900/50 text-blue-300 border border-blue-700">Admin</span>
                                </td>
                            </tr>
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">2</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center">
                                        <div class="h-8 w-8 rounded-full bg-emerald-600 flex items-center justify-center text-white font-bold text-xs">BS</div>
                                        <div class="ml-3">
                                            <p class="text-sm font-medium text-white">Bob Sec</p>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-300">Security Analyst</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-900/50 text-purple-300 border border-purple-700">Auditor</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </main>
        
        <footer class="bg-gray-800 border-t border-gray-700 mt-auto">
            <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
                <p class="text-center text-sm text-gray-500">Secure Pipeline AWS Project &copy; 2026. Built with Flask, Docker, and Terraform.</p>
            </div>
        </footer>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    """Serves the frontend dashboard landing page."""
    return render_template_string(DASHBOARD_HTML)

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