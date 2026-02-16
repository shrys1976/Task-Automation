from cgitb import text
import html
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
now  = datetime.datetime.now()
import smtplib

import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")



# email content placeholder
content = ''


def extract_news(url):
    print("Extracting Hacker news stories...")
    cnt = ''
    cnt +=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content  = response.content

    soup = BeautifulSoup(content,'html.parser')
    for i, tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):

        cnt+=((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text != 'More' else '')
    return (cnt)    

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content +=('<br>---------------<br>')
content +=('<br><br>End of message')


print("Composing Email...")

SERVER = 'smtp.gmail.com' # smtp server address for gmail 
FROM = EMAIL_USER
TO = EMAIL_USER
PASS =EMAIL_PASS
PORT =  587


msg = MIMEMultipart()
msg['Subject'] = 'Top News Stories HN [Automated Email]'+ ' ' + str(now.day) + '-' + str(now.month) + '-' +str(now.year)


msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content,'html'))


server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())
print("Email sent.")
server.quit()




