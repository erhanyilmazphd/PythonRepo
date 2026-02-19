# Phone Book Management System

A comprehensive Python application that implements a doubly-linked list-based phone book with full contact management capabilities.

## Project Structure

```
PhoneBook/
├── contact.py       # Contact class definition
├── node.py          # Node class for doubly-linked list
├── phonebook.py     # PhoneBook class with all operations
├── main.py          # Interactive user interface
├── phonebook.json   # Saved contacts (auto-generated)
└── README.md        # This file
```

## Features

### Core Operations

1. **Add Contact** - Append a new contact to the end of the list
2. **Insert Contact** - Insert a contact at a specific position
3. **List/Print Contacts** - Display all contacts in a formatted table
4. **Search Contacts**:
   - By ID (unique identifier)
   - By Name (first name, case-insensitive)
   - By Surname (last name, case-insensitive)
   - By Phone Number
5. **Update Contact** - Modify contact information
6. **Delete Contact** - Remove a contact by ID
7. **Sort Operations** - Sort by:
   - Name (alphabetically)
   - Surname (alphabetically)
   - ID (numerically)
   - Phone Number
   - Profession (alphabetically)
8. **Save/Load** - Persist contacts to/from JSON files

### Data Structure

Each contact contains:
- **Name**: First name of the contact
- **Surname**: Last name of the contact
- **ID**: Unique identifier (integer)
- **Phone**: Phone number (string)
- **Profession**: Contact's profession/occupation

### Implementation Details

- **Doubly-Linked List**: Each node has `prev` and `next` pointers, allowing bidirectional traversal
- **Bubble Sort**: Used for all sorting operations (suitable for linked lists)
- **JSON Storage**: Contacts are saved in human-readable JSON format
- **ID Uniqueness**: System prevents duplicate IDs

## Usage

### Running the Application

```bash
python main.py
```

### Menu Options

```
1.  Add Contact                    - Add a new contact to the end
2.  Insert Contact                 - Insert at specific position
3.  List All Contacts              - Display all contacts
4.  Search by ID                   - Find contact by unique ID
5.  Search by Name                 - Find contacts by first name
6.  Search by Surname              - Find contacts by last name
7.  Search by Phone                - Find contact by phone number
8.  Update Contact                 - Modify contact information
9.  Delete Contact                 - Remove a contact
10. Sort by Name                   - Sort alphabetically by first name
11. Sort by Surname                - Sort alphabetically by last name
12. Sort by ID                     - Sort by ID number
13. Sort by Phone                  - Sort by phone number
14. Sort by Profession             - Sort by profession
15. Save Phone Book                - Save to JSON file
16. Load Phone Book                - Load from JSON file
17. Exit                           - Exit the application
```

## Examples

### Example Session

```
1. Add Contact
   - Name: John
   - Surname: Doe
   - ID: 1001
   - Phone: 555-1234
   - Profession: Engineer

2. Add Contact
   - Name: Jane
   - Surname: Smith
   - ID: 1002
   - Phone: 555-5678
   - Profession: Doctor

3. List All Contacts
   ═══════════════════════════════════════════════════════════════════════════════════════════
   Phone Book (2 contacts)
   ═══════════════════════════════════════════════════════════════════════════════════════════
   1. ID: 1001 | Name: John           | Surname: Doe            | Phone: 555-1234     | Profession: Engineer
   2. ID: 1002 | Name: Jane           | Surname: Smith          | Phone: 555-5678     | Profession: Doctor
   ═══════════════════════════════════════════════════════════════════════════════════════════

4. Sort by Name
   ═══════════════════════════════════════════════════════════════════════════════════════════
   Phone Book (2 contacts)
   ═══════════════════════════════════════════════════════════════════════════════════════════
   1. ID: 1002 | Name: Jane           | Surname: Smith          | Phone: 555-5678     | Profession: Doctor
   2. ID: 1001 | Name: John           | Surname: Doe            | Phone: 555-1234     | Profession: Engineer
   ═══════════════════════════════════════════════════════════════════════════════════════════
```

## Class Documentation

### Contact Class

```python
Contact(name, surname, contact_id, phone, profession)
```

**Methods:**
- `to_dict()` - Convert to dictionary for storage
- `from_dict(data)` - Create from dictionary
- `update(name, surname, phone, profession)` - Update fields

### Node Class

```python
Node(contact)
```

**Attributes:**
- `contact` - Contact object
- `next` - Reference to next node
- `prev` - Reference to previous node

### PhoneBook Class

**Main Methods:**
- `add_contact(name, surname, contact_id, phone, profession)` - Add at end
- `insert_contact(position, ...)` - Insert at position
- `delete_contact(contact_id)` - Delete by ID
- `list_contacts()` - Print all contacts
- `search_by_id(contact_id)` - Search by ID
- `search_by_name(name)` - Search by name
- `search_by_surname(surname)` - Search by surname
- `search_by_phone(phone)` - Search by phone
- `sort_by_name()` - Sort by name
- `sort_by_surname()` - Sort by surname
- `sort_by_id()` - Sort by ID
- `sort_by_phone()` - Sort by phone
- `sort_by_profession()` - Sort by profession
- `update_contact(contact_id, ...)` - Update contact
- `save_to_file(filename)` - Save to JSON
- `load_from_file(filename)` - Load from JSON

## File Format

Contacts are saved in JSON format:

```json
[
    {
        "name": "John",
        "surname": "Doe",
        "id": 1001,
        "phone": "555-1234",
        "profession": "Engineer"
    },
    {
        "name": "Jane",
        "surname": "Smith",
        "id": 1002,
        "phone": "555-5678",
        "profession": "Doctor"
    }
]
```

## Time Complexity

| Operation | Time Complexity |
|-----------|-----------------|
| Add Contact | O(1) |
| Insert at Position | O(n) |
| Delete | O(n) |
| Search by ID | O(n) |
| Search by Name/Surname | O(n) |
| Sort | O(n²) |
| List | O(n) |

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Features Highlights

✓ Doubly-linked list implementation  
✓ Full CRUD operations  
✓ Multiple sorting options  
✓ Multiple search capabilities  
✓ Persistent storage (JSON)  
✓ User-friendly interactive menu  
✓ Input validation  
✓ Duplicate ID prevention  
✓ Formatted output display  

## Error Handling

The application includes comprehensive error handling for:
- Invalid input format
- Duplicate IDs
- Non-existent contacts
- File I/O errors
- Invalid positions
- Invalid menu choices

## Future Enhancements

Potential improvements:
- Export to CSV or other formats
- Import from external sources
- Advanced search filters
- More efficient sorting algorithms (merge sort, quick sort)
- Database integration
- GUI implementation
- Contact groups/categories
- Call/message history
- Contact backup features

## License

This is an educational project.
