import json

data = '''[
{
    "name": "Erhan",
    "surname": "YILMAZ",
    "phone": {
        "type": "intl",
        "number": "+905331111111"
    },
    "email": {
        "hide": "yes"
    }
}, 
{
    "name": "Ahmet",
    "surname": "YILMAZ",
    "phone": {
        "type": "intl",
        "number": "+905221111111"
    },
    "email": {
        "hide": "yes"
    }
}
]'''

info = json.loads(data)  # info becomes a LIST with 2 elements each a dictionary

print('User Count:', len(info))
print('---------------------------')
for item in info:
    print('Name:', item["name"], item["surname"])
    print('Phone:', item["phone"]["number"], '\n\t\t', 'type:', item["phone"]["type"])
    print('Attr:', item["email"]["hide"])
    print('---------------------------')