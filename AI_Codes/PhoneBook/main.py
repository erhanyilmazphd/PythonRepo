"""
Main program with interactive menu for the Phone Book application
"""

from phonebook import PhoneBook

def print_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("         PHONE BOOK MANAGEMENT SYSTEM")
    print("="*50)
    print("1.  Add Contact")
    print("2.  Insert Contact (at specific position)")
    print("3.  List All Contacts")
    print("4.  Search Contact by ID")
    print("5.  Search Contact by Name")
    print("6.  Search Contact by Surname")
    print("7.  Search Contact by Phone")
    print("8.  Update Contact")
    print("9.  Delete Contact")
    print("10. Sort by Name")
    print("11. Sort by Surname")
    print("12. Sort by ID")
    print("13. Sort by Phone")
    print("14. Sort by Profession")
    print("15. Save Phone Book")
    print("16. Load Phone Book")
    print("17. Exit")
    print("="*50)

def get_contact_info():
    """Get contact information from user"""
    try:
        name = input("Enter first name: ").strip()
        if not name:
            print("Error: Name cannot be empty!")
            return None
        
        surname = input("Enter surname: ").strip()
        if not surname:
            print("Error: Surname cannot be empty!")
            return None
        
        contact_id = int(input("Enter ID: "))
        
        phone = input("Enter phone number: ").strip()
        if not phone:
            print("Error: Phone number cannot be empty!")
            return None
        
        profession = input("Enter profession: ").strip()
        if not profession:
            print("Error: Profession cannot be empty!")
            return None
        
        return name, surname, contact_id, phone, profession
    except ValueError:
        print("Error: Invalid input format!")
        return None

def display_search_results(results, search_type):
    """Display search results"""
    if not results:
        print(f"\nNo contacts found matching the search criteria!")
        return
    
    print(f"\n{len(results)} contact(s) found:")
    print("-" * 90)
    for i, node in enumerate(results, 1):
        print(f"{i}. {node.contact}")
    print()

def main():
    """Main program loop"""
    pb = PhoneBook()
    
    # Load existing phone book if available
    pb.load_from_file('phonebook.json')
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-17): ").strip()
        
        if choice == '1':
            # Add Contact
            print("\n--- Add Contact ---")
            info = get_contact_info()
            if info:
                success = pb.add_contact(*info)
                if success:
                    print(f"✓ Contact '{info[0]} {info[1]}' added successfully!")
        
        elif choice == '2':
            # Insert Contact
            print("\n--- Insert Contact ---")
            print(f"Current contacts: {pb.get_count()}")
            try:
                position = int(input(f"Enter position (0 to {pb.get_count()}): "))
                info = get_contact_info()
                if info:
                    success = pb.insert_contact(position, *info)
                    if success:
                        print(f"✓ Contact '{info[0]} {info[1]}' inserted at position {position}!")
            except ValueError:
                print("Error: Invalid position!")
        
        elif choice == '3':
            # List All Contacts
            pb.list_contacts()
        
        elif choice == '4':
            # Search by ID
            try:
                contact_id = int(input("\nEnter ID to search: "))
                node = pb.search_by_id(contact_id)
                if node:
                    print(f"\nContact found:\n{node.contact}\n")
                else:
                    print(f"\nNo contact found with ID {contact_id}!\n")
            except ValueError:
                print("Error: Invalid ID format!")
        
        elif choice == '5':
            # Search by Name
            name = input("\nEnter name to search: ").strip()
            results = pb.search_by_name(name)
            display_search_results(results, "name")
        
        elif choice == '6':
            # Search by Surname
            surname = input("\nEnter surname to search: ").strip()
            results = pb.search_by_surname(surname)
            display_search_results(results, "surname")
        
        elif choice == '7':
            # Search by Phone
            phone = input("\nEnter phone number to search: ").strip()
            node = pb.search_by_phone(phone)
            if node:
                print(f"\nContact found:\n{node.contact}\n")
            else:
                print(f"\nNo contact found with phone {phone}!\n")
        
        elif choice == '8':
            # Update Contact
            try:
                contact_id = int(input("\nEnter ID of contact to update: "))
                print("(Leave field empty to keep current value)")
                name = input("New name (optional): ").strip() or None
                surname = input("New surname (optional): ").strip() or None
                phone = input("New phone (optional): ").strip() or None
                profession = input("New profession (optional): ").strip() or None
                
                if pb.update_contact(contact_id, name, surname, phone, profession):
                    print("✓ Contact updated successfully!")
            except ValueError:
                print("Error: Invalid ID format!")
        
        elif choice == '9':
            # Delete Contact
            try:
                contact_id = int(input("\nEnter ID of contact to delete: "))
                if pb.delete_contact(contact_id):
                    print(f"✓ Contact with ID {contact_id} deleted successfully!")
            except ValueError:
                print("Error: Invalid ID format!")
        
        elif choice == '10':
            # Sort by Name
            print("\nSorting by name...")
            pb.sort_by_name()
            print("✓ Phone book sorted by name!")
            pb.list_contacts()
        
        elif choice == '11':
            # Sort by Surname
            print("\nSorting by surname...")
            pb.sort_by_surname()
            print("✓ Phone book sorted by surname!")
            pb.list_contacts()
        
        elif choice == '12':
            # Sort by ID
            print("\nSorting by ID...")
            pb.sort_by_id()
            print("✓ Phone book sorted by ID!")
            pb.list_contacts()
        
        elif choice == '13':
            # Sort by Phone
            print("\nSorting by phone...")
            pb.sort_by_phone()
            print("✓ Phone book sorted by phone!")
            pb.list_contacts()
        
        elif choice == '14':
            # Sort by Profession
            print("\nSorting by profession...")
            pb.sort_by_profession()
            print("✓ Phone book sorted by profession!")
            pb.list_contacts()
        
        elif choice == '15':
            # Save Phone Book
            filename = input("\nEnter filename to save (default: phonebook.json): ").strip()
            if not filename:
                filename = 'phonebook.json'
            pb.save_to_file(filename)
        
        elif choice == '16':
            # Load Phone Book
            filename = input("\nEnter filename to load (default: phonebook.json): ").strip()
            if not filename:
                filename = 'phonebook.json'
            pb.load_from_file(filename)
        
        elif choice == '17':
            # Exit
            print("\nDo you want to save before exiting? (y/n): ", end="")
            if input().strip().lower() == 'y':
                pb.save_to_file('phonebook.json')
            print("Thank you for using Phone Book Management System!")
            break
        
        else:
            print("Error: Invalid choice! Please enter a number between 1 and 17.")

if __name__ == "__main__":
    main()
