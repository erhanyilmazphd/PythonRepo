import xml.etree.ElementTree as ET

data = '''<person>
    <name> Erhan </name>
    <phone type="intl">+905331111111 </phone>
    <email hide="yes"/>     
</person>'''

tree = ET.fromstring(data)

print('Name:', tree.find('name').text)
print('Phone:', tree.find('phone').text, 'type:', tree.find('phone').get("type"))
print('Attr:', tree.find('email').get("hide"))