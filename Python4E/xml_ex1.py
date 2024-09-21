import xml.etree.ElementTree as ET

inp = '''<stuff>
    <users>
        <user x="2">
            <id>001</id>
            <name>Erhan</name>
        </user>
        <user x="7">
            <id>009</id>
            <name>Ahmet</name>
        </user>
    </users> 
</stuff>'''

stuff = ET.fromstring(inp)
lst = stuff.findall('users/user')
print('User Count:', len(lst))

for item in lst:
    print('Name:', item.find('name').text)
    print('Id:', item.find('id').text)
    print('Attribute:', item.get("x"))