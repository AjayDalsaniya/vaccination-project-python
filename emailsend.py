import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

sender_email = "abpatel0421@gmail.com"
rec_email = ["ajaydalsaniya99794@gmail.com"]

#password = input(str("please enter your password : "))
password =str("iavr livu soti qslo")
subject = "new email from tie attachment"
"""
server = smtplib.SMTP('smtp.gmail.com',587)
server.ehlo()
server.starttls()
server.login(sender_email,password)
print("login success ")
server.sendmail(sender_email,rec_email,message)
print("email has been send to ",rec_email)
"""
   

def send_emails(rec_email):
    for person in rec_email:

        body = """
                    1
                    2
                    3
                    
                """
        msg = MIMEMultipart()
        msg['from'] = sender_email
        msg['to'] =person
        msg['subject'] = subject

       
        msg.attach(MIMEText(body,'plain'))


        filename = "PDF//A Vaccine Report.pdf"
    
        attachment = open(filename,'rb')
        attachment_package = MIMEBase('application','octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition','attachment', filename='A Vaccine Report.pdf')
        msg.attach(attachment_package)
    
        text =msg.as_string()
    
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(sender_email,password)
        print("login success ")

        print(f"sending email to :{person}...")           
        server.sendmail(sender_email,person,text)
        print("email has been send to {person}")
        print()
        server.quit()
    
send_emails(rec_email)