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

		#get today date and first date of this month
		today = date.today()
		d1 = today.strftime("%m-%d-%Y")
		thisYear = d1[6:10]
		if d1[0:1] == '0':
		   thisMonth = d1[1:2]
		else:
		   thisMonth = d1[0:2]
		thisDay = d1[3:5]

		locl = time.localtime()
		#get first and last date of last month
		last1mon = date(locl.tm_year, locl.tm_mon, 1) - timedelta(1)
		first1mon = last1mon.replace(day=1)
		first1mon = first1mon.strftime("%m-%d-%Y")
		last1mon = last1mon.strftime("%m-%d-%Y")
		last1min = first1mon[3:5]+first1mon[0:2]
		last1max = last1mon[3:5]+last1mon[0:2]

		#get first and last date of 2 months ago
		last2mon = date(locl.tm_year, locl.tm_mon, 1) - timedelta(int(last1mon[3:5]) + 1)
		first2mon = last2mon.replace(day=1)
		first2mon = first2mon.strftime("%m-%d-%Y")
		last2mon = last2mon.strftime("%m-%d-%Y")
		last2min = first2mon[3:5]+first2mon[0:2]
		last2max = last2mon[3:5]+last2mon[0:2]

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
		get_data = {
		'value(D1)': '0',
		'value(r1)': '1',
		'value(startDt)': '01',
		'value(startMt)': thisMonth,
		'value(startYr)': thisYear,
		'value(endDt)': thisDay,
		'value(endMt)': thisMonth,
		'value(endYr)': thisYear,
		'value(fDt)': '',
		'value(tDt)': '',
		'value(submit1)': 'Lihat Mutasi Rekening'
		}
		get_data1 = {
		'value(D1)': '0',
		'value(r1)': '2',
		'value(x)': '1',
		'value(fDt)': last1min,
		'value(tDt)': last1max,
		'value(submit1)': 'Lihat Mutasi Rekening'
		}
		get_data2 = {
		'value(D1)': '0',
		'value(r1)': '2',
		'value(x)': '2',
		'value(fDt)': last2min,
		'value(tDt)': last2max,
		'value(submit1)': 'Lihat Mutasi Rekening'
		}
		log_out = {
		'value(actions)': 'logout'
		}

		with requests.Session() as c:
		    url = 'https://ibank.klikbca.com/authentication.do'
		    url2 = 'https://ibank.klikbca.com/accountstmt.do?value(actions)=acctstmtview'
		    url3 = 'https://ibank.klikbca.com/balanceinquiry.do'
		    #login
		    r = c.get(url, headers=headers)
		    r = c.post(url, data = login_data, headers=headers)

		    r = c.post(url3, headers=headers)
		    soup = BeautifulSoup(r.content,"lxml")
		    bal = soup.find_all("font")

		    r = c.post(url2, data = get_data, headers=headers)
		    soup = BeautifulSoup(r.content,"lxml")
		    month = soup.find_all("font")

		    r = c.post(url2, data = get_data1, headers=headers)
		    soup = BeautifulSoup(r.content,"lxml")
		    month1 = soup.find_all("font")

		    r = c.post(url2, data = get_data2, headers=headers)
		    soup = BeautifulSoup(r.content,"lxml")
		    month2 = soup.find_all("font")

		    #logout
		    c.post('https://ibank.klikbca.com/authentication.do?value(actions)=logout', data = log_out, headers = headers)

		    useable = {
		    "availableBalance": bal[10].get_text().strip()
		    }

		    return_data = {
		    "dataOf": month[1].get_text()[1:],
		    "accNo": month[4].get_text(),
		    "name": month[7].get_text().rstrip(),
		    "period": month[10].get_text(),
		    "currency": month[13].get_text(),
		    "transaction": list(),
		    "startingBal": month[len(month)-11].get_text(),
		    "totalCredits": month[len(month)-8].get_text(),
		    "totalDebits": month[len(month)-5].get_text(),
		    "endBal": month[len(month)-2].get_text()
		    }

		    for itr in range (19, len(month)-14, 6):
		        return_data['transaction'].append({
		        "date": month[itr].get_text()[1:],
		        "detail": month[itr+1].get_text()[1:],
		        "branch": month[itr+2].get_text()[1:],
		        "amount": month[itr+3].get_text()[1:],
		        "bal": month[itr+5].get_text()[1:]  
		        })

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

		    return_data2 = {
		    "dataOf": month2[1].get_text()[1:],
		    "accNo": month2[4].get_text(),
		    "name": month2[7].get_text().rstrip(),
		    "period": month2[10].get_text(),
		    "currency": month2[13].get_text(),
		    "transaction": list(),
		    "startingBal": month2[len(month2)-11].get_text(),
		    "totalCredits": month2[len(month2)-8].get_text(),
		    "totalDebits": month2[len(month2)-5].get_text(),
		    "endBal": month2[len(month2)-2].get_text()
		    }

		    for itr in range (19, len(month2)-14, 6):
		        return_data2['transaction'].append({
		        "date": month2[itr].get_text()[1:],
		        "detail": month2[itr+1].get_text()[1:],
		        "branch": month2[itr+2].get_text()[1:],
		        "amount": month2[itr+3].get_text()[1:],
		        "bal": month2[itr+5].get_text()[1:]  
		        })

		    tojsn = json.dumps(useable)
		    jsned = json.loads(tojsn)

		    dtos = json.dumps(return_data)
		    jsn = json.loads(dtos)

		    dtos1 = json.dumps(return_data1)
		    jsn1 = json.loads(dtos1)

		    dtos2 = json.dumps(return_data2)
		    jsn2 = json.loads(dtos2)

		    jsn_mrge = [jsned,jsn,jsn1,jsn2]
		    jsn_trns = json.dumps(jsn_mrge, indent=4, sort_keys=True)


		    return HttpResponse(jsn_trns, content_type='text/json')