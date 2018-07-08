import pprint
import code
import json
import requests
import sys
import random
import re
import vk
from datetime import datetime, date
import time
import instabot
import blbot
class biglike:



	def __init__(self,i_u,i_l,i_p,b_l,b_p,vk):

		#Учетка инстаграм
		self.i_link = i_u
		self.i_login = i_l
		self.i_password = i_p

		#Учетка biglike
		self.b_login =b_l
		self.b_password = b_p

		#токен вк
		self._t = vk
		#hash
		self._h = 1491737238109
		BL_headers = {}
		BL_INST = {}
		I = {}
		i_headers = {}
		logg = ""
		
		
	def set(self):
		global BL_headers,BL_INST,I,i_headers
		
		try:
			I = instabot.bot(self.i_login,self.i_password)
			i_headers = I.login()

			if str(self.b_login) == '0' :
				BL_headers = i_headers
				BL = blbot.bot(self.i_login,self.i_password)
				BL_INST = BL.inst_to_bl(BL_headers,i_headers,self.i_link)
				
			else:
				BL = blbot.bot(self.b_login,self.b_password)
				BL_headers = BL.login()
				BL_INST = BL.inst_to_bl(BL_headers,i_headers,self.i_link)
					
			f = open('ins.txt', 'w')
			for item in BL_INST:
				f.write("bl_i %s\n" % item)
			return "OK"
		except:
			return "None"

		
	def vklike(self):
		global BL_headers,BL_INST
		session = vk.Session()
		api = vk.API(session) 
		non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)  #переводим спец.символы в читаемые

		r = requests.get('http://biglike.org/vklike',headers = BL_headers).text.translate(non_bmp_map)
		try:
			point = r.split('id="points"',1)[1].split('</font>',1)[0].split('px;">',1)[1]
			r = r.split('proverka(',1)[1].split('"',1)[0]
			task_id =  r.split(', ',1)[0]
			link =  r.split(';',4)[3].split('&',1)[0]
			screen_name = link.split('.com/',1)[1]
		except:
			self.vklike()
		#r = r.split('proverka(',1)[1].split('"',1)[0]


		if "wall" in screen_name:type_ob = "post"
		elif "photo" in screen_name:type_ob = "photo"
		elif "video" in screen_name:type_ob = "video"

		#выполняем задание
		owner_id =  str(re.findall('\d+',screen_name.split('_',1)[0])).replace('\'','').replace('[','').replace(']','')

		if "-" in screen_name: owner_id = '-'+str(owner_id)
		item_id =  str(re.findall('\d+',screen_name.split('_',1)[1])).replace('\'','').replace('[','').replace(']','')
		try:
			s = api.likes.add (access_token= self._t,type=type_ob,owner_id=owner_id,item_id=item_id)

			#берем заслуженные баллы
			url = 'http://biglike.org/ajax.php?divid='+task_id +'&taskid='+task_id+'&task=vklike&_='+ str(self._h+1)
			r = requests.get(url,headers = BL_headers).text.translate(non_bmp_map)

			if '<font size="6" >' in r:
				
				print (datetime.now().strftime("%H:%M:%S")+ ' Банк: ' + point + ' ' + r.split('<font size="6" >',1)[1].split('<',1)[0] + ' лайк вконтакте ')
			else:
				url2 = 'http://biglike.org/ajax.php?divid=1&taskid='+task_id+'&task=vklike'
				requests.get(url2,headers = BL_headers).text.translate(non_bmp_map)
				print('problemes.../' + screen_name)
			
		except Exception as e:
			pprint.pprint(str(e))
			url2 = 'http://biglike.org/ajax.php?divid=1&taskid='+task_id+'&task=vklike'
			requests.get(url2,headers = BL_headers).text.translate(non_bmp_map)
			
		time.sleep(random.randint(2, 5))
	def vkfollow(self):
		global BL_headers,BL_INST
		session = vk.Session()
		api = vk.API(session) 
		non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)  #переводим спец.символы в читаемые
		r = requests.post('http://biglike.org/vkgroup',headers = BL_headers,data={'': ''}).text.translate(non_bmp_map)
		try:
			point = r.split('id="points"',1)[1].split('</font>',1)[0].split('px;">',1)[1]
			r = r.split('proverka(',1)[1].split('"',1)[0]
			task_id =  r.split(', ',1)[0]
			link =  r.split(';',4)[3].split('&',1)[0]
			screen_name = link.split('.com/',1)[1]
		except:
			self.vkfollow()


		#выполняем задание
		group_id = api.utils.resolveScreenName (screen_name=screen_name)['object_id']
		try:
			api.groups.join(access_token=self._t,group_id=group_id)
			#берем заслуженные баллы
			url = 'http://biglike.org/ajax.php?divid='+task_id +'&taskid='+task_id+'&task=vkgroup&_='+ str(self._h+2)

			r = requests.post(url,headers = BL_headers,data={'': ''}).text.translate(non_bmp_map)
			balls = r.split('<font size="6" >',1)[1].split('<',1)[0]
			
			print (datetime.now().strftime("%H:%M:%S")+ ' Банк: ' + point + ' ' + balls + ' подписка вконтакте ')
		except Exception as e:
			pprint.pprint(str(e))
			url2 = 'http://biglike.org/ajax.php?divid=1&taskid='+task_id+'&task=vkgroup'
			requests.post(url2,headers = BL_headers,data={'': ''}).text.translate(non_bmp_map)
			
		time.sleep(random.randint(3, 7))

	def instalike(self):
		global BL_headers,BL_INST,I,i_headers, logg
		non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)  #переводим спец.символы в читаемые
		r = requests.get('http://biglike.org/instalike',headers = BL_INST).text.translate(non_bmp_map) 
		inst_link = ''
		try:
			point = r.split('id="points"',1)[1].split('</font>',1)[0].split('px;">',1)[1]
			r = r.split('proverka(',1)[1].split('"',1)[0]
			task_id =  r.split(', ',1)[0]
			inst_link =  r.split(';',4)[3].split('&',1)[0]
		except:
			self.instalike()		

		#print("Инста лайк " + inst_link)
		if I.like(inst_link) == None : 
			return None
		time.sleep(random.randint(1, 3))        
		#берем заслуженные баллы
		#url = 'http://biglike.org/ajax.php?divid='+task_id +'&taskid='+task_id+'&task=instalike&_='+ str(self._h-1)
		url = 'http://biglike.org/ajax.php?divid='+task_id +'&taskid='+task_id+'&task=instalike'
		#print('Забираем баллы' + url)
		#r = requests.get(url,headers = BL_INST).text.translate(non_bmp_map)
		r = requests.get(url,headers = BL_INST)
		r = r.text.translate(non_bmp_map)

		#print(r)
		
		#исключение
		def waiting():
			time.sleep(random.randint(1, 3))
			url = 'http://biglike.org/ajax.php?divid='+task_id +'&taskid='+task_id+'&task=instalike'
			#pprint.pprint(BL_INST)
			r = requests.get(url,headers = BL_INST).text.translate(non_bmp_map)
			try:
				balls = r.split('<font size=\"6\" >',1)[1].split('<',1)[0]
				
				print (datetime.now().strftime("%H:%M:%S")+ ' Банк: ' + point + ' ' + balls + ' лайк в инстаграме ')
			except:
				url2 = 'http://biglike.org/ajax.php?divid=1&taskid='+task_id+'&task=instalike'
				requests.get(url2,headers = BL_INST).text.translate(non_bmp_map)
				#f = open('logg.txt', 'a')
				#logg = 'Поймано исключение \n' + url + '\n' + inst_link + '\n\n ' +  r + '\n\n\n'
				#f.write(logg)
				#f.close()
				#http://biglike.org/ajax.php?divid=1&taskid=479824&task=instalike
				#print(r)
		try:
			balls = r.split('<font size=\"6\" >',1)[1].split('<',1)[0]
			
			print (datetime.now().strftime("%H:%M:%S")+ ' Банк: ' + point + ' ' + balls + ' лайк в инстаграме ')
		except IndexError:
			#print('поймали исключение сплита 152 строка bot.py')
			waiting()

	def instafollow(self):
		global BL_headers,BL_INST,I,i_headers, logg
		non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)  #переводим спец.символы в читаемые
		r = requests.get('http://biglike.org/instasub',headers = BL_INST,data={'': ''}).text.translate(non_bmp_map)
		inst_link = ''
		try:
			point = r.split('id="points"',1)[1].split('</font>',1)[0].split('px;">',1)[1]
			r = r.split('proverka(',1)[1].split('"',1)[0]
			task_id =  r.split(', ',1)[0]
			inst_link =  r.split(';',4)[3].split('&',1)[0]
		except:
			return None

		#print ('\n\nПодписка на ' + inst_link)
		I.follow(inst_link)

		time.sleep(random.randint(1, 3))        
		#берем заслуженные баллы
		
		url = 'http://biglike.org/ajax.php?divid='+task_id +'&taskid='+task_id+'&task=instasub'
		#print('Забираем баллы за подписку \n' + url)
		r = requests.get(url,headers = BL_INST)
		r = r.text.translate(non_bmp_map)
		#print ('\n ' + r)	
		#исключение
		def waiting():
			time.sleep(random.randint(1, 3))
			
			url = 'http://biglike.org/ajax.php?divid='+task_id +'&taskid='+task_id+'&task=instasub'
			#print ('\nпопытка 2\n' + url)
			#pprint.pprint(BL_INST)
			r = requests.get(url,headers = BL_INST)
			r = r.text.translate(non_bmp_map)
			try:
				balls = r.split('<font size=\"6\" >',1)[1].split('<',1)[0]
				
				print (datetime.now().strftime("%H:%M:%S")+ ' Банк: ' + point + ' ' + balls + ' подписка в инстаграме ')

			except:
				url2 = 'http://biglike.org/ajax.php?divid=1&taskid='+task_id+'&task=instasub'
				requests.get(url2,headers = BL_INST).text.translate(non_bmp_map)
				#print ('\n' + r)
				#f = open('logg.txt', 'a')
				#logg = 'Поймано исключение \n' + url + '\n' + inst_link + '\n ' +  r + '\n\n\n'
				#f.write(logg)
				#f.close()
		try:
			balls = r.split('<font size=\"6\" >',1)[1].split('<',1)[0]
			
			print (datetime.now().strftime("%H:%M:%S")+ ' Банк: ' + point + ' ' + balls + ' подписка в инстаграме ')
			
		except IndexError:
			waiting()
	def go(self,all,count):
		
		count = count +1
		
		if all==1:
			for i in range(0,count):
				self.vklike()
				self.vkfollow()
				self.instalike()
				self.instafollow()
				
		elif all==0:
			for i in range(0,count):
				self.instalike()
				self.instafollow()
				
"""
for i in range(1, 30):
    vklike()
    vkfollow()
    instafollow()
    instalike()
    _h = _h + 4*i
"""
