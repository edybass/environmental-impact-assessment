#!/usr/bin/env python3
"""
EIA Pro Platform - Comprehensive Backend Launcher
Launches the full professional environmental assessment platform

Created by: Edy Bassil
Email: bassileddy@gmail.com
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_requirements():
    """Check if all required modules are available"""
    print("🔍 Checking system requirements...")
    
    required_modules = [
        'flask',
        'flask_cors'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - installed")
        except ImportError:
            print(f"❌ {module} - missing")
            missing.append(module)
    
    if missing:
        print("\n⚠️  Missing required packages!")
        print("Please install them using:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True

def check_assessment_modules():
    """Check if all assessment modules are present"""
    print("\n📋 Checking assessment modules...")
    
    module_files = [
        'src/assessment/waste_management.py',
        'src/assessment/water_resources.py',
        'src/assessment/biological_environment.py',
        'src/assessment/comprehensive_risk_assessment.py',
        'src/assessment/socio_economic_environment.py',
        'src/assessment/soil_geology.py',
        'src/assessment/environmental_management_plan.py'
    ]
    
    all_present = True
    for module_file in module_files:
        if Path(module_file).exists():
            print(f"✅ {module_file}")
        else:
            print(f"❌ {module_file} - MISSING")
            all_present = False
    
    return all_present

def main():
    """Main launcher function"""
    print("="*80)
    print("🌿 EIA Pro Platform - Comprehensive Environmental Assessment")
    print("="*80)
    print("Professional EIA platform with 9 integrated assessment modules")
    print("Created by: Edy Bassil (bassileddy@gmail.com)")
    print("="*80)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Cannot start: Missing requirements")
        sys.exit(1)
    
    # Check assessment modules
    if not check_assessment_modules():
        print("\n⚠️  Warning: Some assessment modules are missing")
        print("The platform may not function properly")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print("\n🚀 Starting comprehensive backend server...")
    print("="*80)
    
    # Launch the comprehensive backend
    try:
        subprocess.run([
            sys.executable,
            'backend_comprehensive.py'
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()