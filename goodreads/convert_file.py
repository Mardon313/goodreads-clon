# convert_file.py
with open('fayl.txt', encoding='cp1251') as f:
    text = f.read()

text_utf8 = text.encode('utf-8', errors='ignore').decode('utf-8')

# Tekshirish uchun faylga yozib qo‘yish
with open('fayl_utf8.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(text_utf8)
