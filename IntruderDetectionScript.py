# Autor:   Gavin Fennelly
# College: Waterford Institute of Technology
# Course:  Applied Computing

import RPi.GPIO as GPIO #Enables script to access GPIO Pins
from pygame.locals import * 
import pygame.camera #Python library used to take and store images
import MySQLdb #Imports the MySQL DB
import time, datetime #Enables script to access date-time function below
import pygame, sys

#These are the email libraries for Python needed to end them.
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

#Date format which will be used when saving images
dateString = '%Y-%m-%d %H-%M-%S'

#GPIO Pins which are in use for both components
pir=7
buz=10

#Board numbering system, GPIO pins will go by numbers printed on the board
GPIO.setmode(GPIO.BOARD)

#Configuring sensors to detection signals from buzzer and PIR sensor

#Buzzer (
GPIO.setup(buz,GPIO.OUT)
GPIO.output(buz,GPIO.LOW)

#PIR Sensor
GPIO.setup(pir,GPIO.IN)

print("PROGRAM IS CURRENTLY RUNNING.")

#All functioning code is contained in while loop, allowing code to run continuously until program is shut down via CMD. 
while True:
    x=GPIO.input(pir)
    if x==1:
	
	#Buzzer goes to high when motion detect, emits tone
	GPIO.output(buz,GPIO.HIGH)

	#This is where the date and time variables are initialised and printed with variable name x
	x = datetime.datetime.now().strftime(dateString)
	
	#Prints variable x
	print x 
	
	#This is the camera section, here the camera gets called from /dev/video0 and saves the picture to Intruder_Image_Logs in the /var/www/html folder on the Raspberry Pi
	
	#Initializes and selects web-cam in which to use
	pygame.init() 
        pygame.camera.init()
        cam = pygame.camera.Camera("/dev/video0",(640,480))
		
	#Starts web-cam and takes image, saving it to the specified folder
        cam.start()
        image= cam.get_image()
        pygame.image.save(image,'Intruder_Image_Logs/%s.png' %str(z))
        cam.stop()
		
	#This is where the Intruder_Images folder links up with the MySQL database
	path='Intruder_Image_Logs/'+str(z)+'.png' 
	
	#Login credentials for database and database name 
        db=MySQLdb.connect("localhost","root","","intrudersdatabase")
        curs=db.cursor()
        with db:
            curs.execute("""INSERT into detectionlogs values (%s,%s)""",(z,path))
            db.commit()
        print("Data Saved to Database and Uploaded To Webpage Successfully")
		
		#Once picture is taken, this will tell the buzzer to stop emitting a tone
		GPIO.output(buz,GPIO.LOW)
		
	
	#This is where the emails get sent. The emails are sent from the configured Raspberry Pi email to the users email.
	fromaddr = "projectraspberrypii@gmail.com" 
	toaddr = "gavinfennelly@hotmail.com"
	#Creates the container (outer) email message
	msg = MIMEMultipart()
	
	# From is the sender's email address
	# To is the recipient's email address
	# basic message headers
	msg['From'] = fromaddr
	msg['To'] = toaddr
    msg['Subject'] = "!!ATTENTION!! Activity Detected At Household!"
	body = "Please see Image attached of possible Intruder or View Website @ "+str(z)
	
	# Record the MIME types of both parts - text/plain.
	msg.attach(MIMEText(body, 'plain'))
	filename = str(z)+".png"
	
	# List of attachments
	attachment = open('Intruder_Image_Logs/%s.png'%str(z) "rb")
	
	#"application/octet-stream" is a binary file used that can be opened by applications
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	msg.attach(part)
	
	# Send the message through our own SMTP server
	s = smtplib.SMTP('smtp.gmail.com', 587)
	
	#TLS will protect users password
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(fromaddr, "test1234!")
	text = msg.as_string()
	s.sendmail(fromaddr, toaddr, text)
	s.quit()
	print("ACTIVITY DETECTED IN AREA! CHECK E-MAIL OR WEBSITE FOR IMAGES OF ACTIVITY")
	
