"""
Phone Book GUI Application with Modern Interface
Built with tkinter for cross-platform compatibility
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from phonebook import PhoneBook
from contact import Contact
import os

class PhoneBookGUI:
    """Modern GUI Application for Phone Book Management"""
    
    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("Phone Book Manager")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Set modern color scheme
        self.bg_color = "#f0f0f0"
        self.accent_color = "#2196F3"
        self.secondary_color = "#FFC107"
        self.danger_color = "#f44336"
        self.success_color = "#4CAF50"
        self.text_color = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize phone book
        self.pb = PhoneBook()
        self.pb.load_from_file('phonebook.json')
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.refresh_contact_list()
    
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        style.configure('Title.TLabel', background=self.bg_color, foreground=self.text_color, 
                       font=('Segoe UI', 16, 'bold'))
        style.configure('Header.TLabel', background=self.bg_color, foreground=self.accent_color,
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Accent.TButton', font=('Segoe UI', 10))
        style.map('Accent.TButton',
                 foreground=[('pressed', 'white'), ('active', 'white')],
                 background=[('pressed', '#1976D2'), ('active', '#1E88E5')])
        
        style.configure('TEntry', fieldbackground='white', foreground=self.text_color)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_container)
        
        # Content area with two columns
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Left panel - Form
        self.create_form_panel(content_frame)
        
        # Right panel - List
        self.create_list_panel(content_frame)
        
        # Footer
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """Create header section"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="📱 Phone Book Manager", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        count_frame = ttk.Frame(header_frame)
        count_frame.pack(side=tk.RIGHT)
        
        ttk.Label(count_frame, text="Total Contacts:", style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.count_label = ttk.Label(count_frame, text="0", font=('Segoe UI', 12, 'bold'),
                                     foreground=self.success_color)
        self.count_label.pack(side=tk.LEFT)
    
    def create_form_panel(self, parent):
        """Create left panel with input form"""
        form_frame = ttk.Frame(parent)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Form title
        form_title = ttk.Label(form_frame, text="Add/Edit Contact", style='Header.TLabel')
        form_title.pack(pady=(0, 15))
        
        # Create a more compact form
        fields = [
            ("Name:", "name_entry"),
            ("Surname:", "surname_entry"),
            ("ID:", "id_entry"),
            ("Phone:", "phone_entry"),
            ("Profession:", "profession_entry"),
        ]
        
        self.form_entries = {}
        
        for label_text, var_name in fields:
            field_frame = ttk.Frame(form_frame)
            field_frame.pack(fill=tk.X, pady=5)
            
            label = ttk.Label(field_frame, text=label_text, width=12)
            label.pack(side=tk.LEFT)
            
            entry = ttk.Entry(field_frame, width=25)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
            
            self.form_entries[var_name] = entry
        
        # Buttons frame
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        add_btn = tk.Button(buttons_frame, text="➕ Add Contact", bg=self.success_color,
                           fg='white', command=self.add_contact, font=('Segoe UI', 10, 'bold'),
                           padx=10, pady=8, relief=tk.FLAT, cursor="hand2")
        add_btn.pack(fill=tk.X, pady=(0, 5))
        
        update_btn = tk.Button(buttons_frame, text="✏️ Update Contact", bg=self.accent_color,
                              fg='white', command=self.update_contact, font=('Segoe UI', 10, 'bold'),
                              padx=10, pady=8, relief=tk.FLAT, cursor="hand2")
        update_btn.pack(fill=tk.X, pady=(0, 5))
        
        clear_btn = tk.Button(buttons_frame, text="🗑️ Clear Form", bg="#9E9E9E",
                             fg='white', command=self.clear_form, font=('Segoe UI', 10, 'bold'),
                             padx=10, pady=8, relief=tk.FLAT, cursor="hand2")
        clear_btn.pack(fill=tk.X)
        
        # Search section
        search_frame = ttk.LabelFrame(form_frame, text="🔍 Search", padding=10)
        search_frame.pack(fill=tk.X, pady=20)
        
        search_type_frame = ttk.Frame(search_frame)
        search_type_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_type_frame, text="Search by:").pack(side=tk.LEFT)
        self.search_type = ttk.Combobox(search_type_frame, 
                                       values=['ID', 'Name', 'Surname', 'Phone'],
                                       state='readonly', width=15)
        self.search_type.set('ID')
        self.search_type.pack(side=tk.LEFT, padx=(5, 0))
        
        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_input_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_input_frame, width=22)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        search_btn = tk.Button(search_frame, text="🔎 Find", bg=self.accent_color,
                              fg='white', command=self.search_contact, font=('Segoe UI', 9, 'bold'),
                              padx=10, pady=6, relief=tk.FLAT, cursor="hand2")
        search_btn.pack(fill=tk.X)
        
        # Sort section
        sort_frame = ttk.LabelFrame(form_frame, text="↕️ Sort", padding=10)
        sort_frame.pack(fill=tk.X, pady=20)
        
        sort_options = ['Name', 'Surname', 'ID', 'Phone', 'Profession']
        for i, option in enumerate(sort_options):
            btn = tk.Button(sort_frame, text=option, bg=self.secondary_color,
                           fg='white', command=lambda o=option: self.sort_by(o.lower()),
                           font=('Segoe UI', 9), padx=8, pady=5, relief=tk.FLAT, cursor="hand2")
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
        
        sort_frame.grid_columnconfigure(0, weight=1)
        sort_frame.grid_columnconfigure(1, weight=1)
    
    def create_list_panel(self, parent):
        """Create right panel with contact list"""
        list_frame = ttk.Frame(parent)
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # List title and controls
        list_header = ttk.Frame(list_frame)
        list_header.pack(fill=tk.X, pady=(0, 10))
        
        list_title = ttk.Label(list_header, text="📋 All Contacts", style='Header.TLabel')
        list_title.pack(side=tk.LEFT)
        
        # Refresh button
        refresh_btn = tk.Button(list_header, text="🔄 Refresh", bg=self.accent_color,
                               fg='white', command=self.refresh_contact_list, font=('Segoe UI', 9, 'bold'),
                               padx=10, pady=5, relief=tk.FLAT, cursor="hand2")
        refresh_btn.pack(side=tk.RIGHT)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('ID', 'Name', 'Surname', 'Phone', 'Profession')
        self.tree = ttk.Treeview(tree_frame, columns=columns, height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Define column headings and widths
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.W, width=50)
        self.tree.column('Name', anchor=tk.W, width=120)
        self.tree.column('Surname', anchor=tk.W, width=120)
        self.tree.column('Phone', anchor=tk.W, width=120)
        self.tree.column('Profession', anchor=tk.W, width=150)
        
        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('ID', text='ID', anchor=tk.W)
        self.tree.heading('Name', text='Name', anchor=tk.W)
        self.tree.heading('Surname', text='Surname', anchor=tk.W)
        self.tree.heading('Phone', text='Phone', anchor=tk.W)
        self.tree.heading('Profession', text='Profession', anchor=tk.W)
        
        # Configure row styles
        self.tree.tag_configure('oddrow', background='#f9f9f9')
        self.tree.tag_configure('evenrow', background='#ffffff')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click to load contact
        self.tree.bind('<Double-1>', self.load_contact_from_tree)
        
        # Context menu for delete
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Bottom buttons
        bottom_frame = ttk.Frame(list_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        delete_btn = tk.Button(bottom_frame, text="🗑️ Delete Selected", bg=self.danger_color,
                              fg='white', command=self.delete_selected, font=('Segoe UI', 10, 'bold'),
                              padx=10, pady=8, relief=tk.FLAT, cursor="hand2")
        delete_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        view_btn = tk.Button(bottom_frame, text="👁️ View Details", bg=self.accent_color,
                            fg='white', command=self.view_details, font=('Segoe UI', 10, 'bold'),
                            padx=10, pady=8, relief=tk.FLAT, cursor="hand2")
        view_btn.pack(side=tk.LEFT)
    
    def create_footer(self, parent):
        """Create footer with file operations"""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        file_frame = ttk.LabelFrame(footer_frame, text="💾 File Operations", padding=10)
        file_frame.pack(fill=tk.X)
        
        save_btn = tk.Button(file_frame, text="💾 Save to File", bg=self.success_color,
                            fg='white', command=self.save_to_file, font=('Segoe UI', 10, 'bold'),
                            padx=10, pady=8, relief=tk.FLAT, cursor="hand2")
        save_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        load_btn = tk.Button(file_frame, text="📂 Load from File", bg=self.accent_color,
                            fg='white', command=self.load_from_file, font=('Segoe UI', 10, 'bold'),
                            padx=10, pady=8, relief=tk.FLAT, cursor="hand2")
        load_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        export_btn = tk.Button(file_frame, text="📤 Export as CSV", bg=self.secondary_color,
                              fg='white', command=self.export_csv, font=('Segoe UI', 10, 'bold'),
                              padx=10, pady=8, relief=tk.FLAT, cursor="hand2")
        export_btn.pack(side=tk.LEFT)
    
    def add_contact(self):
        """Add a new contact"""
        try:
            name = self.form_entries['name_entry'].get().strip()
            surname = self.form_entries['surname_entry'].get().strip()
            id_str = self.form_entries['id_entry'].get().strip()
            phone = self.form_entries['phone_entry'].get().strip()
            profession = self.form_entries['profession_entry'].get().strip()
            
            if not all([name, surname, id_str, phone, profession]):
                messagebox.showwarning("Validation Error", "All fields must be filled!")
                return
            
            contact_id = int(id_str)
            
            if self.pb.add_contact(name, surname, contact_id, phone, profession):
                messagebox.showinfo("Success", f"Contact '{name} {surname}' added successfully!")
                self.clear_form()
                self.refresh_contact_list()
            else:
                messagebox.showerror("Error", f"Contact with ID {contact_id} already exists!")
        
        except ValueError:
            messagebox.showerror("Error", "ID must be a number!")
    
    def update_contact(self):
        """Update existing contact"""
        try:
            id_str = self.form_entries['id_entry'].get().strip()
            if not id_str:
                messagebox.showwarning("Validation Error", "Enter the ID of contact to update!")
                return
            
            contact_id = int(id_str)
            name = self.form_entries['name_entry'].get().strip() or None
            surname = self.form_entries['surname_entry'].get().strip() or None
            phone = self.form_entries['phone_entry'].get().strip() or None
            profession = self.form_entries['profession_entry'].get().strip() or None
            
            if self.pb.update_contact(contact_id, name, surname, phone, profession):
                messagebox.showinfo("Success", f"Contact ID {contact_id} updated successfully!")
                self.clear_form()
                self.refresh_contact_list()
            else:
                messagebox.showerror("Error", f"Contact with ID {contact_id} not found!")
        
        except ValueError:
            messagebox.showerror("Error", "ID must be a number!")
    
    def delete_selected(self):
        """Delete selected contact from tree"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a contact to delete!")
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        contact_id = int(values[0])
        
        if messagebox.askyesno("Confirm", f"Delete contact with ID {contact_id}?"):
            if self.pb.delete_contact(contact_id):
                messagebox.showinfo("Success", f"Contact ID {contact_id} deleted successfully!")
                self.refresh_contact_list()
                self.clear_form()
            else:
                messagebox.showerror("Error", f"Failed to delete contact!")
    
    def refresh_contact_list(self):
        """Refresh the contact list display"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add contacts
        current = self.pb.head
        index = 0
        while current:
            contact = current.contact
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(
                contact.id,
                contact.name,
                contact.surname,
                contact.phone,
                contact.profession
            ), tags=(tag,))
            current = current.next
            index += 1
        
        # Update count
        self.count_label.config(text=str(self.pb.get_count()))
    
    def load_contact_from_tree(self, event):
        """Load contact details into form when double-clicked"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        
        self.form_entries['id_entry'].delete(0, tk.END)
        self.form_entries['id_entry'].insert(0, str(values[0]))
        
        self.form_entries['name_entry'].delete(0, tk.END)
        self.form_entries['name_entry'].insert(0, values[1])
        
        self.form_entries['surname_entry'].delete(0, tk.END)
        self.form_entries['surname_entry'].insert(0, values[2])
        
        self.form_entries['phone_entry'].delete(0, tk.END)
        self.form_entries['phone_entry'].insert(0, values[3])
        
        self.form_entries['profession_entry'].delete(0, tk.END)
        self.form_entries['profession_entry'].insert(0, values[4])
    
    def view_details(self):
        """Show detailed view of selected contact"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a contact to view!")
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        
        details = f"""
ID: {values[0]}
Name: {values[1]}
Surname: {values[2]}
Phone: {values[3]}
Profession: {values[4]}
        """
        messagebox.showinfo("Contact Details", details)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        selection = self.tree.selection()
        if not selection:
            return
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="📋 View Details", command=self.view_details)
        menu.add_command(label="✏️ Edit", command=lambda: self.load_contact_from_tree(None))
        menu.add_separator()
        menu.add_command(label="🗑️ Delete", command=self.delete_selected)
        
        menu.post(event.x_root, event.y_root)
    
    def clear_form(self):
        """Clear all form fields"""
        for entry in self.form_entries.values():
            entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
    
    def search_contact(self):
        """Search for contact"""
        search_type = self.search_type.get()
        search_value = self.search_entry.get().strip()
        
        if not search_value:
            messagebox.showwarning("Warning", "Enter search value!")
            return
        
        # Clear tree first
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        results = []
        
        if search_type == 'ID':
            try:
                contact_id = int(search_value)
                node = self.pb.search_by_id(contact_id)
                if node:
                    results.append(node)
            except ValueError:
                messagebox.showerror("Error", "ID must be a number!")
                self.refresh_contact_list()
                return
        
        elif search_type == 'Name':
            results = self.pb.search_by_name(search_value)
        
        elif search_type == 'Surname':
            results = self.pb.search_by_surname(search_value)
        
        elif search_type == 'Phone':
            node = self.pb.search_by_phone(search_value)
            if node:
                results.append(node)
        
        # Display results
        if not results:
            messagebox.showinfo("Search Results", f"No contacts found!")
            self.refresh_contact_list()
            return
        
        for node in results:
            contact = node.contact
            self.tree.insert('', 'end', values=(
                contact.id,
                contact.name,
                contact.surname,
                contact.phone,
                contact.profession
            ))
        
        messagebox.showinfo("Search Results", f"Found {len(results)} contact(s)!")
    
    def sort_by(self, field):
        """Sort contacts by field"""
        sort_methods = {
            'name': self.pb.sort_by_name,
            'surname': self.pb.sort_by_surname,
            'id': self.pb.sort_by_id,
            'phone': self.pb.sort_by_phone,
            'profession': self.pb.sort_by_profession,
        }
        
        sort_methods[field]()
        self.refresh_contact_list()
        messagebox.showinfo("Success", f"Contacts sorted by {field}!")
    
    def save_to_file(self):
        """Save phone book to file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.pb.save_to_file(file_path):
                messagebox.showinfo("Success", f"Phone book saved to {os.path.basename(file_path)}!")
    
    def load_from_file(self):
        """Load phone book from file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.pb.load_from_file(file_path):
                self.refresh_contact_list()
                self.clear_form()
                messagebox.showinfo("Success", f"Phone book loaded from {os.path.basename(file_path)}!")
    
    def export_csv(self):
        """Export contacts to CSV file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    # Write header
                    f.write("ID,Name,Surname,Phone,Profession\n")
                    
                    # Write contacts
                    current = self.pb.head
                    while current:
                        contact = current.contact
                        f.write(f"{contact.id},{contact.name},{contact.surname},{contact.phone},{contact.profession}\n")
                        current = current.next
                
                messagebox.showinfo("Success", f"Contacts exported to {os.path.basename(file_path)}!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PhoneBookGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
