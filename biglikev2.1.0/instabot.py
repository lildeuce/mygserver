import requests
import pprint
import json

class bot:

	def __init__(self, login, password):
		self.l = login
		self.p = password


	session = requests.Session()
	_insta_login = {}
	_insta_like = {}
	def login(self):
		session = requests.Session()
		global _insta_login,_insta_like,login,password

		response = session.get('https://www.instagram.com')
		x = session.cookies.get_dict()
		csrftoken = x["csrftoken"]
		mid = x["mid"]
		rur = x["rur"]

		data = { 'username': self.l,'password':self.p}
		cook = {
		'accept' : '*/*',
		'accept-encoding' : 'gzip, deflate, br',
		'accept-language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
		'content-length': '41',
		'content-type' : 'application/x-www-form-urlencoded',
		'cookie' :  'mid=' + str(mid)+  ';csrftoken='+ str(csrftoken)+';s_network=""; ig_vw=1366; ig_pr=1;rur=ATN' ,
		'origin' : 'https://www.instagram.com',
		'referer' : 'https://www.instagram.com/',
		'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 OPR/44.0.2510.857',
		'x-csrftoken': csrftoken,
		'x-instagram-ajax' : '1',
		'x-requested-with' : 'XMLHttpRequest'
		}

		q = session.post('https://www.instagram.com/accounts/login/ajax/', headers = cook, data = data)
		cookIn = session.cookies.get_dict()
		_insta_login = cookIn
		


		if "ds_user_id" in cookIn:
		
			_insta_like = {
			'Host': 'www.instagram.com',
			'Accept': '*/*',
			'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
			'Accept-Encoding': 'gzip, deflate, br',
			'X-Instagram-AJAX': '1',
			'Content-Type': 'application/x-www-form-urlencoded',
			'X-Requested-With': 'XMLHttpRequest',
			'X-CSRFToken' : _insta_login["csrftoken"],
			'Cookie':  'mid='+_insta_login["mid"]+ ';csrftoken='+ _insta_login["csrftoken"] +';sessionid='+ _insta_login["sessionid"],
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
			'Referer': ''
			}
			#print ('https://www.instagram.com/' + self.l + '/?__a=1')
			#res = session.post('https://www.instagram.com/' + self.l + '/?__a=1', headers = cookIn, data = {})

			#uname = json.loads(res.text)["graphql"]["user"]["username"]
			print("INSTAGRAM: успешная авторизация | " + self.l  + "  id: " + str(cookIn["ds_user_id"]))
			return _insta_like
		else:
			print("INSTAGRAM: Неверный логин или пароль.")
			return "None"
	  
	def like(self,inst_link):

		global _insta_login,_insta_like
		try:
			screen_name = inst_link.split('.com/',1)[1].split('?',1)[0]
		except:
			return None
		get_media_id = 'https://www.instagram.com/' + screen_name + '?__a=1'
		
		#заполняем refer
		_insta_like["Referer"] = 'https://www.instagram.com/' + screen_name

		try:
			r = requests.get(get_media_id,headers = _insta_login,data={'': ''}).json()
			setLike = 'https://www.instagram.com/web/likes/' + r['graphql']['shortcode_media']['id'] + '/like/'
			#print('like:  ' + setLike)
			res = requests.post(setLike,headers = _insta_like ,data={'': ''}).json()
			#print(res["status"])
			return _insta_like
		except:
			return "INSTAGRAM: Ошибка доступа"
		
	def follow(self,inst_link):
		global _insta_like
		screen_name = inst_link.split('.com/',1)[1].split('/',1)[0]
		#print ('screen_name: ' + screen_name)
		#get_user_id = 'https://www.instagram.com/' + screen_name + '?__a=1'
		get_user_id = 'https://www.instagram.com/' + screen_name + '?__a=0'
		refer = 'https://www.instagram.com/' + screen_name
		_insta_like["Referer"] = 'https://www.instagram.com/' + screen_name
		try:
			#r = requests.get(get_user_id,headers = _insta_like,data={'': ''}).json()
			r = requests.get(get_user_id,headers = _insta_like,data={'': ''}).text
			src = r.split('graphql":',1)[1].split(',"mutual_followers"',1)[0]+'}}'
			r = json.loads(src)
			
			user_id = r['user']['id']
			follow = 'https://www.instagram.com/web/friendships/' + user_id + '/follow/'
			r = requests.post(follow,headers = _insta_like,data={'': ''}).json()
			return r["status"]
		except:
			return "INSTAGRAM: Ошибка доступа"
  

		"""
		пример работы
		bot = instabot.bot(login,password)
		bot.login()
		bot.like(link)
		bot.follow(link)
		"""
  
