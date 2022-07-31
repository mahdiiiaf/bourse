from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager import chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup 
from selenium.common.exceptions import WebDriverException
from urllib.parse import quote,unquote
import urllib.request

import os 
import pickle


data_directory=r"C:\Users\Asus\Downloads\code\data"
data_list=os.listdir(data_directory)
if "hist.pkl" not in data_list :
	hist={}
else :
	hist=pickle.load(open(rf"{data_directory}\hist.pkl","rb"))



if True:
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument('--ignore-ssl-errors=yes')
	options.add_argument('--ignore-certificate-errors')
	options.add_experimental_option("prefs",{"download.default_directory":r"data\statements"})

	#options.add_argument("user-data-dir=C:\\Users\\Asus\\python-virtual-environments\\env")
	#options.add_argument(f"user-data-dir={cwd}\driver")

driver = webdriver.Chrome(r"C:\Users\Asus\Downloads\New folder (7)\driver\chromedriver.exe",options=options, service_args=["--verbose", "--log-path=D:\\qc1.log"])



def down_data(comp="نوری",num=1):
	
	data_directory=r"C:\Users\Asus\Downloads\code\data"
	data_list=os.listdir(data_directory)
	company_name=quote(comp)

	if comp not in hist :
		hist[comp]=[]

	for i in range(num):

		page_number=i+1
		if page_number not in hist[comp]:
			link=f"https://search.codal.ir/api/search/v2/q?&Audited=true&AuditorRef=-1&Category=-1&Childs=true&CompanyState=0&CompanyType=1&Consolidatable=true&IsNotAudited=false&Isic=341010&Length=-1&LetterType=-1&Mains=true&NotAudited=true&NotConsolidatable=true&PageNumber={page_number}&Publisher=false&Symbol={company_name}&TracingNo=-1&search=true"

			driver.get(link)

			parse=BeautifulSoup(driver.page_source,features="xml")
			excel_url=parse.find_all("ExcelUrl")
			title_name=parse.find_all("Title")
			for k,l in zip(excel_url,title_name): 
				if k.text!="" and ( "صورت‌های" in l.text ):	
					print(l.text,"\n",k.text,"\n---------------------------------------------------")
					####### I should check some cases
			for k,l in zip(excel_url,title_name):	
				if k.text!="" and ( "صورت‌های" in l.text ):
					sal=""
					mah=""
					for (c,p) in enumerate(l.text):
						if p.isdigit():
							if l.text[c+2]!="م":
								sal+=p
							else :
								mah+=p

					sub=""
					if "سال مالی" in  l.text:
						if "حسابرسی شده" in l.text:
							if "اصلاحیه" in l.text:
								sub="sal-hesab-eslah"
							else :
								sub="sal-hesab"
						elif "حسابرسی نشده" in l.text:	
							sub="sal-bihesab"

					elif "میاندوره‌ای" in  l.text:
						if "حسابرسی شده" in l.text:

							sub="mian-hesab"
						elif "حسابرسی نشده" in  l.text:
							sub="mian-bihesab" 

					direct=f"{comp}_{sub}_{sal}.xls" if mah=="" else f"{comp}_{sub}_{sal}_{mah}.xls"
					

					if direct not in data_list:
						urllib.request.urlretrieve(k.text,rf"{data_directory}\{direct}")

			hist[comp].append(page_number)
					
