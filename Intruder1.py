

import RPi.GPIO as GPIO
import time, datetime
import pygame, sys
from pygame.locals import *
import pygame.camera
import MySQLdb
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

dateString = '%Y-%m-%d %H-%M-%S'
pir=7
buz=10

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pir,GPIO.IN)
GPIO.setup(buz,GPIO.OUT)

GPIO.output(buz,GPIO.LOW)
time.sleep(5) #SETTING UP THE SENSOR
print("PROGRAM IS CURRENTLY RUNNING.")

while True:
    x=GPIO.input(pir)
    if x==1:
	GPIO.output(buz,GPIO.HIGH)
	print("ALERT!!!INTRUSION DETECTED at detectionlogs")
	#This is where the date and time variables are initialised and printed with variable name z
	z= datetime.datetime.now().strftime(dateString)
	print z 
	#This is the camera section, here the camera gets called from /dev/video0 and saves the picture to Intruder_Images
	pygame.init() 
        pygame.camera.init()
        cam = pygame.camera.Camera("/dev/video0",(1280,720))
        cam.start()
        image= cam.get_image()
        pygame.image.save(image,'Intruder_Images/%s.png'%str(z))
        cam.stop()
		
	#This is where the Intruder_Images folder links up with the MySQL database
	path='Intruder_Images/'+str(z)+'.png' 
	
	#Login credentials for database and database name 
        db=MySQLdb.connect("localhost","root","","intrudersdatabase")
        curs=db.cursor()
        with db:
            curs.execute("""INSERT into detectionlogs values (%s,%s)""",(z,path))
            db.commit()
        print("Data Saved to Database and Uploaded To Webpage Successfully")
	#This is where the emails get sent. The emails are sent from the configured Raspberry Pi email to the users email.
	fromaddr = "projectraspberrypii@gmail.com" 
	toaddr = "gavinfennelly@hotmail.com"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
        msg['Subject'] = "!!ATTENTION!! Activity Detected At Household!"
	body = "Please see Image attached of possible Intruder or View Website @ "+str(z)
	msg.attach(MIMEText(body, 'plain'))
	filename = str(z)+".png"
	attachment = open('Intruder_Images/%s.png'%str(z), "rb")
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	msg.attach(part)
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "test1234!")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	print("ACTIVITY DETECTED IN AREA! CHECK E-MAIL OR WEBSITE FOR IMAGES OF ACTIVITY")
	GPIO.output(buz,GPIO.LOW)
