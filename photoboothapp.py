# import the necessary packages
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import tkinter.font as font
import threading
import datetime
import imutils
import cv2
import os
import time 

# import config as conf
from config import conf

from inviteme_connector import Connector
from image_label import ImageLabel

BASE_URL = "https://inviteme.ovh"






class PhotoBoothApp:
	def __init__(self, vs, outputPath):
		# store the video stream object and output path, then initialize
		# the most recently read frame, thread for reading frames, and
		# the thread stop event
		self.vs = vs 
		self.outputPath = outputPath
		self.frame = None
		self.thread = None
		self.stopEvent = None
		# initialize the root window and image panel
		self.root = tki.Tk()
		self.panel = None
		self.qcd = cv2.QRCodeDetector()
		
		self.conn = None
		self.conn = Connector()
		self.conn.login()

		# cap = cv2.VideoCapture(camera_id)

		# create a button, that when pressed, will take the current
		# frame and save it to file
		self.w_size = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
		self.root.geometry(f"{self.w_size[0]}x{self.w_size[0]}")
		
		if conf.seamless:
			self.root.overrideredirect(True)


		# self.root(f"{self.w_size}x{self.w_size}")
		print(self.w_size)
		print(f"width {int(self.w_size[0]/2)}")
		print(f"height {int(self.w_size[1]/10)}")

		myFont = font.Font(family=conf.fontfamily, size=50)

		pixel = tki.PhotoImage(width=1, height=1 )

		btn_int = tki.Button(
			self.root, 
			text=conf.button_in_text,
			font=myFont,
			image=pixel,
			command=self.send_attendance_in,  
			bg="#00ff00",
			fg="#ffffff",
			height=int(self.w_size[1]*conf.buttons_dim.get('height')),
			width=int(self.w_size[0]*conf.stream_dim.get('width')),
			compound="c",
			anchor="w"
			)

		btn_int.image = pixel
		btn_out = tki.Button(self.root, 
			text=conf.button_out_text,
			font=myFont,
			image=pixel,
			command=self.send_attendance_out, 
			bg="#ff0000",
			fg="#ffffff",
			height=int(self.w_size[1]*conf.buttons_dim.get('height')),
			width=int(self.w_size[0]*(1-conf.stream_dim.get('width'))),
			compound="c",
			anchor="w"

			)
		btn_out.image = pixel

		print(f"height --> {int(self.w_size[1]*conf.buttons_dim.get('height')) }")
		print(f"width --> {int(self.w_size[0]*conf.buttons_dim.get('width')) }")

		# btn_int.place(x=0, y=0 int(self.w_size[1]/10)*0.3)
		# btn_int.place(x=0, y=0 int(self.w_size[1]/10)*0.3)


		# btn_int.place(x=1, y=1, width=int(self.w_size[0]*conf.buttons_dim.get("width")), height=2)
		# btn_out.place(x=1, y=1, width=int(self.w_size[0]*conf.buttons_dim.get("width")), height=2)
		# btn_out.config( , )
		# btn_int.config(width=int(self.w_size[0]*conf.buttons_dim.get("width")) ,height=int(self.w_size[1]*conf.buttons_dim.get("height")) )
		
		# btn_int.width=int(self.w_size[0]/10*0.5) 
		# btn_int.height=int(self.w_size[1]/10*0.3)

		# btn_int.width=int(self.w_size[0]/10*0.5) 
		# btn_int.height=int(self.w_size[1]/10*0.3)
		
		btn_out.pack_propagate(0)
		btn_out.pack_propagate(0)

		# btn_out.width = 20

		self.fr = tki.Frame(
			bg="white")
		self.fr.config(width=int((self.w_size[0]/10)*0.5) ,height=int((self.w_size[1]/10)*0.7) )



		# btn_int.grid(row=1, column=0, columnspan=2, sticky="nsew")
		# btn_out.grid(row=1, column=1, columnspan=2, sticky="nsew")


		
		self.fr.grid(row=0, column=1, columnspan=2, sticky="nsew")
		btn_int.grid(row=1, column=0, columnspan=2, sticky="nsew")
		btn_out.grid(row=1, column=1, columnspan=2, sticky="nsew")


		
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.setDaemon(True)
		self.thread.start()
		# set a callback to handle when the window is closed
		self.root.wm_title("invite_me qr code reader")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)


		self.users = {}

		if len(self.users) == 0:
			self.create_gif()
		else:
			self.create_textbox()



		self.error = None

		# self.create_error()

	


	def create_gif(self):
		self.textbox = None
		self.gif = ImageLabel(self.fr)
		self.gif.config(borderwidth=0)
		self.gif.pack()
		self.gif.load(conf.gif_path)


	def clear_textbox(self):

		self.users = dict()
		if self.textbox:
			self.textbox.pack_forget()
			self.instruct.pack_forget()
			self.create_gif()

	def create_error(self, body):
		fnt = font.Font(
			family=conf.fontfamily, 
			size=60)

		if self.error == None:

			self.error =  tki.Text(self.root,
				bg="red",
				fg="white",
				borderwidth=2,
				font=fnt,
				height=5,
				width=20)

			if body.get("info"):
				info = body.get("info")
			else:
				info = "BŁĄD SIECI"

			self.error.insert(tki.END, info)
			self.error.tag_configure("center", justify='center')
			self.error.tag_add("center", 1.0, "end")


			# self.error.place(x=100, y=100)

			self.w_size[0]/10

			self.error.place(x=int((self.w_size[0]/100)*15), y=int((self.w_size[1]/100)*15), width=int((self.w_size[0]/100)*70), height=int((self.w_size[1]/100)*70))

			self.error.lift()

			print(f"create error, {self.error}")

		# self.error

	def clear_error(self):
		print(f"clear error, {self.error}")
		if self.error:
			self.error.place_forget()
			self.error = None

	def create_textbox(self):
		code_fnt = font.Font(
			family=conf.fontfamily, 
			size=15)
		self.textbox = tki.Text(self.fr, 
			bg="white", 
			fg="black", 
			font=code_fnt,
			borderwidth=0,
			height=3,
			wrap=tki.WORD)

		# self.textbox.width = int(self.w_size[0]*conf.buttons_dim.get("width"))
		# self.textbox.height = 2

		self.textbox.config(state="disabled")
		

		fnt = font.Font(
			family=conf.fontfamily, 
			size=30,)

		self.instruct = tki.Text(self.fr, 
			bg="white", 
			fg="black", 
			borderwidth=0, 
			font=fnt,
			height=3,
			width=25,
			wrap=tki.WORD)
		# self.instruct.configure(justify='center')
		self.instruct.tag_configure("center", justify='center')
		self.instruct.tag_add("center", 1.0, "end")


		# self.instruct.tag_configure("center", justify='center')

		# self.instruct.width = int(self.w_size[0]*conf.buttons_dim.get("width")/2)
		# self.instruct.width = 2
		

		# self.instruct.config(state="normal")
		self.instruct.insert(tki.END, f"zeskanuj kolejny kod lub kliknij przycisk \n")
		# self.instruct.config(state="disabled")


		self.instruct.place(x=0, y=200)
		self.textbox.place(x=0, y=0)

	def parse_qr(self, s):
		if not s.startswith(BASE_URL):
			return ""

		s = s.split("/")
		for elem in s:
			if "invitation=" in elem:
				code = elem[elem.index("=")+1:]
				if self.users.get(code) == None:

					self.users[code] = 0
					
					if self.textbox == None:
						self.gif.pack_forget()
						self.create_textbox()

					self.textbox.config(state="normal")
					self.textbox.insert(tki.END, f"code {code} \n")
					self.textbox.config(state="disabled")

					print(self.textbox)




	def videoLoop(self):
		
		while True:
			try:
				while not self.stopEvent.is_set():

					self.frame = self.vs.read()
					ret_qr, decoded_info, points, _ = self.qcd.detectAndDecodeMulti(self.frame)
			
					if ret_qr:
						for s, p in zip(decoded_info, points):
							if s:
								data = self.parse_qr(s)
								color = (0, 255, 0)
							else:
								color = (0, 0, 255)

							self.frame = cv2.polylines(self.frame, [p.astype(int)], True, color, 5)
					
					self.frame = imutils.resize(self.frame)
							

					image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
					dim = (int(self.w_size[0]*conf.stream_dim.get("width")), int(self.w_size[0]*conf.stream_dim.get("height")))

					image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
					image = Image.fromarray(image)
					image = ImageTk.PhotoImage(image)
			
					if self.panel is None:
						self.panel = tki.Label(image=image)
						self.panel.image = image

						self.panel.grid(row=0, column=0)
						self.panel.lower()

					else:
						self.panel.configure(image=image)
						self.panel.image = image
					

			except RuntimeError as e:
				print(e)
				print("[INFO] caught a RuntimeError")


	def send_attendance_in(self):
		print(self.users)
		out = list()
		
		for user in self.users:
			print(user)
			# for i in range(0, 10):
			print("while in")
			res  = self.conn.attendance_in(user)
			print(f"works: {res}")
			if res.status_code == 200:
				print("WORKS")
				
				out.append(res)
				self.clear_error()
				break
			else:
				self.create_error(res.json())
				print("failure")
				time.sleep(1)
				# return False

		self.clear_textbox()
		return out
	def send_attendance_out(self):
		print(self.users)
		out = list()
		
		for user in self.users:
			print(user)
			# for i in range(0, 10):
			print("while in")
			res  = self.conn.attendance_out(user)
			print(f"works: {res}")
			if res.status_code == 200:
				print("WORKS")
				
				out.append(res)
				self.clear_error()
				break
			else:
				self.create_error(res.json())
				print("failure")
				time.sleep(1)
				# return False

		self.clear_textbox()
		return out


				




	def onClose(self):

		print("[INFO] closing...")

		self.stopEvent.set()
		print(1)
		time.sleep(1)
		self.vs.stop()
		time.sleep(1)

		print(2)
		self.root.quit()
		print(3)