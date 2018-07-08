import requests
import pprint
import instabot
import json
import sys, traceback

class bot:
	def __init__(self, login, password):
		self.l = login
		self.p = password

	PHPSESSID = ''
	def login(self):
		session = requests.Session()
		
		global login,password,PHPSESSID
		
		response = session.get('http://biglike.org/')
		x = session.cookies.get_dict()

		data = {
					'logpass' :'1',
					'vklink' : self.l,
					'pass' : self.p
					}
		cook= {
					'Accept':'*/*',
					'Accept-Encoding':'gzip, deflate',
					'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
					'Connection':'keep-alive',
					'Content-Length':'58',
					'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
					'Cookie':'PHPSESSID=' + x["PHPSESSID"],
					'Host':'biglike.org',
					'Origin':'http://biglike.org',
					'Referer':'http://biglike.org/',
					'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
					'X-Requested-With':'XMLHttpRequest'
					}


		r = session.post('http://biglike.org/login.php',headers = cook, data = data)
		x = session.cookies.get_dict()
		if r.text=="Login error!":
			print("Ошибка авторизации biglike. Неверный логин и/или пароль.")
			return "Ошибка авторизации biglike. Неверный логин и/или пароль."
		
		cook2 = {
					'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'Accept-Encoding':'gzip, deflate, sdch',
					'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
					'Connection':'keep-alive',
					'Cookie':'PHPSESSID='+ x["PHPSESSID"],
					'Host':'biglike.org',
					'Referer':'http://biglike.org/',
					'Upgrade-Insecure-Requests':'1',
					'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
					}

		r = session.get('http://biglike.org/instr',headers = cook2)
		x = session.cookies.get_dict()

		PHPSESSID = x["PHPSESSID"]
		hash = x["hash"]
		fermer = x["fermer"]
			
		headers = {
		'Host': 'biglike.org',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate',
		'Referer': 'http://biglike.org/earn',
		'Cookie': 'PHPSESSID=' + PHPSESSID + '; hash=' + hash + '; fermer=' + fermer,
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'Cache-Control': 'max-age=0'
				}
		print ("BIGLIKE: успешная авторизация. | id: " + x["fermer"])
		return headers


	def inst_to_bl(self,_bl_cook,i_cook,insta_link):	
		# get profile info
		url_edit = 'https://www.instagram.com/accounts/edit/'
		page_html = requests.get(url_edit, headers = i_cook)

		src = page_html.text.split('sharedData = ',1)[1].split(';</script',1)[0]
		r = json.loads(src)
		bio = r['entry_data']['SettingsPages'][0]['form_data']
		# bio - json bi

		global PHPSESSID
		bl_session = requests.Session()

		data = {
			'linkinsta':insta_link,
			'type':'instalog'
			}
		response = bl_session.get('http://biglike.org/')
		x = bl_session.cookies.get_dict()
		PHPSESSID = x["PHPSESSID"]
		cook ={
			'Accept':'*/*',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
			'Connection':'keep-alive',
			'Content-Length':'18',
			'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			'Cookie':'PHPSESSID='+ PHPSESSID,
			'Host':'biglike.org',
			'Origin':'http://biglike.org',
			'Referer':'http://biglike.org/',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
			'X-Requested-With':'XMLHttpRequest'
		}

		ck = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
			'Connection':'keep-alive',
			'Cookie':'PHPSESSID=' + PHPSESSID,
			'Host':'biglike.org',
			'Referer':'http://biglike.org/',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
			}

		r = bl_session.post('http://biglike.org/login.php',headers = cook,data = data).json()
		x = bl_session.cookies.get_dict()	
		#pprint.pprint(r)
		if (r['response']['link']=='https://www.instagram.com/accounts/edit/'):
			print("Привязываем инстаграм через временную правку био профиля")
			phrase = r['response']['phrase']
			print("Фраза: \n" + bio['biography'] + "\nвременно будет заменена на: " + phrase)
			

			# set new bio
			bio_new = bio
			bio_new['biography'] = phrase
			
			i_session = requests.Session()
			r = i_session.post(url_edit,headers = i_cook,data = bio_new).json()
			x = i_session.cookies.get_dict()	
			print ("Статус смены био:" + r['status'])
			try:
				r = bl_session.post('http://biglike.org/login.php',headers = cook,data = {'instchkcom':'true'}).json()
				print(r)
				#r = requests.post('http://biglike.org/login.php',headers = cook,data = {'instchkcom':'true'}).json()
				#print(r)
				x = bl_session.cookies.get_dict()	
				
				#print(x)
				if r["response"]["type"]=="ok":
					print("Замена БИО подтверждена...меняем обратно...")
					
					r = i_session.post(url_edit,headers = i_cook,data = bio).json()
					x = i_session.cookies.get_dict()	
					print ("Статус смены био:" + r['status'])

					r = bl_session.get('http://biglike.org/instr',headers = ck)
					x = bl_session.cookies.get_dict()

					if "hash" in x:
						
						PHPSESSID = x["PHPSESSID"]
						hash = x["hash"]
						fermer = x["fermer"]
							
						headers = {
						'Host': 'biglike.org',
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
						'Accept-Encoding': 'gzip, deflate',
						'Referer': 'http://biglike.org/earn',
						'Cookie': 'PHPSESSID=' + PHPSESSID + '; hash=' + hash + '; fermer=' + fermer,
						'Connection': 'keep-alive',
						'Upgrade-Insecure-Requests': '1',
						'Cache-Control': 'max-age=0'
								}
						print("BIGLIKE: Успешная привязка instagram")	
					else:
						print("Нет хэша в куках")
					return	headers

			except Exception as e:
				print(str(e))
		return None	


		
	def inst_to_bl2(self,_bl_cook,i_cook,insta_link):
		global PHPSESSID
		session = requests.Session()
		si = requests.Session()
		data = {
			'linkinsta':insta_link,
			'type':'instalog'
			}
		response = session.get('http://biglike.org/')
		x = session.cookies.get_dict()
		PHPSESSID = x["PHPSESSID"]
		cook ={
			'Accept':'*/*',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
			'Connection':'keep-alive',
			'Content-Length':'18',
			'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			'Cookie':'PHPSESSID='+ PHPSESSID,
			'Host':'biglike.org',
			'Origin':'http://biglike.org',
			'Referer':'http://biglike.org/',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
			'X-Requested-With':'XMLHttpRequest'
		}

		r = session.post('http://biglike.org/login.php',headers = cook,data = data).json()
		x = session.cookies.get_dict()
		if (r["response"]["type"]=='1'):
			print("Привязываем инстаграм через временный комментарий")
			#pprint.pprint(r)
			link_comment = r["response"]["link"]

			try:
				r = requests.get(link_comment + '&__a=1',headers = i_cook).json()
			except:
				r = requests.get(link_comment + '?__a=1',headers = i_cook).json()
			#pprint.pprint(r)
			try:
				media_id = r["media"]["id"]
			except:
				media_id = r["graphql"]["shortcode_media"]["id"]
			#pprint.pprint(str(media_id))
			#Комментим
			i_cook["referer"] = link_comment
			text = {'comment_text':'не плохо)'}
			r = si.post('https://www.instagram.com/web/comments/' + str(media_id) + '/add/',headers = i_cook,data = text).json()
			print ("Статус комментария: " + r["status"])
			comment_id = r["id"]
			

			try:		

				r = requests.post('http://biglike.org/login.php',headers = cook,data = {'instlikecheck':'true'}).json()
				
				if (r["response"]["type"]=='3'):
					print("Комментарий найден")
				else:
					print("Комментарий не найден")
			except:
				print("не можем найти комментарий")
			#Удаляем
			r = si.post('https://www.instagram.com/web/comments/' + str(media_id) + '/delete/' + str(comment_id) + '/',headers = i_cook).json()
			print("Статус удаления комментария: " + r["status"])

			r = session.post('http://biglike.org/login.php',headers = cook,data = {'instchkcom':'true'}).json()
			
				
			if r["response"]["type"]=="ok":
				x = session.cookies.get_dict()
				
						#Проверяем привязку
				ck = {
					'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'Accept-Encoding':'gzip, deflate, sdch',
					'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
					'Connection':'keep-alive',
					'Cookie':'PHPSESSID=' + PHPSESSID,
					'Host':'biglike.org',
					'Referer':'http://biglike.org/',
					'Upgrade-Insecure-Requests':'1',
					'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
					}
				
				r = session.get('http://biglike.org/instr',headers = ck)
				x = session.cookies.get_dict()

				if "hash" in x:
					
					PHPSESSID = x["PHPSESSID"]
					hash = x["hash"]
					fermer = x["fermer"]
						
					headers = {
					'Host': 'biglike.org',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
					'Accept-Encoding': 'gzip, deflate',
					'Referer': 'http://biglike.org/earn',
					'Cookie': 'PHPSESSID=' + PHPSESSID + '; hash=' + hash + '; fermer=' + fermer,
					'Connection': 'keep-alive',
					'Upgrade-Insecure-Requests': '1',
					'Cache-Control': 'max-age=0'
							}
					print("BIGLIKE: Успешная привязка instagram")	
				else:
					print("Нет хэша в куках")
				return	headers
			elif r["response"]["type"]=='10':
				print("BL не может проверить удаление комментария...")
				print(link_comment)
			else:
				print ("Ошибка BL!")
				print(link_comment)
				pprint.pprint(r)
		else:
			#session.cookies.get_dict()
			#session.get('http://biglike.org/instr',headers = ck)
			
			print("BigLike предложил алтернативную авторизацию через инстаграм.")
			print("info")
			pprint.pprint(r.text)
			return "None"
	
			

		
