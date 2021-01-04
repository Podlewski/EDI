import html2text
#concatenate_text
file = open('ul.html').read()
txt = html2text.html2text(file)

file = open('ul.txt', 'w', encoding='utf-8')
file.write(txt)

file.close()
