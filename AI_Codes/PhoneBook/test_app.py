"""
Phone Book Web App - Comprehensive Test Suite
Tests all features and functionality
"""

import sys
import os
import json
import subprocess
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

print(f"""
{BLUE}╔══════════════════════════════════════════════════════════════╗{END}
{BLUE}║  📱 Phone Book Web App - Comprehensive Test Suite             ║{END}
{BLUE}╚══════════════════════════════════════════════════════════════╝{END}
""")

# Track test results
tests_passed = 0
tests_failed = 0

def test(name, condition, error_msg=""):
    """Helper function to report test results"""
    global tests_passed, tests_failed
    if condition:
        print(f"{GREEN}✓{END} {name}")
        tests_passed += 1
    else:
        print(f"{RED}✗{END} {name}")
        if error_msg:
            print(f"  {RED}Error: {error_msg}{END}")
        tests_failed += 1

print(f"\n{YELLOW}1. CHECKING ENVIRONMENT{END}")
print("=" * 60)

# Test 1: Python version
python_version = sys.version_info
test("Python 3.6+", python_version.major == 3 and python_version.minor >= 6,
     f"Found Python {python_version.major}.{python_version.minor}")

# Test 2: Check required files
print(f"\n{YELLOW}2. CHECKING PROJECT FILES{END}")
print("=" * 60)

files_to_check = [
    'app.py',
    'phonebook.py',
    'contact.py',
    'node.py',
    'templates/index.html',
    'requirements.txt'
]

for file in files_to_check:
    exists = os.path.exists(file)
    test(f"File exists: {file}", exists, f"File not found at {file}")

# Test 3: Check Flask installation
print(f"\n{YELLOW}3. CHECKING FLASK{END}")
print("=" * 60)

try:
    import flask
    test("Flask installed", True, f"Flask {flask.__version__}")
    print(f"  Flask version: {flask.__version__}")
except ImportError:
    test("Flask installed", False, "Flask not found. Run: pip install Flask")

# Test 4: Test Core Logic
print(f"\n{YELLOW}4. TESTING CORE LOGIC (phonebook.py){END}")
print("=" * 60)

try:
    from phonebook import PhoneBook
    from contact import Contact
    
    # Create test phonebook
    pb = PhoneBook()
    test("PhoneBook class loads", True)
    
    # Test adding contact
    success = pb.add_contact("John", "Doe", 1001, "555-1234", "Engineer")
    test("Add contact", success, "Failed to add contact")
    
    # Test contact count
    test("Contact count (1)", pb.get_count() == 1, f"Count is {pb.get_count()}")
    
    # Test search by ID
    node = pb.search_by_id(1001)
    test("Search by ID", node is not None, "Search failed")
    
    # Test search by name
    results = pb.search_by_name("John")
    test("Search by name", len(results) > 0, "Name search failed")
    
    # Test duplicate prevention
    dup_success = pb.add_contact("Jane", "Smith", 1001, "555-5678", "Doctor")
    test("Prevent duplicate ID", not dup_success, "Should reject duplicate ID")
    
    # Test sort
    pb.add_contact("Alice", "Brown", 1002, "555-5678", "Teacher")
    pb.add_contact("Bob", "Green", 1003, "555-9999", "Nurse")
    pb.sort_by_name()
    test("Sort by name", pb.head.contact.name == "Alice", "Sort failed")
    
    # Test delete
    delete_success = pb.delete_contact(1001)
    test("Delete contact", delete_success, "Delete failed")
    test("Contact count after delete (2)", pb.get_count() == 2, f"Count is {pb.get_count()}")
    
    # Test save
    save_success = pb.save_to_file('test_phonebook.json')
    test("Save to JSON", save_success and os.path.exists('test_phonebook.json'))
    
    # Test load
    pb2 = PhoneBook()
    load_success = pb2.load_from_file('test_phonebook.json')
    test("Load from JSON", load_success and pb2.get_count() == 2)
    
    # Cleanup
    if os.path.exists('test_phonebook.json'):
        os.remove('test_phonebook.json')
    
except Exception as e:
    test("Core logic tests", False, str(e))

# Test 5: Test Flask App
print(f"\n{YELLOW}5. TESTING FLASK APP (app.py){END}")
print("=" * 60)

try:
    from app import app
    test("Flask app loads", True)
    
    # Test app configuration
    test("Flask debug mode", hasattr(app, 'debug'))
    
    # Create test client
    with app.test_client() as client:
        # Test homepage
        response = client.get('/')
        test("GET / (homepage)", response.status_code == 200, 
             f"Status code: {response.status_code}")
        
        # Test API - get empty contacts
        response = client.get('/api/contacts')
        test("GET /api/contacts", response.status_code == 200,
             f"Status code: {response.status_code}")
        
        # Test API - add contact
        response = client.post('/api/contacts',
                              json={
                                  'name': 'Test',
                                  'surname': 'User',
                                  'id': 9001,
                                  'phone': '555-0000',
                                  'profession': 'Tester'
                              },
                              content_type='application/json')
        test("POST /api/contacts (add)", response.status_code == 200,
             f"Status code: {response.status_code}")
        
        # Test API - search
        response = client.post('/api/search',
                              json={'type': 'id', 'value': '9001'},
                              content_type='application/json')
        test("POST /api/search", response.status_code == 200,
             f"Status code: {response.status_code}")
        
        # Test API - sort
        response = client.get('/api/sort/name')
        test("GET /api/sort/name", response.status_code == 200,
             f"Status code: {response.status_code}")
        
        # Test API - export CSV
        response = client.get('/api/export/csv')
        test("GET /api/export/csv", response.status_code == 200,
             f"Status code: {response.status_code}")
        
