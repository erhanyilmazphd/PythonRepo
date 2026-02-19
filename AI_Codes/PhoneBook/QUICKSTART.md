# Phone Book Project - Quick Start Guide

## 📁 Project Files Created

Your Python Phone Book project has been created in:
```
/home/erhan/work/learning/PythonProgramming/PythonRepo/AI_Codes/PhoneBook/
```

### Files:

1. **contact.py** - Contact class with fields (Name, Surname, ID, Phone, Profession)
2. **node.py** - Node class for doubly-linked list structure
3. **phonebook.py** - PhoneBook class with all operations
4. **main.py** - Interactive menu-driven application
5. **demo.py** - Demonstration script showing all features
6. **README.md** - Comprehensive documentation

## 🚀 Quick Start

### Option 1: Run Interactive Application
```bash
cd /home/erhan/work/learning/PythonProgramming/PythonRepo/AI_Codes/PhoneBook/
python main.py
```

### Option 2: Run Demo Script
```bash
python demo.py
```

This will show all features in action without user interaction.

## 📋 Supported Operations

### Add/Insert Operations
- **Add Contact** - Append to the end
- **Insert Contact** - Insert at specific position

### Display Operations
- **List/Print** - Show all contacts in formatted table

### Search Operations
- **Search by ID** - Find by unique identifier
- **Search by Name** - Find by first name
- **Search by Surname** - Find by last name
- **Search by Phone** - Find by phone number

### Sort Operations (per field)
- **Sort by Name** - Alphabetically by first name
- **Sort by Surname** - Alphabetically by last name
- **Sort by ID** - Numerically ascending
- **Sort by Phone** - Phone number order
- **Sort by Profession** - Alphabetically by profession

### Modify Operations
- **Update Contact** - Modify contact information
- **Delete Contact** - Remove by ID

### File Operations
- **Save** - Save phone book to JSON file
- **Load** - Load phone book from JSON file

## 🏗️ Data Structure

```
PhoneBook
  ├─ head ──→ Node
  │            ├─ prev ◄────┐
  │            ├─ contact   │
  │            │   ├─ Name  │
  │            │   ├─ Surname
  │            │   ├─ ID    │
  │            │   ├─ Phone │
  │            │   └─ Profession
  │            └─ next ───→ Node ────┐
  │                         ├─ prev ◄─┘
  │                         └─ ...
  └─ tail ──→ (last Node)
```

Each node contains:
- **Contact** object with fields
- **prev** pointer (doubly-linked)
- **next** pointer (doubly-linked)

## 📊 Example Usage in Code

```python
from phonebook import PhoneBook

# Create phone book
pb = PhoneBook()

# Add contacts
pb.add_contact("John", "Doe", 1001, "555-1234", "Engineer")
pb.add_contact("Jane", "Smith", 1002, "555-5678", "Doctor")

# List all
pb.list_contacts()

# Search
contact = pb.search_by_id(1001)

# Sort
pb.sort_by_name()

# Update
pb.update_contact(1001, phone="555-9999")

# Delete
pb.delete_contact(1002)

# Save
pb.save_to_file("my_contacts.json")

# Load
pb.load_from_file("my_contacts.json")
```

## 🎯 Key Features

✅ **Doubly-Linked List** - Bidirectional traversal capable  
✅ **Bubble Sort** - Implemented for all sorting operations  
✅ **JSON Storage** - Human-readable file format  
✅ **ID Uniqueness** - Prevents duplicate entries  
✅ **Error Handling** - Comprehensive validation  
✅ **User-Friendly Menu** - Interactive interface  
✅ **Search Flexibility** - Multiple search methods  
✅ **Data Persistence** - Save and load functionality  

## 📝 Contact Fields

Every contact must have:
- **Name** (string) - First name
- **Surname** (string) - Last name
- **ID** (integer) - Unique identifier
- **Phone** (string) - Phone number
- **Profession** (string) - Job title/profession

## 💾 File Format

Contacts are stored in JSON:
```json
[
  {
    "name": "John",
    "surname": "Doe",
    "id": 1001,
    "phone": "555-1234",
    "profession": "Engineer"
  }
]
```

## ⚙️ Requirements

- Python 3.6 or higher
- No external libraries required (uses only standard library)

## 🔧 Troubleshooting

**Q: How do I run the application?**
A: Navigate to the project directory and run `python main.py`

**Q: Can I modify existing contacts?**
A: Yes, use the Update option (menu item 8)

**Q: Can I load contacts from a different file?**
A: Yes, the Load option (menu item 16) lets you specify a filename

**Q: Will my contacts be saved when I exit?**
A: The application will ask if you want to save before exiting

**Q: Can I have duplicate IDs?**
A: No, the system prevents duplicate IDs automatically

## 📚 Additional Resources

- See **README.md** for detailed documentation
- Run **demo.py** to see all features in action
- Review **main.py** for interactive menu implementation
- Check **phonebook.py** for all class methods

## 🎓 Learning Points

This project demonstrates:
- Doubly-linked list implementation
- Bubble sort algorithm
- File I/O with JSON
- Object-oriented programming
- Data validation and error handling
- Interactive menu-driven application design
- Search and sort algorithms
- Time complexity considerations

---

**Enjoy your Phone Book management system!** 📱
