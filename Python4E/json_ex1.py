import json

data = '''{
"name": "Erhan",
"surname": "YILMAZ",
"phone": {
    "type": "intl",
    "number": "+905331111111"
},
"email": {
    "hide": "yes"
}
}'''

info = json.loads(data)  # info is a dictionary

print('Name:', info["name"], info["surname"])
print('Phone:', info["phone"]["number"], '\n\t\t', 'type:', info["phone"]["type"])
print('Attr:', info["email"]["hide"])
