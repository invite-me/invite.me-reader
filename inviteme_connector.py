import requests
from bs4 import BeautifulSoup
# import config as conf
from config import conf




class Connector():
	def __init__(self):
		self.session = requests.Session()
		self.csrf_token = self.get_csrf()

	def parse_csrf(self,html: str) -> str :
		soup = BeautifulSoup(html)
		token = soup.find('input', {'name':'csrf_token'})['value']

		conf.payload["csrf_token"] = token
		return token

	def get_csrf(self) -> str:
		html = self.session.get(conf.url_login)
		return self.parse_csrf(html.text)

	def login(self) -> str:
		s = self.session.post(conf.url_login, data=conf.payload)
		self.parse_csrf(html=s.text)

		if "You are logged as" in s.text:
			print("============ API logged in")
			return True
		else:
			print("============ API loggin error")
			return False

	def attendance_in(self, invitation_str: str):
		print("ATTENDANCE in")

		try:
			s = self.session.post(conf.url_att_in, data=conf.payload, params={"invitation_string":invitation_str})

		except Exception as e:
			print(e)

		print(f"status_code: {s.status_code}")

		print(s.json())
		# if s.status_code == 200:
		# 	print("ATTENDANCE REGISTERED")
		# 	# return True
		# 	return s.json()
		# else:
		# 	return False
		return s

	def attendance_out(self, invitation_str: str):
		s = self.session.post(conf.url_att_out, data=conf.payload, params={"invitation_string":invitation_str})
		# if s.status_code == 200:
		# 	return True
		# else:
		# 	return False
			
		return s





if __name__ == "__main__":
	con = Connector()
	print(con.login())
	con.attendance_in("YTonCmRhIGchdcYHPTbCrFJkOtxeAcjxDAuFdXGPkNEXkAaNuUzlKoRceGPFNber")
	con.attendance_out("YTonCmRhIGchdcYHPTbCrFJkOtxeAcjxDAuFdXGPkNEXkAaNuUzlKoRceGPFNber")