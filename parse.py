import urllib.request as ulib
from urllib.parse import quote
from bs4 import BeautifulSoup 
import argparse 
import re


def get_html(url):#получаем страницу целиком
    response = ulib.urlopen(url)
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
    demands = parse_demands(html)


    print("Название вакансии:",name,"\nЗарплата:",salary,"\nТребуемый опыт:",exp,"\nЗанятость:",employment,"\nРабочие часы:",schedule,"\nОрганизация:",organization)
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
	# 	print(i, '\n')
	return demands1



mode = argparse.ArgumentParser(description='find vacancy by name')
mode.add_argument("--name", dest="name",default="информационная безопасность", type=str, help="add name here")
args=mode.parse_args()



vacs = []# все вакансии на сайте
url = "https://omsk.hh.ru/search/vacancy?text={}&enable_snippets=true&clusters=true&area=68&page=".format(quote(args.name))# url страницы с вакнсиями
url1 = "https://omsk.hh.ru/vacancy/"# страница конкретной вакансии
for i in range(get_nubm(url+"0")):#
    html = get_html(url+str(i))
    vacs.append(parse(html))
for i in vacs:
    for j in i:
        parse_vac(get_html(j))































