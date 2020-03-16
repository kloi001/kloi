from django.shortcuts import render
from django.http import  HttpResponse, QueryDict, HttpResponseRedirect, Http404, JsonResponse
from .models import userinputs
import time
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import csv
import json
import pandas as pd
import random
from .forms import userprofileform

def userprofile(request):
	user_job = request.GET.get('user_job', None)
	user_study = request.GET.get('user_study', None)
	user_interest = request.GET.get('user_interest', None)
	context_data = {'user_job' : user_job,
					'user_study': user_study,
					'user_interest': user_interest
	}

	if user_job is None:
			return render(request, 'stockexplorer/userprofile.html', context=context_data)

	with pd.ExcelFile('stockexplorer/static/Projectdata.xlsx') as xlsx:
	    df1 = pd.read_excel(xlsx, 'Professions')
	    df2 = pd.read_excel(xlsx, 'Education')
	    df3 = pd.read_excel(xlsx, 'Hobbies')

	sector_name_1 = df1[df1['Profession'] == str(user_job)]['Relevant Sector']
	sector_name_2 = df2[df2['Education'] == str(user_study)]['Relevant Sector']
	sector_name_3 = df3[df3['Interests'] == str(user_interest)]['Relevant Sector']
	sector_name_1 = list(sector_name_1)
	sector_name_2 = list(sector_name_2)
	sector_name_3 = list(sector_name_3)
	industries_1 = sector_name_1[0]
	industries_2 = sector_name_2[0]
	industries_3 = sector_name_3[0]
	sector_name_1 = industries_1.split(', ')
	sector_name_2 = industries_2.split(', ')
	sector_name_3 = industries_3.split(', ')

	#this generates 3 random sectors of interest
	sector_list = [random.choice(sector_name_1),random.choice(sector_name_2),random.choice(sector_name_3)]

	#this saves sector interests in a json for display
	sector_list.to_json(r'stockexplorer/static/sector_interest.json')

	#this preps the sector_list for web scrapping
	sector_list = [s.replace(' ', '') for s in sector_list]

	#this creates a list for the 3 recommended stocks
	stock_exp_info = ["ticker_key"]
	stock_exp = pd.DataFrame(columns=stock_exp_info)

	for x in sector_list:
		try:
			url_screen = 'https://finviz.com/screener.ashx?v=111&f=cap_largeover,idx_sp500,ind_' + x +'&o=-marketcap'
			res = requests.get(url_screen)
			soup = BeautifulSoup(res.content, 'html.parser')
			ticker = soup.find_all(class_="screener-link-primary")
			stock = soup.find_all(class_="screener-link")

			company_name_ticker = stock[1].get_text() + "(" + ticker[0].get_text() + ")"

			ticker_name = ticker[0].get_text()

	        #for each ticker, go to database and pick out and show Company Profile, MarCap, Div, SharesOut, SharesFloat, PrevClose

			with open('stockexplorer/static/stockdata.json') as json_file:
				data = json.load(json_file)

			def get_key(val):
				for key, value in data['ticker'].items():
					if val == value:
						return key

			stock_exp_data = pd.DataFrame([[key]],columns=stock_exp_info)
			stock_exp = stock_exp.append(stock_exp_data, ignore_index=True)

		except Exception as e:
			url_screen = 'https://finviz.com/screener.ashx?v=111&f=cap_largeover,idx_sp500&o=-marketcap'
			res = requests.get(url_screen)
			soup = BeautifulSoup(res.content, 'html.parser')
			ticker = soup.find_all(class_="screener-link-primary")
			stock = soup.find_all(class_="screener-link")

			company_name_ticker = stock[1].get_text() + "(" + ticker[0].get_text() + ")"

			ticker_name = ticker[0].get_text()

	        #for each ticker, go to database and pick out and show Company Profile, MarCap, Div, SharesOut, SharesFloat, PrevClose

			with open('stockexplorer/static/stockdata.json') as json_file:
				data = json.load(json_file)

			def get_key(val):
				for key, value in data['ticker'].items():
					if val == value:
						return key

			stock_exp_data = pd.DataFrame([[key]],columns=stock_exp_info)
			stock_exp = stock_exp.append(stock_exp_data, ignore_index=True)

		#this saves dataframe of 3 ticker keys into json
		stock_exp.to_json(r'stockexplorer/static/stock_keys.json')


		context = {'sector_x': random.choice(sector_name_1),
			   'sector_y': random.choice(sector_name_2),
			   'sector_z': random.choice(sector_name_3),
			   'stock_exp': stock_exp,
			   }
