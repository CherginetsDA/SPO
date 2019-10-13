import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sys

if not len(sys.argv) == 1:
	print("use: python ./lab_3.py")
	exit()

url = "http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg"
response = requests.get(url)
page = BeautifulSoup(response.content, "lxml")

dump_folder = sys.argv[0][:sys.argv[0].rfind('/')+1] + "data"
if not os.path.exists(dump_folder):
	os.makedirs(dump_folder)

votes = {'atd':'', 'data':{}}

admin_data = pd.read_html(url,encoding='')[7]
admin_data.columns = ['admin','municipal']
admin_data = admin_data.iloc[1:,:]
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
votes['atd'] = admin_data
admin_data.to_csv(os.path.join(dump_folder, 'main.csv'), sep=';')
main_links = page.find_all('a')
for main_tag in main_links:
	main_link = main_tag.get('href',None)
	if 'region=78'in main_link:
		name = main_tag.text.replace('Выборы депутатов ','').replace('Муниципального ','').replace('Муниципальный ','').replace('муниципальный ','').replace('муниципального ','').replace('Cовета ', '').replace('cовета ', '').replace('Совета ', '').replace('совета ', '').replace('образования ', '').replace('округа ', 'округ ').replace('Санкт-Петербурга ', '').replace('внутригородского ', '').replace('Внутригородского ', '').replace(' шестого созыва', '').strip()
		votes['data'][name] = {'votes':{}}
		region_page = BeautifulSoup(requests.get(main_link).content, "lxml")
		tik_tags = region_page.find_all('option')
		region_tags = region_page.find_all('a')
		for region_tag in region_tags:
			region_link = region_tag.get('href',None)
			if 'type=220'in region_link:
				candidates = []
				for i in range(1,6):
					candidates_link = region_link + '&number=' + str(i)
					try:
						candidates_df = pd.read_html(candidates_link, encoding='')[5].iloc[:,1:]
						candidates_df.columns = ['name','date', 'party', 'okrug', 'drived', 'registered', 'elected']
						candidates.append(candidates_df)
					except:
						pass
				candidates = pd.concat(candidates, axis=0).reset_index().drop('index',axis=1)
				votes['data'][name]['candidates'] = candidates
				candidates.to_csv(os.path.join(dump_folder, ('data_' + name + '_candidates.csv')), sep=';')
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
						okrug_columns = ['parameter', 'overall'] + list(okrug_df.iloc[0,:])[3:]
						candidates_columns = ['name', 'overall'] + list(okrug_df.iloc[0,:])[3:]
						okrug_stats = okrug_df.iloc[1:13,1:]
						candidates_stats = okrug_df.iloc[14:,1:]
						okrug_stats.columns = okrug_columns
						candidates_stats.columns = candidates_columns
						okrug_stats.to_csv(os.path.join(dump_folder, ('data_' + name + '_' + str(okrug) + '_okrug_stats.csv')), sep=';')
						candidates_stats.to_csv(os.path.join(dump_folder, ('data_' + name + '_' + str(okrug) + '_candidates_stats.csv')), sep=';')
						okrug_stats = {'okrug_stats': okrug_stats, 'candidates_stats': candidates_stats}
						votes['data'][name]['votes'][okrug] = okrug_stats