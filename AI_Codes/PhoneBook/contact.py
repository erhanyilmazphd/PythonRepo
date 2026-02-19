"""
Contact class for phone book entries
"""

class Contact:
    """Represents a single contact in the phone book"""
    
    def __init__(self, name, surname, contact_id, phone, profession):
        """
        Initialize a Contact object
        
        Args:
            name (str): Contact's first name
            surname (str): Contact's last name
            contact_id (int): Unique identifier for the contact
            phone (str): Phone number
            profession (str): Contact's profession
        """
        self.name = name
        self.surname = surname
        self.id = contact_id
        self.phone = phone
        self.profession = profession
    
    def __str__(self):
        """String representation of the contact"""
        return f"ID: {self.id:4} | Name: {self.name:15} | Surname: {self.surname:15} | Phone: {self.phone:15} | Profession: {self.profession}"
    
    def __repr__(self):
        """Representation of the contact"""
        return f"Contact('{self.name}', '{self.surname}', {self.id}, '{self.phone}', '{self.profession}')"
    
    def to_dict(self):
        """Convert contact to dictionary for file storage"""
        return {
            'name': self.name,
            'surname': self.surname,
            'id': self.id,
            'phone': self.phone,
            'profession': self.profession
        }
    
    @staticmethod
    def from_dict(data):
        """Create a Contact from a dictionary"""
        return Contact(
            data['name'],
            data['surname'],
            data['id'],
            data['phone'],
            data['profession']
        )
    
    def update(self, name=None, surname=None, phone=None, profession=None):
        """Update contact information"""
        if name:
            self.name = name
        if surname:
            self.surname = surname
        if phone:
            self.phone = phone
        if profession:
            self.profession = profession
