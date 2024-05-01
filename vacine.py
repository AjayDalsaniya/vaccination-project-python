from datetime import date
from datetime import datetime,timedelta
import time
from time import strftime
from fpdf import FPDF
import pymysql
import qrcode as qr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

"""named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)"""
#time
time1 =strftime("%I : %M : %S")
print(time1)

#vacine dose date 
presentday  = datetime.now()
dose_Date = presentday + timedelta(90)

print('Today : ',presentday.strftime('%d-%m-%y'))
print("Dose Date  : ",dose_Date.strftime('%d-%m-%y'))

#d = (date.today())
d = (presentday.strftime('%d-%m-%y'))
d1= str(d)



print(d1)
#file name 
filen = d1+".txt"
filep = d1+".pdf"

f = open(filen,"a")

status = True
while status:
    f.write("\n")
    menu = """   
                Vaccination
                ____________
                               
    """
    
    f.write(menu)
    f.write("Date & Time : "+str(presentday.strftime('%d-%m-%y')) +" "+str(time1) +"\n")
   
    name = input("Enter Your Name : ")
    fpname = "PDF\\"+name + " Vaccine Report.pdf"
    
    qrname = name + "Vacine QRCODE.png"

    f.write("\n")
    f.write("Name : "+ name)

    email = input("Enter your Email : ")
    list1=email.split()
    f.write("\nEmail : "+email)

    Age = input("Enter your Age : ")
    f.write("\nAge : "+str(Age))
    
    Gender = input("Your Gender : ")
    f.write("\nGender : "+Gender)
    
    
    phone = input("Enter phone Number : ")
    f.write("\nPhone Number : "+phone)
    
    address = input("Enter Address : ")
    f.write("\nAddress : "+address)
    
    vaccine = input("Enter Vaccine Name : ")
    f.write("\nvaccine Name : "+vaccine)
    
    vaccine_dose = input("Enter Vaccine Dose : ")
    f.write("\nVaccine Dose : "+vaccine_dose)
    
    
    if vaccine_dose == '1' :
        f.write("\n You should take the second does on this date " +str(dose_Date.strftime('%d-%m-%y')))
        
    f.write("\n------------ \n")
    
    #Qr Code
    qrdata =f'Name : {name}\nEmail : {email}\nAge : {Age}\nGender : {Gender}\nPhone Number : {phone}\nAddress : {address}\nVacine Name : {vaccine}\n vacine Dose : {vaccine_dose}\n Date : {d1}'
    
    img =qr.make(qrdata)

    img.save("QR-CODE\\" +qrname)
    
    
    #pdf code
    page=FPDF()#object
    page.add_page()
    page.set_font('Arial','B',20)
    
    page.image("img/logo2.png",0,10,200)
    page.cell(0,90," ",0,1)
    
    page.set_text_color(9,121,105)
    page.cell(0,10,"Vaccination Report ",0,1,'C')
    
    page.cell(0,10," ",0,1)
    page.set_text_color(0,0,0)
    page.set_font('Arial','',16)
    page.cell(20,10,"Date & Time : "+ str(presentday.strftime('%d-%m-%y')) + " "+str(time1)  ,0)

    page.cell(0,10," ",0,1)
    page.cell(20,10,"Name : "+name  ,0)

   
    page.cell(0,10," ",0,1)
    page.cell(20,10,"Email : "+email  ,0)

    page.cell(0,10," ",0,1)
    page.cell(20,10,"Age : "+Age  ,0)

    page.cell(0,10," ",0,1)
    page.cell(20,10,"Gender : "+Gender  ,0)

    page.cell(0,10," ",0,1)
    page.cell(20,10,"Phone Number : "+phone  ,0)

    page.cell(0,10," ",0,1)
    page.cell(20,10,"Address : "+address  ,0)

    page.cell(0,10," ",0,1)
    page.cell(20,10,"Vaccine Name : "+vaccine  ,0)

    page.cell(0,10," ",0,1)
    page.cell(20,10,"Vaccine Dose : "+vaccine_dose  ,0)
    
    page.cell(0,10," ",0,1)
    if vaccine_dose == '1' :
        page.cell(20,10,"You should take the second does on this date "+str(dose_Date.strftime('%d-%m-%y')),0)
     
    page.cell(0,10," ",0,1)
    page.image('img/logo3.png',10,220,190)
    
    
    page.cell(0,10," ",0,1)
    page.image("QR-CODE//"+qrname,125,225,70)
    
    page.output(fpname,'F')

    #fpname = "PDF\\"+name + " Vaccine Report.pdf"
    
    sender_email = "abpatel0421@gmail.com"
    
    rec_email = list1
    f1 = "PDF//"+ name + " Vaccine Report.pdf"
    #password = input(str("please enter your password : "))
    password =str("iavr livu soti qslo")
   
    subject = "new email from tie attachment"
    def send_emails(rec_email):
        for person in rec_email:

            body = """
                       Certificate for COVID-19 Vaccination
                        
                    """
            msg = MIMEMultipart()
            msg['from'] = sender_email
            msg['to'] =person
            msg['subject'] = subject

            
            msg.attach(MIMEText(body,'plain'))


            filename = f1
            
            attachment = open(filename,'rb')
            attachment_package = MIMEBase('application','octet-stream')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition','attachment', filename=filename)
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
    #database
    conn = pymysql.connect(host="localhost",user="root",password="",port=3306,database="vacine")
    cur= conn.cursor()
        
    data = "insert into  v_details(name,email,age,gender,phone_number,address,vacine_name,vacine_dose,date) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
    args=(name,email,Age,Gender,phone,address,vaccine,vaccine_dose,d1)
    cur.execute(data%args)
        
    conn.commit()
    
    
   
        
    choice = input("Do you Wanto add vaccine yes or no : ")
    if choice == "y" or choice == "Y":
        
        
        status = True
        
    else:
        cur.execute("select * from v_details")
        
        result = cur.fetchall()
        for i in result:
            print()
            print("-------------------")
            print("name",i[1])
            print("email",i[2])
            print("age",i[3])
            print("gender",i[4])
            print("phone number",i[5])
            print("address",i[6])
            print("vacine name",i[7])
            print("vacine dose",i[8])
            print("vacine date",i[9])
            print()
            print("-------------------")
            print()
            
        
        conn.commit()
        status = False
        
        
        
    
    

#pdf code


f.close()
