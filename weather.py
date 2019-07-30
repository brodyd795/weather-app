from urllib import request
from bs4 import BeautifulSoup
import smtplib

def getConditions():
    url = "https://www.weather-forecast.com/locations/Ames-1/forecasts/latest"
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    conditions = []
    counter = 0

    trTag = soup.find_all("tr", {"class": "b-forecast__table-summary"})
    for tag in trTag:
        divTag = tag.find_all("div", {"class": "b-forecast__text-limit"})
        for newtag in divTag:
            conditions.append(newtag.text)
    today_conditions = conditions[1:4]
    today_conditions = ' '.join(today_conditions)
    return(today_conditions)


def sendemail(from_addr,
              to_addr,
              subject,
              message,
              login,
              password):
        smtpserver = 'smtp.gmail.com:587'
        header = 'From: %s\n' % from_addr
        header += 'To: %s\n' % to_addr
        header += 'Subject: %s\n\n' % subject
        message = header + message

        server = smtplib.SMTP(smtpserver)
        server.starttls()
        server.login(login, password)
        problems = server.sendmail(from_addr, to_addr, message)
        server.quit()
        

def job():
    data = getConditions()
    
    with open('/home/pi/Desktop/weather/secrets.txt', 'r') as f:
        lines = f.readlines()
        sender_addr = lines[0].rstrip()
        passwd = lines[1].rstrip()
        recipient_addr = lines[2].rstrip()
    f.close()
    
    if 'rain' in data:
        description = "Hey, Brody! It may rain today in Ames!"
        sendemail(sender_addr, recipient_addr, "Today's Weather - Alert", description, sender_addr, passwd)
    elif 'snow' in data:
        description = "Hey, Brody! It may snow today in Ames!"
        sendemail(sender_addr, recipient_addr, "Today's Weather - Alert", description, sender_addr, passwd)
    else:
        print("nope")
        
job()
