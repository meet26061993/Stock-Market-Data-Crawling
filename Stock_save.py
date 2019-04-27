# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib2
from bs4 import BeautifulSoup
import bs4 as bs
import pickle
import requests
import xlwt 
wb = xlwt.Workbook() 
sheet1 = wb.add_sheet('Sheet 1') 
tickers = []
def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text
        ticker= ticker.encode('ascii', 'ignore')
        tickers.append(ticker)
       
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
     
    return tickers

save_sp500_tickers()
print tickers 
row_number=1

for n in range(len(tickers)):
    stock= "https://finance.yahoo.com/quote/"+tickers[n]+"/key-statistics?p="+tickers[n]+"&.tsrc=fin-srch"
    
    page = urllib2.urlopen(stock)
    soup = BeautifulSoup(page,'lxml')
    csv_data = []
    
    
    tags = soup('td')
    for tag in tags:
        inner_text = tag.text
        strings = inner_text.split("\n")
    
        csv_data.extend([string for string in strings if string])
    values=[]
    number=1
    for n in range(len(csv_data)):
        if n%2!=0:
            csv_data[n]=csv_data[n].encode('ascii','ignore')
            values.insert(number,str(csv_data[n]))
            number=number+1
    
    print values
    column_number=1
    
    for value in values:
        sheet1.write(row_number,column_number,value)
        column_number=column_number+1
    row_number=row_number+1
    wb.save('xlwt example.xls')
wb.save('xlwt example.xls') 
