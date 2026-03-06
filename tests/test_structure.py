#!/usr/bin/env python3
"""
Test to verify Flask app structure without Flask installed.
"""

import os
import sys

def test_structure():
    """Test that all required files exist and have basic content."""
    
    base = '/home/foo/opencode-sessions/pktamp'
    
    required_files = [
        'app/__init__.py',
        'app/api.py',
        'app/config.py',
        'app/replay_manager.py',
        'requirements.txt',
        'install.sh',
        'templates/index.html',
        'static/css/winamp.css',
        'static/js/app.js',
        'pktamp.service',
        'README.md',
        'INSTALL.md',
        'pktamp.8',
        '.github/workflows/ci.yml',
    ]
    
    print("Verifying project structure...")
    all_ok = True
    
    for rel_path in required_files:
        full_path = os.path.join(base, rel_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"  ✓ {rel_path} ({size} bytes)")
        else:
            print(f"  ✗ {rel_path} MISSING")
            all_ok = False
    
    # Check directory structure
    print("\nChecking directories...")
    required_dirs = [
        'app',
        'templates',
        'static/css',
        'static/js',
        'tests',
        'tests/e2e',
    ]
    
    for rel_dir in required_dirs:
        full_dir = os.path.join(base, rel_dir)
        if os.path.isdir(full_dir):
            print(f"  ✓ {rel_dir}/")
        else:
            print(f"  ✗ {rel_dir}/ MISSING")
            all_ok = False
    
    return all_ok

if __name__ == '__main__':
    ok = test_structure()
    print("\n" + "="*50)
    if ok:
        print("✓ Project structure looks good!")
        sys.exit(0)
    else:
        print("✗ Some files/directories are missing")
        sys.exit(1)
