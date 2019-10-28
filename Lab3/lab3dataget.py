import pandas as pd
from bs4 import BeautifulSoup
import requests

def ls2f(str_list):# list string to float
    return list(map(lambda x: float(x), str_list))

def get_main_url():
    return "http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg"

def get_page_from_url(url = get_main_url()):
    response = requests.get(url)
    return BeautifulSoup(response.content, "lxml")

def get_table_name():
    response = requests.get(get_main_url())
    admin_data = pd.read_html(get_main_url(),encoding='')[7]
    admin_data.columns = ['admin','municipal']
    admin_data = admin_data.iloc[2:,:]
    admin_data = admin_data.fillna(method='ffill')
    admin_data['municipal'] = admin_data['municipal'].str.replace('Выборы депутатов ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('Муниципального ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('муниципального ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('Муниципальный ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('муниципальный ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('совета ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('Совета ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('cовета ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('Cовета ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('образования ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('округа ', 'округ ')
    admin_data['municipal'] = admin_data['municipal'].str.replace('Санкт-Петербурга ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('внутригородского ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace('Внутригородского ', '')
    admin_data['municipal'] = admin_data['municipal'].str.replace(' шестого созыва', '')
    admin_data['municipal'] = admin_data['municipal'].str.strip()
    admin_data['admin'] = admin_data['admin'].str.replace('город Санкт-Петербург ','')
    admin_data['admin'] = admin_data['admin'].str.strip()
    return admin_data

def get_districts_name():
    response = requests.get(get_main_url())
    admin_data = pd.read_html(get_main_url(),encoding='')[7]
    admin_data = admin_data.fillna(' ')
    admin_data = admin_data.iloc[2:,:1]
    admin_data = admin_data[admin_data[0] != ' ']
    return admin_data[0]

def get_district_site(district):
    dist_names = get_table_name()
    result = {}
    for dist_name in dist_names[list(map(lambda a: district in a, dist_names['admin']))]['municipal']:
        dist_name = dist_name.replace('округ ','')
        result[dist_name] = get_area_site(dist_name)
    return result

def get_area_site(area):
    admin_data = get_table_name()
    page = get_page_from_url()
    main_links = page.find_all('a')
    afp = next(x for x in main_links if area in x.text)
    area_page = BeautifulSoup(requests.get(afp.get('href',None)).content, "lxml")
    tik_tags = area_page.find_all('option')
    all_okrug = {}
    for tik_tag in tik_tags:
        tik_link = tik_tag.get('value',None)
        if tik_link is not None:
            okrug = int(tik_tag.text[:tik_tag.text.find(" ")])
            tik_page = BeautifulSoup(requests.get(tik_link).content, "lxml")
            okrug_tags = tik_page.find_all('a')
            for okrug_tag in okrug_tags:
                okrug_link = okrug_tag.get('href',None)
                if 'type=424'in okrug_link:

                    dd = pd.read_html(okrug_link,encoding='cp1251')
                    okrug_df = pd.concat([dd[6], dd[7]], axis=1)
                    # okrug_df.iloc[0,1] = 'param/name'
                    all_okrug[tik_tag.text[tik_tag.text.find('№')+1:]] = okrug_df.iloc[:,1:]
    return all_okrug
