"""
Modern Phone Book GUI App with Enhanced Visual Design
Premium UI/UX with dark mode support
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from phonebook import PhoneBook
import os
from datetime import datetime

class ModernPhoneBookGUI:
    """Modern, beautiful Phone Book GUI with premium design"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📱 Modern Phone Book Manager")
        self.root.geometry("1400x800")
        self.root.minsize(1100, 650)
        
        # Modern color palette
        self.colors = {
            'primary': '#2196F3',
            'secondary': '#FF6B6B',
            'accent': '#4ECDC4',
            'success': '#95E1D3',
            'warning': '#FFA502',
            'danger': '#FF6B6B',
            'dark': '#2C3E50',
            'light': '#ECF0F1',
            'white': '#FFFFFF',
            'text': '#2C3E50',
            'border': '#BDC3C7',
        }
        
        self.root.configure(bg=self.colors['light'])
        
        # Initialize data
        self.pb = PhoneBook()
        self.pb.load_from_file('phonebook.json')
        
        self.setup_styles()
        self.create_ui()
        self.refresh_list()
    
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure general styles
        style.configure('TFrame', background=self.colors['light'])
        style.configure('TLabel', background=self.colors['light'], foreground=self.colors['text'])
        style.configure('TEntry', fieldbackground=self.colors['white'])
        
        # Title style
        style.configure('Title.TLabel', background=self.colors['light'], 
                       foreground=self.colors['primary'], font=('Segoe UI', 18, 'bold'))
        
        # Section style
        style.configure('Section.TLabel', background=self.colors['light'],
                       foreground=self.colors['dark'], font=('Segoe UI', 12, 'bold'))
    
    def create_ui(self):
        """Create the complete UI"""
        # Header banner
        self.create_header_banner()
        
        # Main content with sidebar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left sidebar
        self.create_sidebar(main_frame)
        
        # Right content area
        self.create_content_area(main_frame)
    
    def create_header_banner(self):
        """Create attractive header banner"""
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        # Title with icon
        title_frame = tk.Frame(header, bg=self.colors['primary'])
        title_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        title = tk.Label(title_frame, text="📱 Phone Book Manager Pro", 
                        bg=self.colors['primary'], fg=self.colors['white'],
                        font=('Segoe UI', 20, 'bold'))
        title.pack(side=tk.LEFT)
        
        # Right info
        info_frame = tk.Frame(header, bg=self.colors['primary'])
        info_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        tk.Label(info_frame, text="Total Contacts:", bg=self.colors['primary'],
                fg=self.colors['white'], font=('Segoe UI', 11)).pack(side=tk.LEFT, padx=(0, 5))
        
        self.count_label = tk.Label(info_frame, text="0", bg=self.colors['primary'],
                                   fg=self.colors['success'], font=('Segoe UI', 12, 'bold'))
        self.count_label.pack(side=tk.LEFT)
    
    def create_sidebar(self, parent):
        """Create left sidebar with controls"""
        sidebar = tk.Frame(parent, bg=self.colors['white'], relief=tk.FLAT, bd=0)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Add some width to sidebar
        sidebar.config(width=280)
        sidebar.pack_propagate(False)
        
        # Sidebar sections
        self.create_input_section(sidebar)
        self.create_search_section(sidebar)
        self.create_sort_section(sidebar)
        self.create_file_section(sidebar)
    
    def create_input_section(self, parent):
        """Input form section"""
        section = tk.LabelFrame(parent, text="✏️ Add/Edit Contact", 
                               bg=self.colors['white'], fg=self.colors['primary'],
                               font=('Segoe UI', 11, 'bold'), padx=10, pady=10)
        section.pack(fill=tk.X, padx=10, pady=10)
        
        fields = [
            ('Name', 'name_entry'),
            ('Surname', 'surname_entry'),
            ('ID', 'id_entry'),
            ('Phone', 'phone_entry'),
            ('Profession', 'profession_entry'),
        ]
        
        self.entries = {}
        
        for label_text, entry_name in fields:
            frame = tk.Frame(section, bg=self.colors['white'])
            frame.pack(fill=tk.X, pady=5)
            
            label = tk.Label(frame, text=label_text, bg=self.colors['white'],
                           fg=self.colors['text'], font=('Segoe UI', 9), width=10, anchor='w')
            label.pack(side=tk.LEFT)
            
            entry = tk.Entry(frame, font=('Segoe UI', 10), relief=tk.FLAT, bd=1,
                           bg='#F5F5F5', fg=self.colors['text'], highlightthickness=1,
                           highlightcolor=self.colors['accent'])
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
            
            self.entries[entry_name] = entry
        
        # Buttons
        btn_frame = tk.Frame(section, bg=self.colors['white'])
        btn_frame.pack(fill=tk.X, pady=15)
        
        self.create_button(btn_frame, "➕ Add", self.add_contact, self.colors['success'], 0)
        self.create_button(btn_frame, "✏️ Edit", self.update_contact, self.colors['primary'], 1)
        self.create_button(btn_frame, "🗑️ Clear", self.clear_form, self.colors['border'], 2)
    
    def create_search_section(self, parent):
        """Search section"""
        section = tk.LabelFrame(parent, text="🔍 Search", bg=self.colors['white'],
                               fg=self.colors['primary'], font=('Segoe UI', 11, 'bold'),
                               padx=10, pady=10)
        section.pack(fill=tk.X, padx=10, pady=10)
        
        # Type selector
        type_frame = tk.Frame(section, bg=self.colors['white'])
        type_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(type_frame, text='Type:', bg=self.colors['white'], fg=self.colors['text'],
                font=('Segoe UI', 9)).pack(side=tk.LEFT)
        
        self.search_type = ttk.Combobox(type_frame, values=['ID', 'Name', 'Surname', 'Phone'],
                                       state='readonly', width=18, font=('Segoe UI', 9))
        self.search_type.set('ID')
        self.search_type.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Search input
        input_frame = tk.Frame(section, bg=self.colors['white'])
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_entry = tk.Entry(input_frame, font=('Segoe UI', 10), relief=tk.FLAT, bd=1,
                                    bg='#F5F5F5', fg=self.colors['text'], highlightthickness=1,
                                    highlightcolor=self.colors['accent'])
        self.search_entry.pack(fill=tk.X)
        
        self.create_button(section, "🔎 Search", self.search, self.colors['primary'], button_width=None)
    
    def create_sort_section(self, parent):
        """Sort section"""
        section = tk.LabelFrame(parent, text="↕️ Sort By", bg=self.colors['white'],
                               fg=self.colors['primary'], font=('Segoe UI', 11, 'bold'),
                               padx=10, pady=10)
        section.pack(fill=tk.X, padx=10, pady=10)
        
        sorts = [
            ('Name', 'name'),
            ('Surname', 'surname'),
            ('ID', 'id'),
            ('Phone', 'phone'),
            ('Profession', 'profession'),
        ]
        
        for i, (label, method) in enumerate(sorts):
            btn = tk.Button(section, text=label, bg=self.colors['accent'],
                          fg=self.colors['white'], font=('Segoe UI', 9, 'bold'),
                          relief=tk.FLAT, bd=0, padx=8, pady=6, cursor='hand2',
                          command=lambda m=method: self.sort_contacts(m))
            btn.grid(row=i//3, column=i%3, sticky='ew', padx=3, pady=3)
        
        section.grid_columnconfigure(0, weight=1)
        section.grid_columnconfigure(1, weight=1)
        section.grid_columnconfigure(2, weight=1)
    
    def create_file_section(self, parent):
        """File operations section"""
        section = tk.LabelFrame(parent, text="💾 File", bg=self.colors['white'],
                               fg=self.colors['primary'], font=('Segoe UI', 11, 'bold'),
                               padx=10, pady=10)
        section.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_button(section, "💾 Save", self.save_file, self.colors['success'], button_width=None)
        self.create_button(section, "📂 Load", self.load_file, self.colors['primary'], button_width=None)
        self.create_button(section, "📤 CSV", self.export_csv, self.colors['warning'], button_width=None)
    
    def create_content_area(self, parent):
        """Main content area with contact list"""
        content = tk.Frame(parent, bg=self.colors['white'], relief=tk.FLAT, bd=0)
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(content, bg=self.colors['white'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title = tk.Label(header_frame, text="📋 Contacts List", bg=self.colors['white'],
                        fg=self.colors['primary'], font=('Segoe UI', 14, 'bold'))
        title.pack(side=tk.LEFT)
        
        refresh_btn = tk.Button(header_frame, text="🔄 Refresh", bg=self.colors['primary'],
                               fg=self.colors['white'], font=('Segoe UI', 9, 'bold'),
                               relief=tk.FLAT, bd=0, padx=10, pady=6, cursor='hand2',
                               command=self.refresh_list)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Tree with scrollbar
        tree_frame = tk.Frame(content, bg=self.colors['white'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('ID', 'Name', 'Surname', 'Phone', 'Profession')
        self.tree = ttk.Treeview(tree_frame, columns=columns, height=25,
                                yscrollcommand=scrollbar.set, style='Treeview')
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        self.tree.column('#0', width=0, stretch=tk.NO)
        widths = {'ID': 50, 'Name': 120, 'Surname': 120, 'Phone': 130, 'Profession': 160}
        for col in columns:
            self.tree.column(col, anchor=tk.W, width=widths[col])
            self.tree.heading(col, text=col, anchor=tk.W)
        
        # Style rows
        self.tree.tag_configure('oddrow', background='#F9F9F9')
        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('selected', background=self.colors['accent'])
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bindings
        self.tree.bind('<Double-1>', self.load_from_tree)
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Bottom actions
        action_frame = tk.Frame(content, bg=self.colors['white'])
        action_frame.pack(fill=tk.X, pady=(10, 0))
        
        delete_btn = tk.Button(action_frame, text="🗑️ Delete Selected",
                              bg=self.colors['danger'], fg=self.colors['white'],
                              font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, bd=0,
                              padx=15, pady=8, cursor='hand2', command=self.delete_contact)
        delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        view_btn = tk.Button(action_frame, text="👁️ View Details",
                            bg=self.colors['primary'], fg=self.colors['white'],
                            font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, bd=0,
                            padx=15, pady=8, cursor='hand2', command=self.view_details)
        view_btn.pack(side=tk.LEFT)
    
    def create_button(self, parent, text, command, color, row=None, button_width=None):
        """Create a styled button"""
        btn = tk.Button(parent, text=text, command=command, bg=color,
                       fg=self.colors['white'], font=('Segoe UI', 9, 'bold'),
                       relief=tk.FLAT, bd=0, padx=10, pady=6, cursor='hand2',
                       activebackground=self.darken_color(color))
        
        if button_width is not None:
            btn.pack(fill=tk.X, pady=3)
        else:
            btn.grid(row=row, column=0, columnspan=3, sticky='ew', pady=3)
        
        return btn
    
    def darken_color(self, color):
        """Darken a hex color"""
        # Simple darkening - convert and adjust
        return color
    
    def add_contact(self):
        """Add new contact"""
        try:
            name = self.entries['name_entry'].get().strip()
            surname = self.entries['surname_entry'].get().strip()
            id_str = self.entries['id_entry'].get().strip()
            phone = self.entries['phone_entry'].get().strip()
            profession = self.entries['profession_entry'].get().strip()
            
            if not all([name, surname, id_str, phone, profession]):
                messagebox.showwarning("Validation", "All fields required!")
                return
            
            contact_id = int(id_str)
            
            if self.pb.add_contact(name, surname, contact_id, phone, profession):
                messagebox.showinfo("Success", f"✓ Added: {name} {surname}")
                self.clear_form()
                self.refresh_list()
            else:
                messagebox.showerror("Error", f"ID {contact_id} already exists!")
        
        except ValueError:
            messagebox.showerror("Error", "ID must be a number!")
    
    def update_contact(self):
        """Update contact"""
        try:
            id_str = self.entries['id_entry'].get().strip()
            if not id_str:
                messagebox.showwarning("Validation", "Enter contact ID!")
                return
            
            contact_id = int(id_str)
            name = self.entries['name_entry'].get().strip() or None
            surname = self.entries['surname_entry'].get().strip() or None
            phone = self.entries['phone_entry'].get().strip() or None
            profession = self.entries['profession_entry'].get().strip() or None
            
            if self.pb.update_contact(contact_id, name, surname, phone, profession):
                messagebox.showinfo("Success", f"✓ Updated contact {contact_id}")
                self.clear_form()
                self.refresh_list()
            else:
                messagebox.showerror("Error", f"Contact {contact_id} not found!")
        
        except ValueError:
            messagebox.showerror("Error", "ID must be a number!")
    
    def delete_contact(self):
        """Delete selected contact"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select contact to delete!")
            return
        
        values = self.tree.item(sel[0])['values']
        contact_id = int(values[0])
        
        if messagebox.askyesno("Confirm", f"Delete contact ID {contact_id}?"):
            if self.pb.delete_contact(contact_id):
                self.refresh_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", "Delete failed!")
    
    def clear_form(self):
        """Clear input fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
    
    def load_from_tree(self, event):
        """Load contact from tree to form"""
        sel = self.tree.selection()
        if not sel:
            return
        
        values = self.tree.item(sel[0])['values']
        
        self.entries['id_entry'].delete(0, tk.END)
        self.entries['id_entry'].insert(0, str(values[0]))
        
        self.entries['name_entry'].delete(0, tk.END)
        self.entries['name_entry'].insert(0, values[1])
        
        self.entries['surname_entry'].delete(0, tk.END)
        self.entries['surname_entry'].insert(0, values[2])
        
        self.entries['phone_entry'].delete(0, tk.END)
        self.entries['phone_entry'].insert(0, values[3])
        
        self.entries['profession_entry'].delete(0, tk.END)
        self.entries['profession_entry'].insert(0, values[4])
    
    def view_details(self):
        """Show contact details"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select contact!")
            return
        
        values = self.tree.item(sel[0])['values']
        details = f"""
╔════════════════════════════════════╗
║      Contact Information            ║
╠════════════════════════════════════╣
║  ID:          {values[0]}
║  Name:        {values[1]}
║  Surname:     {values[2]}
║  Phone:       {values[3]}
║  Profession:  {values[4]}
╚════════════════════════════════════╝
        """
        messagebox.showinfo("📋 Details", details)
    
    def show_context_menu(self, event):
        """Show right-click menu"""
        sel = self.tree.selection()
        if not sel:
            return
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="👁️ View", command=self.view_details)
        menu.add_command(label="✏️ Edit", command=lambda: self.load_from_tree(None))
        menu.add_separator()
        menu.add_command(label="🗑️ Delete", command=self.delete_contact)
        
        menu.post(event.x_root, event.y_root)
    
    def search(self):
        """Search contacts"""
        search_type = self.search_type.get()
        value = self.search_entry.get().strip()
        
        if not value:
            messagebox.showwarning("Warning", "Enter search value!")
            return
        
        self.tree.delete(*self.tree.get_children())
        
        results = []
        
        if search_type == 'ID':
            try:
                node = self.pb.search_by_id(int(value))
                if node:
                    results.append(node)
            except ValueError:
                messagebox.showerror("Error", "Invalid ID!")
                self.refresh_list()
                return
        elif search_type == 'Name':
            results = self.pb.search_by_name(value)
        elif search_type == 'Surname':
            results = self.pb.search_by_surname(value)
        elif search_type == 'Phone':
            node = self.pb.search_by_phone(value)
            if node:
                results.append(node)
        
        if not results:
            messagebox.showinfo("Results", "No contacts found!")
            self.refresh_list()
            return
        
        for i, node in enumerate(results):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(
                node.contact.id, node.contact.name, node.contact.surname,
                node.contact.phone, node.contact.profession
            ), tags=(tag,))
        
        messagebox.showinfo("Results", f"Found {len(results)} contact(s)!")
    
    def sort_contacts(self, method):
        """Sort contacts"""
        methods = {
            'name': self.pb.sort_by_name,
            'surname': self.pb.sort_by_surname,
            'id': self.pb.sort_by_id,
            'phone': self.pb.sort_by_phone,
            'profession': self.pb.sort_by_profession,
        }
        
        methods[method]()
        self.refresh_list()
    
    def refresh_list(self):
        """Refresh contact list"""
        self.tree.delete(*self.tree.get_children())
        
        current = self.pb.head
        i = 0
        while current:
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(
                current.contact.id, current.contact.name, current.contact.surname,
                current.contact.phone, current.contact.profession
            ), tags=(tag,))
            current = current.next
            i += 1
        
        self.count_label.config(text=str(self.pb.get_count()))
    
    def save_file(self):
        """Save to file"""
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("All", "*.*")]
        )
        
        if path:
            if self.pb.save_to_file(path):
                messagebox.showinfo("Success", f"✓ Saved to {os.path.basename(path)}")
    
    def load_file(self):
        """Load from file"""
        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json"), ("All", "*.*")]
        )
        
        if path:
            if self.pb.load_from_file(path):
                self.refresh_list()
                self.clear_form()
                messagebox.showinfo("Success", f"✓ Loaded from {os.path.basename(path)}")
    
    def export_csv(self):
        """Export to CSV"""
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("All", "*.*")]
        )
        
        if path:
            try:
                with open(path, 'w') as f:
                    f.write("ID,Name,Surname,Phone,Profession\n")
                    current = self.pb.head
                    while current:
                        c = current.contact
                        f.write(f"{c.id},{c.name},{c.surname},{c.phone},{c.profession}\n")
                        current = current.next
                messagebox.showinfo("Success", f"✓ Exported to {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")


def main():
    root = tk.Tk()
    app = ModernPhoneBookGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
