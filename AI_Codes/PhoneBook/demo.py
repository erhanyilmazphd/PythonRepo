"""
Demo script to test PhoneBook functionality without interactive menu
This script demonstrates all features of the Phone Book system
"""

from phonebook import PhoneBook
from contact import Contact

def demo():
    """Run demonstration of phone book features"""
    
    print("="*60)
    print("PHONE BOOK SYSTEM DEMONSTRATION")
    print("="*60)
    
    # Create a new phone book
    pb = PhoneBook()
    
    # Demo 1: Add Contacts
    print("\n1. ADDING CONTACTS")
    print("-" * 60)
    
    contacts_data = [
        ("Alice", "Johnson", 1001, "555-1111", "Software Engineer"),
        ("Bob", "Smith", 1002, "555-2222", "Doctor"),
        ("Charlie", "Brown", 1003, "555-3333", "Teacher"),
        ("Diana", "Davis", 1004, "555-4444", "Lawyer"),
        ("Eve", "Wilson", 1005, "555-5555", "Nurse"),
    ]
    
    for name, surname, contact_id, phone, profession in contacts_data:
        success = pb.add_contact(name, surname, contact_id, phone, profession)
        if success:
            print(f"✓ Added: {name} {surname}")
    
    # Demo 2: List All
    print("\n2. LIST ALL CONTACTS")
    print("-" * 60)
    pb.list_contacts()
    
    # Demo 3: Search Operations
    print("3. SEARCH OPERATIONS")
    print("-" * 60)
    
    # Search by ID
    print("\nSearching by ID (1003):")
    node = pb.search_by_id(1003)
    if node:
        print(f"Found: {node.contact}")
    
    # Search by Name
    print("\nSearching by Name ('Alice'):")
    results = pb.search_by_name("Alice")
    for node in results:
        print(f"Found: {node.contact}")
    
    # Search by Surname
    print("\nSearching by Surname ('Davis'):")
    results = pb.search_by_surname("Davis")
    for node in results:
        print(f"Found: {node.contact}")
    
    # Search by Phone
    print("\nSearching by Phone ('555-4444'):")
    node = pb.search_by_phone("555-4444")
    if node:
        print(f"Found: {node.contact}")
    
    # Demo 4: Sorting
    print("\n4. SORTING OPERATIONS")
    print("-" * 60)
    
    print("\nSorted by NAME:")
    pb_copy = PhoneBook()
    for name, surname, contact_id, phone, profession in contacts_data:
        pb_copy.add_contact(name, surname, contact_id, phone, profession)
    pb_copy.sort_by_name()
    pb_copy.list_contacts()
    
    print("\nSorted by SURNAME:")
    pb_copy2 = PhoneBook()
    for name, surname, contact_id, phone, profession in contacts_data:
        pb_copy2.add_contact(name, surname, contact_id, phone, profession)
    pb_copy2.sort_by_surname()
    pb_copy2.list_contacts()
    
    print("\nSorted by ID:")
    pb_copy3 = PhoneBook()
    for name, surname, contact_id, phone, profession in contacts_data:
        pb_copy3.add_contact(name, surname, contact_id, phone, profession)
    pb_copy3.sort_by_id()
    pb_copy3.list_contacts()
    
    print("\nSorted by PROFESSION:")
    pb_copy4 = PhoneBook()
    for name, surname, contact_id, phone, profession in contacts_data:
        pb_copy4.add_contact(name, surname, contact_id, phone, profession)
    pb_copy4.sort_by_profession()
    pb_copy4.list_contacts()
    
    # Demo 5: Insert
    print("5. INSERT CONTACT")
    print("-" * 60)
    print("\nInserting 'Frank Green' (ID: 2001) at position 2:")
    pb.insert_contact(2, "Frank", "Green", 2001, "555-6666", "Architect")
    pb.list_contacts()
    
    # Demo 6: Update
    print("6. UPDATE CONTACT")
    print("-" * 60)
    print("\nUpdating contact ID 1005 - change phone and profession:")
    pb.update_contact(1005, phone="555-9999", profession="Senior Nurse")
    node = pb.search_by_id(1005)
    if node:
        print(f"Updated: {node.contact}")
    
    # Demo 7: Delete
    print("\n7. DELETE CONTACT")
    print("-" * 60)
    print(f"\nCurrent count: {pb.get_count()} contacts")
    print("Deleting contact ID 1002...")
    pb.delete_contact(1002)
    print(f"After deletion: {pb.get_count()} contacts")
    pb.list_contacts()
    
    # Demo 8: Save to File
    print("8. SAVE TO FILE")
    print("-" * 60)
    pb.save_to_file('demo_phonebook.json')
    
    # Demo 9: Load from File
    print("\n9. LOAD FROM FILE")
    print("-" * 60)
    pb_loaded = PhoneBook()
    pb_loaded.load_from_file('demo_phonebook.json')
    print("Contents after loading:")
    pb_loaded.list_contacts()
    
    # Demo 10: Duplicate ID Check
    print("10. DUPLICATE ID PREVENTION")
    print("-" * 60)
    print("\nTrying to add contact with duplicate ID 1001:")
    success = pb.add_contact("Test", "User", 1001, "555-7777", "Test")
    if not success:
        print("✓ Correctly prevented duplicate ID!")
    
    # Demo 11: Edge Cases
    print("\n11. EDGE CASES")
    print("-" * 60)
    
    pb_empty = PhoneBook()
    print("\nTesting empty phone book:")
    pb_empty.list_contacts()
    
    print("\nAdding single contact and listing:")
    pb_empty.add_contact("Solo", "Contact", 9999, "555-0000", "Test")
    pb_empty.list_contacts()
    
    print("\nSorting single contact (should work):")
    pb_empty.sort_by_name()
    print("✓ Sort completed successfully!")
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nTo run the interactive application:")
    print("  python main.py")

if __name__ == "__main__":
    demo()