except Exception as e:
    test("Flask app tests", False, str(e))

# Test 6: Test HTML Template
print(f"\n{YELLOW}6. TESTING HTML TEMPLATE{END}")
print("=" * 60)

try:
    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    test("HTML file readable", len(html_content) > 0)
    test("HTML has DOCTYPE", '<!DOCTYPE' in html_content)
    test("HTML has form inputs", '<input' in html_content)
    test("HTML has table element", '<table' in html_content)
    test("HTML has JavaScript", '<script' in html_content)
    test("HTML has CSS styling", '<style' in html_content)
    
    # Check for key UI elements
    test("HTML has 'Add Contact' button", 'Add Contact' in html_content)
    test("HTML has search functionality", 'Search' in html_content)
    test("HTML has sort buttons", 'Sort' in html_content)
    test("HTML has export option", 'Export' in html_content or 'CSV' in html_content)
    
except Exception as e:
    test("HTML template tests", False, str(e))

# Test 7: Test Requirements
print(f"\n{YELLOW}7. CHECKING REQUIREMENTS{END}")
print("=" * 60)

try:
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    test("Requirements file exists", True)
    test("Flask in requirements", 'Flask' in requirements, "Flask not specified")
    
except Exception as e:
    test("Requirements checks", False, str(e))

# Test 8: Test Run Script
print(f"\n{YELLOW}8. CHECKING RUN SCRIPT{END}")
print("=" * 60)

try:
    with open('run.sh', 'r') as f:
        script_content = f.read()
    
    test("Run script exists", True)
    test("Run script is executable", os.access('run.sh', os.X_OK))
    test("Run script has Flask check", 'Flask' in script_content)
    test("Run script launches app", 'app.py' in script_content)
    
except Exception as e:
    test("Run script checks", False, str(e))

# Test 9: Test Data Persistence
print(f"\n{YELLOW}9. TESTING DATA PERSISTENCE{END}")
print("=" * 60)

try:
    # Create test data
    pb_test = PhoneBook()
    pb_test.add_contact("Persist", "Test", 9999, "555-1111", "Tester")
    pb_test.save_to_file('test_persist.json')
    
    # Load and verify
    pb_verify = PhoneBook()
    pb_verify.load_from_file('test_persist.json')
    
    test("Data persists after save/load", pb_verify.get_count() == 1)
    
    node = pb_verify.search_by_id(9999)
    test("Saved contact retrievable", node is not None)
    test("Contact data intact", 
         node.contact.name == "Persist" and node.contact.phone == "555-1111")
    
    # Cleanup
    if os.path.exists('test_persist.json'):
        os.remove('test_persist.json')
    
except Exception as e:
    test("Data persistence tests", False, str(e))

# Test 10: Test API Error Handling
print(f"\n{YELLOW}10. TESTING ERROR HANDLING{END}")
print("=" * 60)

try:
    with app.test_client() as client:
        # Test missing fields
        response = client.post('/api/contacts',
                              json={'name': 'Test'},
                              content_type='application/json')
        test("Reject incomplete contact data", response.status_code == 400,
             f"Status code: {response.status_code}")
        
        # Test invalid ID format
        response = client.post('/api/search',
                              json={'type': 'id', 'value': 'not_a_number'},
                              content_type='application/json')
        test("Handle invalid ID format", response.status_code == 400,
             f"Status code: {response.status_code}")
        
        # Test invalid sort option
        response = client.get('/api/sort/invalid_sort')
        test("Reject invalid sort option", response.status_code == 400,
             f"Status code: {response.status_code}")
        
except Exception as e:
    test("Error handling tests", False, str(e))

# Final Summary
print(f"\n{BLUE}═════════════════════════════════════════════════════════════{END}")
print(f"\n{YELLOW}TEST RESULTS SUMMARY{END}")
print(f"{BLUE}═════════════════════════════════════════════════════════════{END}\n")

total_tests = tests_passed + tests_failed
pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0

print(f"Total Tests:    {total_tests}")
print(f"Passed:         {GREEN}{tests_passed}{END}")
print(f"Failed:         {RED}{tests_failed}{END}")
print(f"Pass Rate:      {pass_rate:.1f}%")

if tests_failed == 0:
    print(f"\n{GREEN}✓ ALL TESTS PASSED! 🎉{END}")
    print(f"\n{YELLOW}Your Phone Book Web App is fully functional!{END}")
    print(f"\n{BLUE}Next step: Run the app{END}")
    print(f"{BLUE}  python app.py{END}\n")
    sys.exit(0)
else:
    print(f"\n{RED}✗ Some tests failed. Please fix issues above.{END}\n")
    sys.exit(1)
