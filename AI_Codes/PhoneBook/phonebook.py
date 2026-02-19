"""
PhoneBook class implementing doubly-linked list operations
"""

import json
from node import Node
from contact import Contact

class PhoneBook:
    """Doubly-linked list based phone book"""
    
    def __init__(self):
        """Initialize an empty phone book"""
        self.head = None
        self.tail = None
        self.count = 0
    
    def add_contact(self, name, surname, contact_id, phone, profession):
        """
        Add a contact to the phone book (append to end)
        
        Args:
            name (str): Contact's first name
            surname (str): Contact's last name
            contact_id (int): Unique identifier
            phone (str): Phone number
            profession (str): Contact's profession
        
        Returns:
            bool: True if successful, False if ID already exists
        """
        # Check if ID already exists
        if self.search_by_id(contact_id):
            print(f"Error: Contact with ID {contact_id} already exists!")
            return False
        
        contact = Contact(name, surname, contact_id, phone, profession)
        new_node = Node(contact)
        
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self.count += 1
        return True
    
    def insert_contact(self, position, name, surname, contact_id, phone, profession):
        """
        Insert a contact at a specific position (0-indexed)
        
        Args:
            position (int): Position to insert (0 = beginning)
            name (str): Contact's first name
            surname (str): Contact's last name
            contact_id (int): Unique identifier
            phone (str): Phone number
            profession (str): Contact's profession
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if ID already exists
        if self.search_by_id(contact_id):
            print(f"Error: Contact with ID {contact_id} already exists!")
            return False
        
        if position < 0 or position > self.count:
            print(f"Error: Position must be between 0 and {self.count}")
            return False
        
        contact = Contact(name, surname, contact_id, phone, profession)
        new_node = Node(contact)
        
        if position == 0:
            # Insert at beginning
            if self.head is None:
                self.head = self.tail = new_node
            else:
                new_node.next = self.head
                self.head.prev = new_node
                self.head = new_node
        elif position == self.count:
            # Insert at end (same as add)
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        else:
            # Insert in middle
            node = self._get_node_at(position)
            new_node.next = node
            new_node.prev = node.prev
            node.prev.next = new_node
            node.prev = new_node
        
        self.count += 1
        return True
    
    def delete_contact(self, contact_id):
        """
        Delete a contact by ID
        
        Args:
            contact_id (int): ID of the contact to delete
        
        Returns:
            bool: True if deleted successfully, False if not found
        """
        node = self.search_by_id(contact_id)
        if node is None:
            print(f"Error: Contact with ID {contact_id} not found!")
            return False
        
        # If it's the only node
        if node == self.head and node == self.tail:
            self.head = self.tail = None
        # If it's the head
        elif node == self.head:
            self.head = node.next
            self.head.prev = None
        # If it's the tail
        elif node == self.tail:
            self.tail = node.prev
            self.tail.next = None
        # If it's in the middle
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        
        self.count -= 1
        return True
    
    def list_contacts(self):
        """
        List/Print all contacts in the phone book
        """
        if self.head is None:
            print("\nPhone book is empty!")
            return
        
        print("\n" + "="*90)
        print(f"Phone Book ({self.count} contacts)")
        print("="*90)
        
        current = self.head
        index = 0
        while current:
            print(f"{index+1:3}. {current.contact}")
            current = current.next
            index += 1
        
        print("="*90 + "\n")
    
    def search_by_id(self, contact_id):
        """
        Search for a contact by ID
        
        Args:
            contact_id (int): ID to search for
        
        Returns:
            Node: Node containing the contact, or None if not found
        """
        current = self.head
        while current:
            if current.contact.id == contact_id:
                return current
            current = current.next
        return None
    
    def search_by_name(self, name):
        """
        Search for contacts by name (case-insensitive)
        
        Args:
            name (str): Name to search for
        
        Returns:
            list: List of nodes matching the name
        """
        results = []
        current = self.head
        while current:
            if current.contact.name.lower() == name.lower():
                results.append(current)
            current = current.next
        return results
    
    def search_by_surname(self, surname):
        """
        Search for contacts by surname (case-insensitive)
        
        Args:
            surname (str): Surname to search for
        
        Returns:
            list: List of nodes matching the surname
        """
        results = []
        current = self.head
        while current:
            if current.contact.surname.lower() == surname.lower():
                results.append(current)
            current = current.next
        return results
    
    def search_by_phone(self, phone):
        """
        Search for a contact by phone number
        
        Args:
            phone (str): Phone number to search for
        
        Returns:
            Node: Node containing the contact, or None if not found
        """
        current = self.head
        while current:
            if current.contact.phone == phone:
                return current
            current = current.next
        return None
    
    def sort_by_name(self):
        """
        Sort phone book by first name (A to Z)
        Uses bubble sort with doubly-linked list
        """
        if self.count <= 1:
            return
        
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            
            while current and current.next:
                if current.contact.name.lower() > current.next.contact.name.lower():
                    # Swap contacts
                    current.contact, current.next.contact = current.next.contact, current.contact
                    swapped = True
                current = current.next
    
    def sort_by_surname(self):
        """
        Sort phone book by surname (A to Z)
        Uses bubble sort with doubly-linked list
        """
        if self.count <= 1:
            return
        
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            
            while current and current.next:
                if current.contact.surname.lower() > current.next.contact.surname.lower():
                    # Swap contacts
                    current.contact, current.next.contact = current.next.contact, current.contact
                    swapped = True
                current = current.next
    
    def sort_by_id(self):
        """
        Sort phone book by ID (ascending)
        Uses bubble sort with doubly-linked list
        """
        if self.count <= 1:
            return
        
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            
            while current and current.next:
                if current.contact.id > current.next.contact.id:
                    # Swap contacts
                    current.contact, current.next.contact = current.next.contact, current.contact
                    swapped = True
                current = current.next
    
    def sort_by_phone(self):
        """
        Sort phone book by phone number
        Uses bubble sort with doubly-linked list
        """
        if self.count <= 1:
            return
        
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            
            while current and current.next:
                if current.contact.phone > current.next.contact.phone:
                    # Swap contacts
                    current.contact, current.next.contact = current.next.contact, current.contact
                    swapped = True
                current = current.next
    
    def sort_by_profession(self):
        """
        Sort phone book by profession (A to Z)
        Uses bubble sort with doubly-linked list
        """
        if self.count <= 1:
            return
        
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            
            while current and current.next:
                if current.contact.profession.lower() > current.next.contact.profession.lower():
                    # Swap contacts
                    current.contact, current.next.contact = current.next.contact, current.contact
                    swapped = True
                current = current.next
    
    def update_contact(self, contact_id, name=None, surname=None, phone=None, profession=None):
        """
        Update contact information
        
        Args:
            contact_id (int): ID of contact to update
            name (str, optional): New name
            surname (str, optional): New surname
            phone (str, optional): New phone number
            profession (str, optional): New profession
        
        Returns:
            bool: True if updated successfully, False if not found
        """
        node = self.search_by_id(contact_id)
        if node is None:
            print(f"Error: Contact with ID {contact_id} not found!")
            return False
        
        node.contact.update(name, surname, phone, profession)
        return True
    
    def save_to_file(self, filename='phonebook.json'):
        """
        Save phone book to a JSON file
        
        Args:
            filename (str): Name of the file to save to
        
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            contacts = []
            current = self.head
            while current:
                contacts.append(current.contact.to_dict())
                current = current.next
            
            with open(filename, 'w') as f:
                json.dump(contacts, f, indent=4)
            
            print(f"Phone book saved to {filename} successfully!")
            return True
        except Exception as e:
            print(f"Error saving phone book: {e}")
            return False
    
    def load_from_file(self, filename='phonebook.json'):
        """
        Load phone book from a JSON file
        Clears existing contacts before loading
        
        Args:
            filename (str): Name of the file to load from
        
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        try:
            with open(filename, 'r') as f:
                contacts = json.load(f)
            
            # Clear existing contacts
            self.head = None
            self.tail = None
            self.count = 0
            
            # Add loaded contacts
            for contact_data in contacts:
                contact = Contact.from_dict(contact_data)
                self.add_contact(
                    contact.name,
                    contact.surname,
                    contact.id,
                    contact.phone,
                    contact.profession
                )
            
            print(f"Phone book loaded from {filename} successfully! ({self.count} contacts)")
            return True
        except FileNotFoundError:
            print(f"Error: File {filename} not found!")
            return False
        except Exception as e:
            print(f"Error loading phone book: {e}")
            return False
    
    def _get_node_at(self, position):
        """
        Get node at a specific position (helper method)
        
        Args:
            position (int): Position (0-indexed)
        
        Returns:
            Node: Node at the position
        """
        current = self.head
        for _ in range(position):
            current = current.next
        return current
    
    def is_empty(self):
        """Check if phone book is empty"""
        return self.count == 0
    
    def get_count(self):
        """Get the number of contacts"""
        return self.count
