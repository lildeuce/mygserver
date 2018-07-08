import bot

a = {
#Учетка №1
	0:{
	#Учетка инстаграм
		'i_login':'xinomorl',
		'i_password': 'vfVFcgb123',
		#Учетка biglike
		'b_login' : 0,
		'b_password': 0,
		#токен вк
		'_t' : 0
	}, #Учетка №2
	1:{
	#Учетка инстаграм
		'i_login' : '',
		'i_password' : '',
		#Учетка biglike
		'b_login' : 0,
		'b_password': 0,
		#токен вк
		'_t' : 0
	},
	#Учетка №3
	2:{
		#Учетка инстаграм
		'i_login' : '',
		'i_password' : '',
		#Учетка biglike
		'b_login' : 0,
		'b_password': 0,
		#токен вк
		'_t' : 0
	}
	,
	#Учетка №3
	3:{
		#Учетка инстаграм
		'i_login' : '',
		'i_password' : '',
		#Учетка biglike
		'b_login' : 0,
		'b_password': 0,
		#токен вк
		'_t' : 0
	}
}

n = int(input("Введите номер учетной записи (0 или 1): "))
i_link = 'https://www.instagram.com/' + a[n]['i_login'] + '/'
b = bot.biglike(i_link,a[n]['i_login'],a[n]['i_password'],a[n]['b_login'],a[n]['b_password'],a[n]['_t'])
if (b.set()=="OK"):
	count = 1
	while count != 0:
		count = int(input("Количество задач, count = : "))
		if count=="": count=30
		type = input("Введите 1 - если будем работать вк и в инсте, 0 - только в инсте: ")
		if type == "": type=1
		b.go(int(type),int(count))

