import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

def url_pars():
    headers_gen = Headers(os='win', browser='chrome')
    url ='https://spb.hh.ru/search/vacancy?area=2&area=1&enable_snippets=true&order_by=publication_time&ored_clusters=true&text=Python+django+flask&search_period=7&page=0'
    response = requests.get(url=url, headers=headers_gen.generate())   
    data = response.text   
    soup = BeautifulSoup(data, 'lxml')

    return soup

def parser(soup):  
    data_tag = soup.find('main', class_='vacancy-serp-content')
    vacancy_tage = data_tag.find_all('div', class_='vacancy-serp-item__layout')
    list_link = []
    for data in vacancy_tage:
        header = data.find('h3')
        a_tag = header.find('a')
        link = a_tag['href']
        list_link.append(link)
        
    return list_link
        
       
        
def main(link): 
    headers_gen = Headers(os='win', browser='chrome')
    list_data =[]
    data_vacancy = {}
         
    for data in link:
        # создаем словарь с ключами
        data_vacancy = dict.fromkeys(['link', 'salary', 'name', 'city'])
        # получаем данные по сылкам вакансий
        vacancy = requests.get(data, headers=headers_gen.generate()).text
        vacancy_soup = BeautifulSoup(vacancy, 'lxml')     
        vacancy_name = vacancy_soup.find('h1')
        # подгчаем название компании
        company = vacancy_soup.find('div', class_='vacancy-company-details')
        # записываем в словарь ссылку и название компаниии
        data_vacancy['link'] =  data
        data_vacancy['name'] =  company.text
        # получаем зарплату
        maney = vacancy_soup.find('span', attrs={'class':'bloko-header-section-2 bloko-header-section-2_lite', 'data-qa':"vacancy-salary-compensation-type-net"})
        # записываем в словарь зарплатную вилку
        if maney:
            data_vacancy['salary'] =  maney.text
        else:
            data_vacancy['salary'] =  'зарплата не указана'
        # получаем название города
        city_tag = vacancy_soup.find('div', class_='vacancy-company-redesigned')
        city_p = city_tag.find('p')
        city_s = city_tag.find('a', attrs={'class':'bloko-link bloko-link_kind-tertiary bloko-link_disable-visited','data-qa':"vacancy-view-link-location",'target':"_blank"})
        # записываем в словарь название города
        if city_p:
            data_vacancy['city'] = city_p.text       
        else:
            data_vacancy['city'] =  city_s.text
            
        list_data.append(data_vacancy) 
            
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(list_data, f, indent=4, ensure_ascii=False)            
        

if __name__ == '__main__':
    pars = url_pars() 
    link = parser(pars)
    main(link)
    
    
       