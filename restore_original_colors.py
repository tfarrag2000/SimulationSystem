#!/usr/bin/env python3
"""
Color Scheme Rollback Script
Run this script to restore original dashboard colors if you don't like the new colorful theme.
"""

import re

def rollback_colors():
    """Restore original dashboard colors"""
    
    # Read the current app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rollback changes - replace enhanced colors with originals
    rollback_patterns = [
        # Header colors
        (r'color="success"', 'color="primary"'),
        (r'className="bg-gradient-primary"', 'className="bg-primary"'),
        
        # Card colors
        (r'color="info"', 'color="light"'),
        (r'color="warning"', 'color="light"'),
        (r'color="success"', 'color="light"'),
        (r'color="danger"', 'color="light"'),
        
        # Button colors
        (r'color="success"', 'color="primary"'),
        (r'color="warning"', 'color="primary"'),
        (r'color="info"', 'color="primary"'),
        
        # Text colors
        (r'text-success', 'text-primary'),
        (r'text-warning', 'text-muted'),
        (r'text-info', 'text-muted'),
        (r'text-danger', 'text-muted'),
        
        # Badge colors
        (r'bg-success', 'bg-primary'),
        (r'bg-warning', 'bg-primary'),
        (r'bg-info', 'bg-primary'),
        (r'bg-danger', 'bg-primary'),
    ]
    
    # Apply rollback patterns
    for pattern, replacement in rollback_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Write back to app.py
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Color scheme rolled back to original!")
    print("💡 Restart your app to see the changes.")

if __name__ == "__main__":
    try:
        rollback_colors()
    except Exception as e:
        print(f"❌ Error during rollback: {e}")
        print("💡 You may need to manually restore colors from the backup.")
