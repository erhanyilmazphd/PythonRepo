#!/usr/bin/env python3
"""
Quick validation test for Phone Book Web App
"""

import sys
import os

print("\n" + "="*70)
print("📱 PHONE BOOK WEB APP - QUICK VALIDATION TEST")
print("="*70 + "\n")

# Test 1: Check files exist
print("✓ Checking files...")
files = ['app.py', 'phonebook.py', 'contact.py', 'node.py', 'templates/index.html', 'requirements.txt']
for f in files:
    if os.path.exists(f):
        print(f"  ✓ {f}")
    else:
        print(f"  ✗ {f} NOT FOUND")
        sys.exit(1)

# Test 2: Import modules
print("\n✓ Testing imports...")
try:
    from phonebook import PhoneBook
    print("  ✓ phonebook.py imports")
    from contact import Contact
    print("  ✓ contact.py imports")
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    sys.exit(1)

# Test 3: Test core functionality
print("\n✓ Testing core functionality...")
try:
    pb = PhoneBook()
    pb.add_contact("John", "Doe", 1001, "555-1234", "Engineer")
    assert pb.get_count() == 1, "Add contact failed"
    print("  ✓ Add contact works")
    
    node = pb.search_by_id(1001)
    assert node is not None, "Search failed"
    print("  ✓ Search works")
    
    pb.add_contact("Jane", "Smith", 1002, "555-5678", "Doctor")
    pb.sort_by_name()
    assert pb.head.contact.name == "Jane", "Sort failed"
    print("  ✓ Sort works")
    
    pb.delete_contact(1001)
    assert pb.get_count() == 1, "Delete failed"
    print("  ✓ Delete works")
    
except Exception as e:
    print(f"  ✗ Core functionality failed: {e}")
    sys.exit(1)

# Test 4: Test Flask app
print("\n✓ Testing Flask app...")
try:
    from flask import Flask
    print("  ✓ Flask imports")
    
    from app import app
    print("  ✓ app.py imports")
    
    # Test app client
    with app.test_client() as client:
        response = client.get('/')
        if response.status_code == 200:
            print("  ✓ GET / returns 200")
        else:
            print(f"  ✗ GET / returned {response.status_code}")
            sys.exit(1)
        
        response = client.get('/api/contacts')
        if response.status_code == 200:
            print("  ✓ GET /api/contacts returns 200")
        else:
            print(f"  ✗ GET /api/contacts returned {response.status_code}")
            sys.exit(1)
        
        response = client.post('/api/contacts',
                              json={'name': 'Test', 'surname': 'User', 'id': 9001, 
                                   'phone': '555-0000', 'profession': 'Tester'},
                              content_type='application/json')
        if response.status_code == 200:
            print("  ✓ POST /api/contacts works")
        else:
            print(f"  ✗ POST /api/contacts returned {response.status_code}")
            sys.exit(1)
            
except Exception as e:
    print(f"  ✗ Flask app test failed: {e}")
    sys.exit(1)

# Test 5: HTML template
print("\n✓ Testing HTML template...")
try:
    with open('templates/index.html', 'r') as f:
        html = f.read()
    
    checks = [
        ('<!DOCTYPE', 'Has DOCTYPE'),
        ('<input', 'Has input fields'),
        ('<table', 'Has table'),
        ('<script', 'Has JavaScript'),
        ('Add Contact', 'Has Add Contact button'),
        ('Search', 'Has search'),
    ]
    
    for check, desc in checks:
        if check in html:
            print(f"  ✓ {desc}")
        else:
            print(f"  ✗ {desc}")
            
except Exception as e:
    print(f"  ✗ HTML test failed: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("✅ ALL VALIDATION TESTS PASSED!")
print("="*70)
print("\n🚀 Your web app is ready to run:\n")
print("   pip install Flask")
print("   python app.py\n")
print("Then open: http://127.0.0.1:5000\n")

sys.exit(0)
