# Creator - Lissan Koirala
# Date - 07/28/2020

import os # To perform operating system's tasks
import cv2 # To work with images
import numpy as np # To work with images, etc
from tkinter import * # For the terms and conditions widget
# To send emails
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase  
from email import encoders
import smtplib


def main():
	try:
		os.mkdir("output_files")  # Tries creating a folder
	except:
		pass # If fails means then it already exists so pass
	# Video Capture 
	capture = cv2.VideoCapture(0) # Captures video from your first webcam, it you want to change it change the number from 0 to ?

	fgbg = cv2.createBackgroundSubtractorMOG2(50, 200, True) # This threashold is best to capture enough movemt
	# We don't want to capture small pixles of movemnt caused by air

	# Keeps track of what frame we're on
	frameCount = 0

	# Initializes a video capture
	fourcc = cv2.VideoWriter_fourcc(*'XVID') 
	numfiles = len(next(os.walk("output_files"))[2]) 
	output = cv2.VideoWriter("output_files/"+str(numfiles) + ".avi", fourcc, 30.0, (int(capture.get(3)), int(capture.get(4))))

	while(1):
		# Return Value and the current frame
		ret, frame = capture.read()

		#  Check if a current frame actually exist
		if not ret:
			break
		
		# Adds the frame count 
		frameCount += 1
		# Resize the frame
		resizedFrame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

		# Get the foreground mask
		motion = fgbg.apply(resizedFrame)

		# Count all the non zero pixels within the mask
		count = np.count_nonzero(motion)

		# Prints the number of changed pixles found
		print('Frame: %d, Pixel Count: %d' % (frameCount, count))

		# Determine how many pixels do you want to detect to be considered "movement"
		if (frameCount > 1 and count > 500):
			# If so then prints movement detected on the console
			print('Movement detected')
			# Prints movement detected on the window
			cv2.putText(resizedFrame, 'Movement detected', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
			# Saves that current frame on the file
			output.write(frame)

		# """ You can delete this part if you don't want the image taken to be shown """
		# This is the normal frame
		cv2.imshow('Frame', resizedFrame)
		# This is the motion detector frame
		cv2.imshow('motion dector', motion)
		# """ Up to here """

		# Press [esc] to break out
		k = cv2.waitKey(1) & 0xff
		if k == 27:
			break

	# Releases the camera and destroys all the windows open
	output.release()
	capture.release()
	cv2.destroyAllWindows()


# Now let's build an terms and conditions widget
# You can let the users now that you will be doing
# Or you may leave it blank if you are the only one using 
def terms():
	def ok():
		# This function grabs the details and saves into a file 
	    user = user_id.get()
	    email = user
	    what = variable.get()
	    t = "Terms and Conditions"
	    file_name = t + ".txt"
	    user = "The owner of " + user + " " + "\n" + str(what) + "s" + " to the Terms and Conditions of Motion Detection Software" + "\n\nThe Terms and Conditions:" + "\n\n\"By using this software you agree that this software can\naccess your webcam when the program is in use to capture\nvideos so that it can process it to detect movement.\nYou also agree that this software can store files on your device\nwhenever it detects movement so that you can view it later;\nafter you view it you may discard those files.\nThis software will also be sending some reports to the\norganization. These are reports upon how well did it\nperformed and the times that it crashed or had issues;\nfor this it will be accessing your internet to send datas.\nPlease also note that if there is any harm to your\nproperty then the organization is not responsible for it.\n"
	    f = open(file_name, 'w')
	    f.write(user)
	    f.close()
	    win.destroy()

		# Then it send them an email saying that they have agreed to the terms and conditions
	    fromaddr = "SENDER_EMAIL"
	    toaddr = email
	    msg = MIMEMultipart() 
	    msg['From'] = fromaddr 
	    msg['To'] = toaddr 
	    msg['Subject'] = "Motion Detection"
	    mes = "Hi There,\nYou just Accepted the terms and conditions of our software\nThanks for using it. We hope to provide you with the best experience possible\n\nSincerely,\nOrganisation"
	    body = mes
	    msg.attach(MIMEText(body, 'plain')) 
	    s = smtplib.SMTP('smtp.gmail.com', 587) 
	    s.starttls() 
	    s.login(fromaddr, "SENDER_PASSWORD") 
	    text = msg.as_string() 
	    s.sendmail(fromaddr, toaddr, text) 
	    s.quit()

	# Widget for the terms and conditions
	win = Tk()
	lb = Label(win, text = "Terms And Conditions", fg = "Red")
	lb.grid(row = 0, column = 0)
	lb = Label(win, text = "By using this software you agree that this software can\naccess your webcam when the program is in use to capture\nvideos so that it can process it to detect movement.\nYou also agree that this software can store files on your device\nwhenever it detects movement so that you can view it later;\nafter you view it you may discard those files.\nThis software will also be sending some reports to the\norganization. These are reports upon how well did it\nperformed and the times that it crashed or had issues;\nfor this it will be accessing your internet to send datas.\nPlease also note that if there is any harm to your\nproperty then the organization is not responsible for it.\n", fg="green")
	lb.grid(row = 1, column = 0)

	lb = Label(win, text = "Your Email ID - Required for Identity", fg = "Blue")
	lb.grid(row = 2, column = 0)
	user_id = Entry(win)
	user_id.grid(row = 3, column = 0)

	variable = StringVar(win)
	variable.set("Click to Select") # default value

	w = OptionMenu(win, variable, "Agree","Disagree")
	w.grid(row = 4, column = 0)

	button = Button(win, text="Submit",fg = "Purple", command=ok)
	button.grid(row = 5, column = 0)

	win.mainloop()



if __name__ == '__main__':
	try:
	    path = "Terms and Conditions.txt"    # Opening the file and seeing if the user has accepted to our Terms and Conditions or not  
	    read_terms = [line for line in open(path)]
	except:
	    f = open("Terms and Conditions.txt",'w')   # If the file is not made then making a file to store if he accepts ot decline
	    f.close()

	try:
	    what_terms = read_terms[1] # This is line two of the Terms and Conditions, here it is written if he has accepted ot declined 
	    what_terms = what_terms[0] # This is the First letter, A or D ,weather Accepted [A] or [D] Declined
	except:
	    what_terms = "blank" # This is so that the if terms doesn't crash if there is nothing

	if what_terms == "A" : # If the terms and conditions was accepted, then it will let the user to use the software
		main()
	else: # Else it will again show the user the same terms and conditions
		terms()
