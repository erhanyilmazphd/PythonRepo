# Phone Book GUI Applications

Two beautiful GUI applications for the Phone Book project with modern, chic interfaces!

## 🎨 Available GUI Applications

### 1. **gui_app.py** - Classic Modern GUI
A clean and professional GUI with a two-column layout.

```bash
python gui_app.py
```

**Features:**
- Professional layout with form on left, list on right
- Clean white and blue color scheme
- Easy-to-use buttons and controls
- Right-click context menu
- Double-click to load contacts for editing
- Formatted contact table display

### 2. **gui_app_modern.py** - Premium Modern GUI ⭐ (Recommended)
An even more stylish and modern interface with premium design elements.

```bash
python gui_app_modern.py
```

**Features:**
- Stunning header banner
- Sidebar with organized sections
- Modern color palette (blue, teal, coral)
- Smooth button animations
- Professional spacing and typography
- Better visual hierarchy
- Enhanced user experience

## 🚀 Quick Start

### Prerequisites
- Python 3.6+
- tkinter (usually comes with Python)

### Running the Applications

**Option 1: Classic GUI**
```bash
cd /home/erhan/work/learning/PythonProgramming/PythonRepo/AI_Codes/PhoneBook/
python gui_app.py
```

**Option 2: Modern Premium GUI (Recommended)**
```bash
python gui_app_modern.py
```

## 📋 Features Comparison

| Feature | gui_app.py | gui_app_modern.py |
|---------|-----------|-----------------|
| Add Contact | ✅ | ✅ |
| Edit Contact | ✅ | ✅ |
| Delete Contact | ✅ | ✅ |
| Search | ✅ | ✅ |
| Sort (all fields) | ✅ | ✅ |
| View Details | ✅ | ✅ |
| Save to JSON | ✅ | ✅ |
| Load from JSON | ✅ | ✅ |
| Export to CSV | ✅ | ✅ |
| Modern Design | ✅ | ✅✅ |
| Premium Styling | - | ✅ |
| Context Menu | ✅ | ✅ |
| Dark Sidebar | - | ✅ |

## 🎯 How to Use

### Adding a Contact
1. Fill all fields in the form:
   - Name
   - Surname
   - ID (unique number)
   - Phone
   - Profession
2. Click "➕ Add Contact" button
3. Contact appears in the list

### Editing a Contact
**Method 1: Double-click on list**
1. Double-click on a contact in the list
2. Form fields populate automatically
3. Modify desired fields
4. Click "✏️ Edit" button

**Method 2: Search and edit**
1. Use search to find contact
2. Double-click to load
3. Make changes
4. Click Edit

### Deleting a Contact
1. Select contact in list
2. Click "🗑️ Delete Selected"
3. Confirm deletion in dialog

### Searching
1. Select search type (ID, Name, Surname, Phone)
2. Enter search value
3. Click "🔎 Search"
4. Results display in list

### Sorting
Click any sort button:
- **Name** - Sort by first name (A-Z)
- **Surname** - Sort by last name (A-Z)
- **ID** - Sort by ID number
- **Phone** - Sort by phone number
- **Profession** - Sort by profession (A-Z)

### File Operations

**Save to JSON:**
1. Click "💾 Save" button
2. Choose filename and location
3. Contacts are saved in JSON format

**Load from JSON:**
1. Click "📂 Load" button
2. Select JSON file
3. All contacts load into application

**Export to CSV:**
1. Click "📤 CSV" button
2. Choose filename and location
3. Contacts exported in CSV format for Excel/spreadsheet use

## 🎨 UI Elements

### Classic GUI (gui_app.py)
```
┌─────────────────────────────────────────────┐
│  Phone Book Manager                  Count: 5│
├─────────────────────────────────────────────┤
│ LEFT PANEL        │   RIGHT PANEL           │
│                   │                         │
│ Form Fields       │   Contact List          │
│ ┌──────────────┐  │   ┌───────────────────┐ │
│ │ Name:  [   ] │  │   │ ID│Name│Surname...│ │
│ │ Surn:  [   ] │  │   │  1│John│ Doe   ..│ │
│ │ ID:    [   ] │  │   │  2│Jane│Smith ..  │ │
│ │ Phone: [   ] │  │   │  3│Bob │Brown ..  │ │
│ │ Prof:  [   ] │  │   └───────────────────┘ │
│ │               │  │   [Delete] [Details]   │
│ │ [Add] [Edit]  │  │                         │
│ │ [Clear]       │  │                         │
│ └──────────────┘  │                         │
│                   │                         │
│ Search & Sort     │                         │
│ [Buttons...]      │                         │
│                   │                         │
│ File Operations   │                         │
│ [Save] [Load]     │                         │
└─────────────────────────────────────────────┘
```

