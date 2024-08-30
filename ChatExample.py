from crushon.client import Client
from crushon.lib import Characters

from bs4 import BeautifulSoup
import requests
import json
import time
import os

class SecMailApi:
	def __init__(self):
		pass

	def getEmail(self):
		resp = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1')
		resp.raise_for_status()
		return resp.json()[0]

	def getMessages(self, email):
		login = email.split("@")[0]
		domain = email.split("@")[1]
		resp = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}")
		resp.raise_for_status()
		return resp.json()

	def openMessage(self, email, msgId):
		login = email.split("@")[0]
		domain = email.split("@")[1]
		resp =requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msgId}")
		resp.raise_for_status()
		return resp.json()

class SimpleTranslator:
	def __init__(self):
		self.base_url = "https://translate.googleapis.com/translate_a/single"
	
	def translate(self, text: str, target_language: str = 'ru') -> str:
		"""
		Переводит текст с одного языка на другой, разбивая текст на части при необходимости.

		Args:
			text (str): Текст для перевода.
			target_language (str): Код языка для перевода (например, 'ru' для русского).

		Returns:
			str: Переведенный текст.
		"""
		# Функция для перевода одного фрагмента текста
		def translate_chunk(chunk: str) -> str:
			params = {
				'client': 'gtx',
				'sl': 'auto',
				'tl': target_language,
				'dt': 't',
				'q': chunk
			}
			response = requests.get(self.base_url, params=params)
			response.raise_for_status()
			result = response.json()
			# Извлечение переведенного текста
			return ''.join([item[0] for item in result[0]])

		# Разбиение текста на части
		chunk_size = 2000  # Максимально допустимый размер фрагмента, может потребоваться корректировка
		chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
		
		# Перевод каждой части и объединение результатов
		translated_chunks = [translate_chunk(chunk) for chunk in chunks]
		return ''.join(translated_chunks)


class ChatExample:
	def __init__(self, nsfw: bool = False, language: str = "ru"):
		self.client = Client()
		self.translator = SimpleTranslator()
		self.EmailApi = SecMailApi()
		self.characterObj = None
		self.language = language
		self.nsfw = nsfw
		self.recomData = {}

	def chat(self):
		select = int(input("""
1. from recommendations
2. from inbox
		
> """))
		if select == 1:
			chats = self.client.get_recommendations(nsfw=self.nsfw)
		elif select == 2:
			chats = self.client.inbox()
		self._clear()
		for idx, chat in enumerate(chats["characters"]):
			print(f'{idx+1}. chat: {chat["name"]}')
			self.recomData[idx+1] = chat["id"]

		charNum = input("Select character: ")
		self._clear()
		for msg in reversed(self.characterObj.get_history(self.recomData.get(int(charNum)))):
			translated_text = self.translator.translate(msg["content"], target_language=self.language)
			role_prefix = "\n[user]: " if msg["role"] == 1 else "\n[bot]: "
			print(f'{role_prefix}{translated_text}')

		while True:
			messsage = input("enter msg to character> ")
			answer = self.characterObj.send_message(text=messsage, charid=self.recomData.get(int(charNum)))["content"]
			translated_text = self.translator.translate(answer, target_language=self.language)
			role_prefix = "\n[user]: " if msg["role"] == 1 else "\n[bot]: "
			print(f'{role_prefix}{translated_text}')

	def _loginCookies(self, fileName):
		with open(fileName, "r") as file:
			cookies = json.load(file)
		self.client.set_cookies(cookies)
		self.characterObj = Characters(self.client)
		self._clear()
		self.chat()
		

	def _login(self, email: str):
		self.client.login(email)
		AuthLink = input("Enter AuthLink from your email: ")
		self.client.confirm(AuthLink)
		self.characterObj = Characters(self.client)
		saveType = input("save cookies to file?(Y/N): ")
		if saveType.lower() == "y":
			with open("cookies.json", "w") as file:
				json.dump(self.client.cookies, file)

		self._clear()
		self.chat()

	def login(self):
		select = int(input('''
1. login by email
2. login by cookies(cookie file)
3. guest

> '''))
		if select == 1:
			email = input("Your email: ")
			self._login(email)
		elif select == 2:
			fileCookies = input("cookie file name(.json): ")
			self._loginCookies(fileCookies)
		elif select == 3:
			self.createGuest()
		else:
			raise Exception("Error!")

	def createGuest(self):
		GuestEmail = self.EmailApi.getEmail()
		print(f"[+] created {GuestEmail} Email")
		self.client.login(GuestEmail)
		AuthUrl = None
		while True:
			time.sleep(1)
			print(f"[!] cheking {GuestEmail} messages")
			messages = self.EmailApi.getMessages(GuestEmail)
			if messages:
				content = self.EmailApi.openMessage(GuestEmail, messages[0]["id"])
				soup = BeautifulSoup(content["body"], 'html.parser')
				img_tag = soup.find('a')
				AuthUrl = img_tag.get('href')
				break

		if AuthUrl:
			self.client.confirm(AuthUrl)
			saveType = input("save cookies to file?(Y/N): ")
			if saveType.lower() == "y":
				with open("Guestcookies.json", "w") as file:
					json.dump(self.client.cookies, file)
			self._clear()
			self.characterObj = Characters(self.client)
			self.chat()

	def _clear(self):
		if os.name == 'nt':
			os.system('cls')
		else:
			os.system('clear')

if __name__ == "__main__":
	nsfw_Allow = input("allow NSFW?(Y/N): ")
	language = input("input language to translate(ru/en/ua/...): ")
	ChatExample(True if nsfw_Allow.lower() == "y" else False, language).login()