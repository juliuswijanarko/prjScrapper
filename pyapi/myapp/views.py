from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from datetime import timedelta
import time
import requests
from bs4 import BeautifulSoup
import json

# Create your views here.

def get_tr(request, user, pss):
	if request.method == 'GET':
		usr = user
		ps = pss

		locl = time.localtime()
		last1mon = date(locl.tm_year, locl.tm_mon, 1) - timedelta(1)
		first1mon = last1mon.replace(day=1)
		first1mon = first1mon.strftime("%m-%d-%Y")
		last1mon = last1mon.strftime("%m-%d-%Y")
		last1min = first1mon[3:5]+first1mon[0:2]
		last1max = last1mon[3:5]+last1mon[0:2]

		headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
		}

		login_data = {
		"value(actions)": "login",
		'value(user_id)': usr,
		'value(user_ip)': '202.80.216.24',
		'value(browser_info)': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
		'value(mobile)': 'false',
		'value(pswd)': ps,
		'value(Submit)': 'LOGIN'
		}
		get_data1 = {
		'value(D1)': '0',
		'value(r1)': '2',
		'value(x)': '1',
		'value(fDt)': last1min,
		'value(tDt)': last1max,
		'value(submit1)': 'Lihat Mutasi Rekening'
		}
		log_out = {
		'value(actions)': 'logout'
		}

		with requests.Session() as c:
		    url = 'https://ibank.klikbca.com/authentication.do'
		    url2 = 'https://ibank.klikbca.com/accountstmt.do?value(actions)=acctstmtview'
		    r = c.get(url, headers=headers)
		    r = c.post(url, data = login_data, headers=headers)

		    r = c.post(url2, data = get_data1, headers=headers)
		    soup = BeautifulSoup(r.content,"lxml")
		    month1 = soup.find_all("font")

		    c.post('https://ibank.klikbca.com/authentication.do?value(actions)=logout', data = log_out, headers = headers)

		    return_data1 = {
		    "dataOf": month1[1].get_text()[1:],
		    "accNo": month1[4].get_text(),
		    "name": month1[7].get_text().rstrip(),
		    "period": month1[10].get_text(),
		    "currency": month1[13].get_text(),
		    "transaction": list(),
		    "startingBal": month1[len(month1)-11].get_text(),
		    "totalCredits": month1[len(month1)-8].get_text(),
		    "totalDebits": month1[len(month1)-5].get_text(),
		    "endBal": month1[len(month1)-2].get_text()
		    }

		    for itr in range (19, len(month1)-14, 6):
		        return_data1['transaction'].append({
		        "date": month1[itr].get_text()[1:],
		        "detail": month1[itr+1].get_text()[1:],
		        "branch": month1[itr+2].get_text()[1:],
		        "amount": month1[itr+3].get_text()[1:],
		        "bal": month1[itr+5].get_text()[1:]  
		        })

		    dtos1 = json.dumps(return_data1)
		    jsn1 = json.loads(dtos1)
		    jsn_trns = json.dumps(jsn1, indent=4, sort_keys=True)


		    return HttpResponse(jsn_trns, content_type='text/json')