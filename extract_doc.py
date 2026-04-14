import zipfile
import xml.etree.ElementTree as ET
import re
import sys

docx_path = r'D:\杨红\梅溪湖小初高贯通培养 2026 暑假招生简章(1).docx'

with zipfile.ZipFile(docx_path, 'r') as z:
    with z.open('word/document.xml') as f:
        content = f.read().decode('utf-8')
        
root = ET.fromstring(content)

texts = []
for elem in root.iter():
    if elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t':
        if elem.text:
            texts.append(elem.text)
    elif elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
        texts.append('\n')

full_text = ''.join(texts)
full_text = re.sub(r'\n{3,}', '\n\n', full_text)
print(full_text)
