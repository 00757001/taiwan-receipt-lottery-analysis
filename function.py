import re
from bs4 import BeautifulSoup
import requests

def job_by_country(year,month,lock,stat1_area,stat2_area):
    try:
        url = "https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_"+year+month
        html = requests.get(url).content.decode('utf-8')
        soup = BeautifulSoup(html,'html.parser')
        table1 = soup.find('table', {'id':'fbonly'})
        table2 = soup.find('table', {'id':'fbonly_200'})
        addr1 = table1.find_all("td",{'headers':'companyAddress'})
        addr2 = table2.find_all("td",{'headers':'companyAddress2'})
        lock.acquire()# IMPRATIVE
        #歸零 Dictionary
        # stat1_area = stat1_area.fromkeys(stat1_area, 0)
        # stat2_area = stat2_area.fromkeys(stat2_area, 0)
        for add in addr1:
            if add.text[:3] in list(stat1_area.keys()):
                stat1_area[add.text[:3]]+=1
            elif add.text[:3] == "台北市":
                stat1_area["臺北市"]+=1
            elif add.text[:3] == "桃園縣":
                stat1_area["桃園市"]+=1
              
        for add in addr2:
            if add.text[:3] in list(stat2_area.keys()):
                stat2_area[add.text[:3]]+=1
            elif add.text[:3] == "台北市":
                stat2_area["臺北市"]+=1
            elif add.text[:3] == "桃園縣":
                stat2_area["桃園市"]+=1
    finally:
        lock.release()  
def job_by_item(year,month,lock,stat1,stat2):
    try:
        url = "https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_"+year+month
        html = requests.get(url).content.decode('utf-8')
        soup = BeautifulSoup(html,'html.parser')
        table1 = soup.find('table', {'id':'fbonly'})
        table2 = soup.find('table', {'id':'fbonly_200'})
        data1 = table1.find_all("td",{'headers':'tranItem'})
        data2 = table2.find_all("td",{'headers':'tranItem2'})
        lock.acquire()# IMPRATIVE
        #歸零
        # stat1.fromkeys(stat1, 0)
        # stat2.fromkeys(stat2, 0)
        for data in data1:
            count = 0 
            if(re.findall(r'飲|咖啡|鮮|乳|水|麵|湯',data.text)): stat1['飲品']+=1;count+=1
            if(re.findall(r'餐|口|食|蛋|零食|茶|冰|飯',data.text)): stat1['食品']+=1;count+=1
            elif(re.findall(r'手續|停車|收|基本台|市話|電信|金|費|門票|租',data.text)): stat1['繳費']+=1;count+=1
            if(re.findall(r'酒|菸',data.text)): stat1['菸酒']+=1;count+=1
            if(re.findall(r'書|報紙',data.text)): stat1['書籍(報紙)']+=1;count+=1
            if(re.findall(r'服|衣|褲',data.text)): stat1['衣服']+=1;count+=1
            if(re.findall(r'生|文具|應用|化妝|化粧|用品|3C|網路|機|家|玩|鞋|電',data.text)): stat1['生活用品']+=1;count+=1
            if(re.findall(r'油',data.text)): stat1['油品']+=1;count+=1  
            if(count==0):stat1['其他']+=1
        for data in data2:
            count = 0 
            if(re.findall(r'飲|咖啡|鮮|乳|水|麵|湯',data.text)): stat2['飲品']+=1;count+=1
            if(re.findall(r'餐|口|食|蛋|零食|茶|冰|飯',data.text)): stat2['食品']+=1;count+=1
            elif(re.findall(r'手續|停車|收|基本台|市話|電信|金|費|門票|租',data.text)): stat2['繳費']+=1;count+=1
            if(re.findall(r'酒|菸',data.text)): stat2['菸酒']+=1;count+=1
            if(re.findall(r'書|報紙',data.text)): stat2['書籍(報紙)']+=1;count+=1
            if(re.findall(r'衣|服|褲',data.text)): stat2['衣服']+=1;count+=1
            if(re.findall(r'生|文具|應用|化妝|化粧|用品|3C|網路|機|家|玩|鞋|電',data.text)): stat2['生活用品']+=1;count+=1
            if(re.findall(r'油',data.text)): stat2['油品']+=1;count+=1  
            if(count==0):stat2['其他']+=1
    finally:
        lock.release()