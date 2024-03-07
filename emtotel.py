import imaplib
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re
import requests
import time
import os
path = "path"
TOKEN = 'TOKEN'
chat_id = "chat_id"
chat_id = {'chat_id' : chat_id}
mail_pass = "mail_pass"
username = "username"
imap_server = "imap_server"
mail_from = "mail_from"
i = 1
while i < 2:
    
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, mail_pass)
    inbox = imap.select("INBOX")
    status, mail_id = imap.search(None, "UNSEEN", 'From', mail_from)  # "UNSEEN", 
    idm = mail_id[0] # Получаем сроку номеров писем
    print(idm)
    id_list = idm.split() # Разделяем ID писем
    if id_list == []:
        print("Нет новых писем")
    else:
        print(id_list)
        id_list = idm.split()
        latest_email_id = id_list[-1] # Берем последний ID
        print(latest_email_id)
        _, data = imap.fetch(latest_email_id, "(RFC822)")# Получаем тело письма (RFC822) для данного ID
        # print(data)
        # print(data[0][1])
        msg = email.message_from_bytes(data[0][1])
        subject = email.header.decode_header(msg["Subject"])[0][0]
        print(f"Непрочитанное сообщение с темой: {subject}")
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                filename = part.get_filename()
                if filename:
                    # Нам плохого не надо, в письме может быть всякое барахло
                    with open(path+part.get_filename(), 'wb') as new_file:
                        new_file.write(part.get_payload(decode=True))
                        files = {'photo': open(path+part.get_filename(), 'rb')}
                        
                        url = "https://api.telegram.org/bot"+TOKEN+"/sendPhoto"
                        print(url)
                        r = requests.post(url, files=files, data=chat_id)
                        print(r.json()) # Эта строка отсылает сообщение
                        os.remove(path+part.get_filename())

        else:    
            body = msg.get_payload(decode=True).decode('utf-8')
           
    data = []
    imap.close()   
    time.sleep(15)
