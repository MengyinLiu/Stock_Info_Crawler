import json
import sys
import re
import urllib
from bs4 import BeautifulSoup

def contractAsJson(filename):
    soup=BeautifulSoup(open(filename))

##find current_price
    current_price=float(soup.find(id=re.compile('yfs_l84_')).text)
    #print current_price

###find url of data
    
    date=[]    
    for dates in soup.findAll('a'):
        if '&amp;m=' in str(dates):
            url = re.findall('["](.+)["]', str(dates))       
            date.append('http://finance.yahoo.com' + url[0])        
    print date

###find detailed info of contract

    detail_list=[]
    for x in soup.findAll('td', class_=re.compile('yfnc_')) :
        detail_list.append(x.text)
    del detail_list[-1]
    #for x in soup.findAll('td', class_=re.compile('yfnc_tabledata1')):
        #detail_list.append(x.text)        
    #print detail_list
    #print len(detail_list)

    contract_detail=[]
    for j in range(len(detail_list)/8):
        lst=[]
        for i in range(0,8):          
            lst.append(detail_list[i+8*j].encode('utf-8'))            
        contract_detail.append(lst)
    #print contract_detail,len(contract_detail)

    optionQuotes = []
    for item in contract_detail:
        dic=dict()
        dic['Ask']=item[5]
        dic['Bid']=item[4]
        dic['Change']=item[3]
        dic['Date']=re.findall('[A-Z]+([0-9]+)[C,P][0-9]+',item[1])[0]
        dic['Last']=item[2]
        dic['Open']=item[7]
        dic['Strike']=item[0]
        dic['Symbol']=re.findall('([A-Z]+)[0-9]+[C,P][0-9]+',item[1])[0]
        dic['Type']=re.findall('[A-Z]+[0-9]+([C,P])[0-9]+',item[1])[0]      
        dic['Vol']=item[6]
        optionQuotes.append(dic)
    #print optionQuotes

    optionQuotes.sort(lambda x, y: int(y['Open'].replace(',', '' ))-int(x['Open'].replace(',', '')) )

    jsonQuoteData = json.dumps({"currPrice":current_price, "dateUrls":date, "optionQuotes":optionQuotes},sort_keys=True, indent=4) 
    
    return jsonQuoteData

contractAsJson('f.dat')
