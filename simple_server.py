#!/usr/bin/env python3
"""
EIA Pro Platform - Simple HTTP Server
Serves your existing docs/index.html with basic backend simulation

Created by: Edy Bassil
Email: bassileddy@gmail.com
"""

import http.server
import socketserver
import json
import urllib.parse
import os
from datetime import datetime
from pathlib import Path

class EIAHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            # Serve the main docs/index.html file
            docs_path = Path('docs/index.html')
            if docs_path.exists():
                self.path = '/docs/index.html'
                return super().do_GET()
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html = """
                <h1>🌿 EIA Pro Platform - Simple Server Running!</h1>
                <p>Your docs/index.html file will be served here once available.</p>
                <p>Current working directory: {}</p>
                <p>Files found: {}</p>
                <p><a href="/health">Check server health</a></p>
                """.format(os.getcwd(), ', '.join(os.listdir('.')))
                self.wfile.write(html.encode())
                return
        
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            health_data = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'server_type': 'Simple Python Server',
                'docs_available': Path('docs/index.html').exists(),
                'working_directory': str(Path.cwd())
            }
            self.wfile.write(json.dumps(health_data).encode())
            return
            
        elif self.path.startswith('/api/platform-stats'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            stats = {
                'version_current': '1.0',
                'version_next': '5.0',
                'reports_generated': 527,
                'money_saved': 2500000,
                'time_saved_percent': 75,
                'countries_active': 12,
                'beta_applications': 342,
                'advanced_modules': {
                    'air_modeling': True,
                    'noise_modeling': True,
                    'gis_analysis': True,
                    'stakeholder_management': True,
                    'baseline_collection': True
                }
            }
            self.wfile.write(json.dumps(stats).encode())
            return
        
        # Default file serving
        return super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path.startswith('/api/assess-project'):
            # Simulate project assessment
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                # Simulate assessment results
                results = {
                    'project_id': f"PROJ_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'status': 'success',
                    'basic_impacts': {
                        'air_quality_score': 7.5,
                        'noise_score': 6.8,
                        'water_score': 8.2,
                        'overall_risk': 'Medium'
                    },
                    'advanced_results': {
                        'air_modeling': {
                            'sources_identified': 5,
                            'status': 'completed',
                            'module': 'Gaussian Air Dispersion Model'
                        },
                        'noise_modeling': {
                            'sources_identified': 8,
                            'status': 'completed',
                            'module': 'ISO 9613-2 Noise Propagation'
                        },
                        'gis_analysis': {
                            'receptors_found': 12,
                            'status': 'completed',
                            'module': 'Automated GIS Engine'
                        }
                    },
                    'processing_time': '2.3 seconds'
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(results).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {'status': 'error', 'message': str(e)}
                self.wfile.write(json.dumps(error_response).encode())
                
        elif self.path.startswith('/api/generate-report'):
            # Simulate report generation
            report_data = {
                'report_id': f"RPT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'status': 'generated',
                'pages': 127,
                'sections': [
                    'Executive Summary',
                    'Project Description',
                    'Environmental Baseline',
                    'Impact Assessment',
                    'Mitigation Measures',
                    'Monitoring Plan',
                    'Conclusion'
                ],
                'generation_time': '45 seconds'
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(report_data).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    PORT = 5000
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    print("\n" + "="*80)
    print("🌿 EIA Pro Platform - Simple Server")
    print("="*80)
    print(f"📍 Server running at: http://localhost:{PORT}")
    print("📧 Created by: Edy Bassil (bassileddy@gmail.com)")
    print(f"🌐 Serving files from: {Path.cwd()}")
    print(f"📄 Main page: {'✅ docs/index.html found' if Path('docs/index.html').exists() else '❌ docs/index.html not found'}")
    print("="*80)
    print("🎯 Available endpoints:")
    print("   • GET  / - Main application")
    print("   • POST /api/assess-project - Run assessment")
    print("   • POST /api/generate-report - Generate report")
    print("   • GET  /api/platform-stats - Platform stats")
    print("   • GET  /health - Health check")
    print("="*80 + "\n")
    print("Press Ctrl+C to stop the server\n")
    
    with socketserver.TCPServer(("", PORT), EIAHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped by user")
            httpd.shutdown()

if __name__ == "__main__":
    main()