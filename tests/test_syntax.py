#!/usr/bin/env python3
"""
Test to verify the Python syntax of the app module without imports.
"""

import ast
import sys

def check_python_syntax(file_path):
    """Parse Python file to check syntax."""
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def main():
    base = '/home/foo/opencode-sessions/pktamp'
    app_dir = os.path.join(base, 'app')
    
    print("Checking Python syntax...")
    
    files_to_check = [
        'app/__init__.py',
        'app/api.py',
        'app/config.py',
        'app/replay_manager.py',
    ]
    
    all_ok = True
    for rel_path in files_to_check:
        full_path = os.path.join(base, rel_path)
        ok, error = check_python_syntax(full_path)
        if ok:
            print(f"  ✓ {rel_path}")
        else:
            print(f"  ✗ {rel_path}: {error}")
            all_ok = False
    
    return all_ok

if __name__ == '__main__':
    import os
    ok = main()
    print("\n" + "="*50)
    if ok:
        print("✓ All Python files have valid syntax!")
        sys.exit(0)
    else:
        print("✗ Some Python files have syntax errors")
        sys.exit(1)
