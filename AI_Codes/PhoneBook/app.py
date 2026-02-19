"""
Phone Book Web Application
Flask-based web application for Phone Book management
"""

from flask import Flask, render_template, request, jsonify
from phonebook import PhoneBook
import json
import os

app = Flask(__name__)
pb = PhoneBook()

# Load existing data
if os.path.exists('phonebook.json'):
    pb.load_from_file('phonebook.json')

def contacts_to_list():
    """Convert phonebook to list format"""
    contacts = []
    current = pb.head
    while current:
        contact = current.contact
        contacts.append({
            'id': contact.id,
            'name': contact.name,
            'surname': contact.surname,
            'phone': contact.phone,
            'profession': contact.profession
        })
        current = current.next
    return contacts

@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Get all contacts"""
    return jsonify({'contacts': contacts_to_list(), 'count': pb.get_count()})

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    """Add new contact"""
    data = request.json
    
    if not all([data.get('name'), data.get('surname'), data.get('id'), 
                data.get('phone'), data.get('profession')]):
        return jsonify({'success': False, 'message': 'All fields required'}), 400
    
    try:
        contact_id = int(data.get('id'))
        success = pb.add_contact(
            data.get('name'),
            data.get('surname'),
            contact_id,
            data.get('phone'),
            data.get('profession')
        )
        
        if success:
            pb.save_to_file('phonebook.json')
            return jsonify({'success': True, 'message': 'Contact added', 
                          'contacts': contacts_to_list()})
        else:
            return jsonify({'success': False, 'message': f'ID {contact_id} already exists'}), 400
    except ValueError:
        return jsonify({'success': False, 'message': 'ID must be a number'}), 400

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """Update contact"""
    data = request.json
    
    success = pb.update_contact(
        contact_id,
        data.get('name'),
        data.get('surname'),
        data.get('phone'),
        data.get('profession')
    )
    
    if success:
        pb.save_to_file('phonebook.json')
        return jsonify({'success': True, 'message': 'Contact updated',
                       'contacts': contacts_to_list()})
    else:
        return jsonify({'success': False, 'message': 'Contact not found'}), 404

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Delete contact"""
    success = pb.delete_contact(contact_id)
    
    if success:
        pb.save_to_file('phonebook.json')
        return jsonify({'success': True, 'message': 'Contact deleted',
                       'contacts': contacts_to_list()})
    else:
        return jsonify({'success': False, 'message': 'Contact not found'}), 404

@app.route('/api/search', methods=['POST'])
def search():
    """Search contacts"""
    data = request.json
    search_type = data.get('type')
    search_value = data.get('value')
    
    results = []
    
    if search_type == 'id':
        try:
            node = pb.search_by_id(int(search_value))
            if node:
                results.append({
                    'id': node.contact.id,
                    'name': node.contact.name,
                    'surname': node.contact.surname,
                    'phone': node.contact.phone,
                    'profession': node.contact.profession
                })
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid ID'}), 400
    
    elif search_type == 'name':
        nodes = pb.search_by_name(search_value)
        for node in nodes:
            results.append({
                'id': node.contact.id,
                'name': node.contact.name,
                'surname': node.contact.surname,
                'phone': node.contact.phone,
                'profession': node.contact.profession
            })
    
    elif search_type == 'surname':
        nodes = pb.search_by_surname(search_value)
        for node in nodes:
            results.append({
                'id': node.contact.id,
                'name': node.contact.name,
                'surname': node.contact.surname,
                'phone': node.contact.phone,
                'profession': node.contact.profession
            })
    
    elif search_type == 'phone':
        node = pb.search_by_phone(search_value)
        if node:
            results.append({
                'id': node.contact.id,
                'name': node.contact.name,
                'surname': node.contact.surname,
                'phone': node.contact.phone,
                'profession': node.contact.profession
            })
    
    return jsonify({'success': True, 'results': results, 'count': len(results)})

@app.route('/api/sort/<sort_by>', methods=['GET'])
def sort_contacts(sort_by):
    """Sort contacts"""
    sort_methods = {
        'name': pb.sort_by_name,
        'surname': pb.sort_by_surname,
        'id': pb.sort_by_id,
        'phone': pb.sort_by_phone,
        'profession': pb.sort_by_profession,
    }
    
    if sort_by in sort_methods:
        sort_methods[sort_by]()
        pb.save_to_file('phonebook.json')
        return jsonify({'success': True, 'contacts': contacts_to_list()})
    
    return jsonify({'success': False, 'message': 'Invalid sort option'}), 400

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export as CSV"""
    try:
        csv_data = "ID,Name,Surname,Phone,Profession\n"
        current = pb.head
        while current:
            c = current.contact
            csv_data += f"{c.id},{c.name},{c.surname},{c.phone},{c.profession}\n"
            current = current.next
        
        return jsonify({
            'success': True,
            'csv': csv_data,
            'filename': 'phonebook.csv'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("📱 Phone Book Web Application")
    print("="*60)
    print("\n🌐 Opening in your browser...")
    print("📍 URL: http://127.0.0.1:5000")
    print("\n✅ Application running!")
    print("Press Ctrl+C to stop\n")
    
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000')
    
    app.run(debug=True, use_reloader=False)
