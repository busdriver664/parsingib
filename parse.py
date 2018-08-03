import urllib.request
from bs4 import BeautifulSoup  
import re
import difflib



education_other = ["Высшее образование", "Высшее техническое образование","Высшее профильное образование", "Техническое образование", " "]



def distance(a, b):# Расстояние левенштейна 
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n+1) # Keep current and previous row, not entire matrix
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1,n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]



def get_html(url):#получаем страницу целиком
    response = urllib.request.urlopen(url)
    return response.read()

def get_nubm(url):# получаем количество страниц с вакансиями
    soup = BeautifulSoup(get_html(url),"html.parser" )#берем страницу целиком
    table2 = soup.find_all("a", class_="bloko-button HH-Pager-Control") #для поиска кол-ва страниц
    num = re.findall(r'\d+', str(table2))#количество страниц с вакансиями
    if not num:
    	return 1
    else:
    	return int(float(num[-1] ))

def parse(html):
    hrefs = []# массив с ссылкми
    soup = BeautifulSoup(html,"html.parser" )#берем страницу целиком
    table = soup.find_all("div",class_="vacancy-serp")#парсинг блока с вакансиями
    pattern = re.compile(r'"vacancyId": "(.*)",')# паттерн для выдергивания id вакансий
    ids = re.findall(pattern, str(table)) # выдергиваем id
    for i in ids:
        hrefs.append(url1+i) # формируем ссылки
    # for i in hrefs:
    #     print(i)
    #     print(hrefs.count(i))
    return hrefs

def parse_vac(html):
    soup = BeautifulSoup(html,"html.parser" )#берем страницу целиком
    name = soup.select('h1')[0].get_text()#название вакансии
    salary = soup.find_all("p", class_="vacancy-salary")
    for i in salary:
        salary = i.get_text()# зарплата
    exp = (soup.find("span",attrs={'data-qa': 'vacancy-experience'})).get_text()# опыт работы
    employment = (soup.find("span",attrs={'itemprop': 'employmentType'})).get_text()# занятость
    schedule = (soup.find("span",attrs={'itemprop': 'workHours'})).get_text()# график
    organization = (soup.find("a",attrs={'itemprop': 'hiringOrganization'})).get_text()# график
    description = soup.find("div",attrs={'class': 'g-user-content'})# описание
    education = ""
    lev_dic = {}
    demands = parse_demands(html)

    #Далее кусок кода, где определяем образование
    for i in demands:
    	if i.lower().find('образование') != 0:
    		for j in education_other:
    			lev_dic[distance(j,i)] = j
    		education = lev_dic[min(lev_dic.keys())]
    		break

    print("Название вакансии:",name,"\nЗарплата:",salary,"\nТребуемый опыт:",exp,"\nЗанятость:",employment,"\nРабочие часы:",schedule,"\nОрганизация:",organization, "\nОбразование:", education)
    print("\nТребования:\n", demands, "\n")


    

def parse_demands(vac):#парсинг требований
	soup = BeautifulSoup(vac,"html.parser" )#берем страницу целиком (vac - html-страница с вакансией)
	description = soup.find("div",attrs={'class': 'g-user-content'})# блок с описаниен

	if not description: # если другая бля*ская разметка
		description = soup.find("div",attrs={'class': 'vacancy-branded-user-content', 'itemprop' : 'description'})# бля*ский блок с описаниен
	

	demand_trigger = False # триггер для записи требований
	demands = []# исходный массив требований
	demands1 = []# конечный массив требований
	for i in description:
			if str(i).find('strong') != -1 and (str(i).lower()).find('требования') != -1:
				demand_trigger = True 
				continue
			if str(i).find('strong') != -1 and (str(i).lower()).find('требования') == -1:
				demand_trigger = False
			if demand_trigger == True:
				demands.append(i)		
	for i in demands:
		if str(type(i)) == "<class 'bs4.element.Tag'>": # избавляемся от тегов
			demands1.append(i.get_text())
			#demands1.append(str(i))
	# for i in demands1:
	#  	print(i, '\n\n')
	return demands1






vacs = []# все вакансии на сайте
url22 = "https://omsk.hh.ru/search/vacancy?text=%D0%90%D0%BB%D0%BA%D0%BE%D0%B3%D0%BE%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%BA%D0%BE%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D1%8F&enable_snippets=true&clusters=true&area=68&page="
#url = "https://omsk.hh.ru/search/vacancy?text=%D0%98%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F+%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D1%8C&enable_snippets=true&clusters=true&area=68&page="# url страницы с вакнсиями
url1 = "https://omsk.hh.ru/vacancy/"# страница конкретной вакансии
for i in range(get_nubm(url22+"0")):#
    html = get_html(url22+str(i))
    vacs.append(parse(html))
for i in vacs:
    for j in i:
        parse_vac(get_html(j))