### Modern GUI (gui_app_modern.py)
```
╔═════════════════════════════════════════════╗
║  📱 Phone Book Manager Pro                  ║
║                              Total: 5       ║
╠════════════════╦═══════════════════════════╣
║ SIDEBAR        ║   CONTENT AREA            ║
║                ║                           ║
║ ✏️ Add/Edit    ║   📋 Contacts List        ║
║ [Form]         ║   ┌─────────────────────┐ ║
║ [Buttons]      ║   │ ID│Name│Surname..  │ ║
║                ║   ├─────────────────────┤ ║
║ 🔍 Search      ║   │ 1 │John│Doe...      │ ║
║ [Type] [Input] ║   │ 2 │Jane│Smith...   │ ║
║ [Search]       ║   │ 3 │Bob │Brown...   │ ║
║                ║   └─────────────────────┘ ║
║ ↕️ Sort         ║   [Delete] [Details]    ║
║ [Buttons...]   ║                           ║
║                ║                           ║
║ 💾 File        ║                           ║
║ [Save]         ║                           ║
║ [Load]         ║                           ║
║ [CSV]          ║                           ║
╚════════════════╩═══════════════════════════╝
```

## 🎯 Keyboard Shortcuts

- **Double-click** on contact → Load to form
- **Right-click** on contact → Context menu
- **Escape** → Clear search (manual)

## 💡 Tips & Tricks

1. **Quick Edit**: Double-click any contact to load it into the form
2. **Right-Click**: Right-click on contacts for quick options
3. **Search First**: Use search to find contacts before editing
4. **Backup**: Always save your data regularly
5. **Multiple Files**: Use Load to switch between different phone books

## 🔧 Troubleshooting

**Q: How do I switch between GUI versions?**
A: Just run the other script. They share the same data files.

**Q: Lost my contacts?**
A: Check if phonebook.json exists. You can load from backup.

**Q: How do I know if my data is saved?**
A: The application auto-saves when you save explicitly. Check the phonebook.json file.

**Q: Can I have duplicate IDs?**
A: No, the system prevents this automatically with an error message.

**Q: Can I edit while searching?**
A: Yes! Double-click the search result to load it into the form.

## 📊 Color Scheme

### Classic GUI (gui_app.py)
- Primary: Blue (#2196F3)
- Secondary: Amber (#FFC107)
- Success: Green (#4CAF50)
- Danger: Red (#f44336)
- Background: Light Gray (#f0f0f0)

### Modern GUI (gui_app_modern.py)
- Primary: Blue (#2196F3)
- Secondary: Coral (#FF6B6B)
- Accent: Teal (#4ECDC4)
- Success: Mint (#95E1D3)
- Warning: Orange (#FFA502)
- Dark: Slate (#2C3E50)
- Light: Off-white (#ECF0F1)

## 📱 Cross-Platform Support

Both applications work on:
- ✅ Windows
- ✅ macOS
- ✅ Linux

## 📚 File Formats

### JSON Format (Default)
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

### CSV Format (Export)
```
ID,Name,Surname,Phone,Profession
1001,John,Doe,555-1234,Engineer
```

## 🎓 Learning Code

The GUI applications demonstrate:
- tkinter GUI development
- Widget styling and layout
- Event handling
- File operations
- Data validation
- Professional UI/UX design

## 🚀 Future Enhancements

Potential improvements:
- Dark mode toggle
- Contact photos
- Favorites/starred contacts
- Recent contacts
- Contact groups
- Import/export from vCard format
- Search history
- Themes/customization

## ❓ FAQ

**Q: Which GUI should I use?**
A: gui_app_modern.py for a premium experience, gui_app.py for simplicity.

**Q: Do they share the same data?**
A: Yes! Both applications save/load from the same phonebook.json file.

**Q: Can I run both at the same time?**
A: Yes, but edit one at a time to avoid conflicts.

**Q: Is there a command-line version?**
A: Yes! Run `main.py` for the CLI version.

---

Enjoy your modern Phone Book application! 📱✨
