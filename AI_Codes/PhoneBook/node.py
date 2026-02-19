"""
Node class for doubly-linked list
"""

from contact import Contact

class Node:
    """Represents a node in the doubly-linked list"""
    
    def __init__(self, contact):
        """
        Initialize a Node
        
        Args:
            contact (Contact): Contact object to store in the node
        """
        self.contact = contact
        self.next = None
        self.prev = None
    
    def __str__(self):
        return str(self.contact)
