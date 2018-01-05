# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 19:09:56 2017

@author: ASHISH SETHIA
"""

   
def change_header():  
    
    from fake_useragent import UserAgent
    ua = UserAgent()
    headers = {'user-agent': ua.random}
    return headers

def get_DataFrame(stock_split_info_list):
    
    import pandas as pd
    cols=["Stock Name","Symbol","Sector","Old FV","New FV","Split-Date"]
    df = pd.DataFrame(stock_split_info_list, columns=cols)
    
    return df


def get_split_data(soup):

    split_ratio_info=[]
    temp=[]
    j=1
        
    for tag in soup.find_all(class_="dvd_brdb", align="center"):
        temp.append(tag.text)        
        if j%3==0:            
            split_ratio_info.append(temp)
            temp=[]        
        j+=1
        
    split_ratio_info=split_ratio_info[1:]      
    return split_ratio_info  


def get_stock_info(url,headers) :
    
    from bs4 import BeautifulSoup 
    import urllib.request
    
    
    # Make a BeautifulSoup Object
    req = urllib.request.Request(url=url,data=b'None',headers=headers)
    sauce=urllib.request.urlopen(req).read()
    soup=BeautifulSoup(sauce,'lxml')
    
    # To fetch symbol,sector,name
    for tag1 in soup.find_all(class_="FL gry10"):
            symbol=tag1.text.split('|')[1].split(':')[1]
            if symbol == '  ' :
                symbol='NA'
            sector=tag1.text.split('|')[3].split(':')[1]
                            
    for tag2 in soup.find_all('h1', class_="b_42"): 
            name=tag2.text 
            
            
    return[name,symbol,sector]           
    
    

def get_stock_split_info(url,headers):
    
    from bs4 import BeautifulSoup 
    import urllib.request
    import re
    
    # Make a BeautifulSoup Object
    req = urllib.request.Request(url=url,data=b'None',headers=headers)
    sauce=urllib.request.urlopen(req).read()
    soup=BeautifulSoup(sauce,'lxml')
    
    # This list will contain the OLD and NEW Face Value and split-date of stock
    split_ratio_info=[]  
    split_ratio_info=get_split_data(soup)
    
    
    # To get the stock name,symbol and sector from an hyperlink of a given stock
    stock_info=[]
    for tag in soup.find_all(class_="bl_12",href=re.compile("/india/stockpricequote")):
        hyperlink_url='http://www.moneycontrol.com' + tag.get('href')
        stock_info.append(get_stock_info(hyperlink_url,headers))
        
        
        
    # Merge stock_info & split_ratio_info into 1 list
    stock_split_info_list=[ x+y for x,y in zip(stock_info,split_ratio_info)]   
       
    
    return stock_split_info_list


if __name__ == "__main__":
    
    import time
    print("This program is to find the Stock-Split information of Indian stocks .")
    print("The data is fetched from MoneyControl.com.")
    
    # Import all required libraries
    
        
    start_time=time.time()
    
    
    # Url address for stock split from Money-Control website 
    url= 'http://www.moneycontrol.com/stocks/marketinfo/splits/index.php'
    
    # Change header param while call to website    
    headers=change_header()
    
    # Call to website mentioned in url1 along with header.This function will return a 
    # list  containing stock name,symbol,sector ,split ratio,split date. 
    
    
    stock_split_info_list=list()    
    stock_split_info_list=get_stock_split_info(url,headers)
    
    df=get_DataFrame(stock_split_info_list)
    print(df)
    end_time=time.time()
    
    print("Execution time:",end_time-start_time)  # Without Multi :276.878
    
    
    
    
    
    
    
    








    
