"""
Le bot de scraping 
------------------

Il s'occupe d'aller chercher tous les éléments nécéssaires pour créer la vidéo (data, images et audio)
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.opera import OperaDriverManager
from selenium.webdriver import ActionChains as A
from selenium.webdriver.common.keys import Keys as K
from selenium.webdriver.support.ui import Select
from PIL import ImageGrab as IG
import os 
import shutil
import time as tm 
from binance.client import Client
from binance.enums import *
import config
import pandas as pd
from datetime import date
import text



#suppression des affichages de webdriver-manager
os.environ['WDM_LOG_LEVEL'] = '0'
os.environ['WDM_PRINT_FIRST_LINE'] = 'False'



class Scraper_bot() : 


	def __init__(self,name) : 
		self.name = name

		#scraping with selenium
		options = webdriver.ChromeOptions()
		options.add_argument("--start-maximized")
		#options.add_argument('headless')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.browser  = webdriver.Chrome(ChromeDriverManager().install(),options=options) #maybe shoud i've call it driver
		self.action = A(self.browser)
		self.text = ""

		#scraping with binance API
		self.client = Client(config.API_KEY, config.API_SECRET, tld='com')
		self.BTC_100 = 0
		self.BTC_50 = 0
		self.BTC_21 = 0
		self.BTC_close = 0 
		self.ETH_100 = 0
		self.ETH_50 = 0
		self.ETH_21 = 0
		self.ETH_close = 0 


	def __repr__(self) : 
		return "Bonjour, je suis " + self.name +" un bot de scraping, grâce à moi il y aura du contenu dans les videos."

	def get_graphs(self) : 

		#aller au graph du bitcoin
		self.browser.get("https://fr.tradingview.com/chart/wKKdRRLf/")
		tm.sleep(5)
		#accepter les cookies
		bouton = self.browser.find_elements_by_class_name("button-1iktpaT1")
		bouton[0].click()
		tm.sleep(5)
		#Capturer le graph
		screenshot("BTC_graph")

		#recommencer avec ether
		self.browser.get("https://fr.tradingview.com/chart/DodBP3Yj/")
		tm.sleep(5)
		screenshot("ETH_graph")
		tm.sleep(5)


	def get_actual_data(self) : 
		"""A function aimed to get the current price of ETH and BTC"""

		#call to Binance API
		raw_data = self.client.get_all_tickers()
		#tighting up data in a panda frame
		data_frame = pd.DataFrame(raw_data)
		data_frame.set_index('symbol', inplace=True)
		self.BTC = float(data_frame.loc['BTCUSDT'].price)
		self.ETH = float(data_frame.loc['ETHUSDT'].price)
		
	def get_historical_data(self,PAIR):
		"""A function aimed to get some historical value and to calculate mooving averages"""
		#FIXME : in fact we could also use it to get actual data

		#call to Binance API
		historical = self.client.get_historical_klines(PAIR,Client.KLINE_INTERVAL_1DAY,"1 jan 2021")
		#tighting up data in a panda frame
		data_frame = pd.DataFrame(historical)
		data_frame.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume' ,'Close Time', 'QAV', \
		'Number of Trades','TBBV','TBQV',"Ignore"]
		numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume','QAV', 'Number of Trades','TBBV','TBQV']
		data_frame[numeric_columns] = data_frame[numeric_columns].apply(pd.to_numeric,axis=1)
		#only for learning purpose
		data_frame['Open Time'] = pd.to_datetime(data_frame['Open Time']/1000, unit = 's')
		data_frame['Close Time'] = pd.to_datetime(data_frame['Close Time']/1000, unit = 's')

		return(data_frame['Close'][-100:].mean(),\
			data_frame['Close'][-50:].mean(),\
			data_frame['Close'][-21:].mean(),\
			data_frame['Close'][-2:-1].mean())

	def get_account(self) : 
		"""
		A function aimed to get an account on Notevibes.
		It's free to use for a short time so we create a new account each time
		"""

		#reset browser
		options = webdriver.ChromeOptions()
		options.add_argument("--start-maximized")
		#options.add_argument('headless')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.browser  = webdriver.Chrome(ChromeDriverManager().install(),options=options) #maybe shoud i've call it driver
		self.action = A(self.browser)

		#set a new browser to remember temp email 
		options_bis = webdriver.ChromeOptions()
		options_bis.add_argument("--start-maximized")
		#options_bis.add_argument('headless')
		options_bis.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.browser_bis  = webdriver.Chrome(ChromeDriverManager().install(),options=options_bis)
		self.action_bis = A(self.browser_bis)
	

		#get a temporal email
		self.browser.get("https://www.crazymailing.com/fr/")
		tm.sleep(5)
		self.action.key_down(K.CONTROL).send_keys("c").perform()


		#use it to register on notevibes
		self.browser_bis.get("https://notevibes.com/cabinet/")
		tm.sleep(5)
		boutons = self.browser_bis.find_elements_by_class_name("firebaseui-idp-button")
		boutons[2].click()
		self.action_bis.key_down(K.CONTROL).send_keys("v").perform()
		boutons = self.browser_bis.find_elements_by_class_name("firebaseui-id-submit")
		boutons[0].click()
		tm.sleep(5)
		self.browser_bis.close()

		#back on temporal email to activate account
		tm.sleep(30)
		boutons = self.browser.find_elements_by_class_name("close")
		boutons[0].click()
		tm.sleep(5)
		mails = self.browser.find_elements_by_class_name("first_td")
		mails[0].click()
		tm.sleep(5)
		boutons = self.browser.find_elements_by_class_name("close")
		boutons[0].click()
		tm.sleep(5)
		#save email adress
		elements = self.browser.find_elements_by_class_name("to")
		self.email = elements[0].text[4:-1]
		#access to mail content in another frame
		self.browser.switch_to.frame("mess_frame")
		links = self.browser.find_elements_by_partial_link_text("ign")
		self.action.click(links[0]).perform()
		#access the new tab 
		tm.sleep(5)
		self.browser.switch_to.window(self.browser.window_handles[1])
		#paste again the email an enter notevibes
		tm.sleep(5)
		inputs = self.browser.find_elements_by_class_name("mdl-textfield__input")
		inputs[0].send_keys(self.email)
		tm.sleep(5)
		boutons = self.browser.find_elements_by_class_name("firebaseui-id-submit")
		boutons[0].click()
		tm.sleep(5)



	def get_voice(self,text) : 
		"""A function aimed to get the voice of the robot, based on the different text it has to say"""

		#select the good voices

		#FIXME : here it bugs sometime so we add a loop to retry 
		try :
			self.select = Select(self.browser.find_element_by_id("voice"))
		except : 
			print("retrying")
			self.retry() 
		self.select.select_by_value("fr-FR-Wavenet-B")
		form = self.browser.find_element_by_id("editor")
		form.send_keys(text)
		submit = self.browser.find_element_by_id("btnSubmit")
		submit.click()
		tm.sleep(3)
		dwl = self.browser.find_elements_by_class_name("btn-primary")[0]
		dwl.click()
		tm.sleep(5)
		self.browser.close()
		tm.sleep(2)
		self.browser.switch_to.window(self.browser.window_handles[0])
		self.browser.close()

	def retry(self):
		inputs = self.browser.find_elements_by_class_name("mdl-textfield__input")
		inputs[0].send_keys(self.email)
		tm.sleep(5)
		boutons = self.browser.find_elements_by_class_name("firebaseui-id-submit")
		boutons[0].click()
		tm.sleep(3)
		try :
			self.select = Select(self.browser.find_element_by_id("voice"))
		except : 
			print("retrying")
			self.retry() 


	
	def get_news(self): 
		"""A function aimed to get the latest news from "journal du coin", and add it to the text"""

		#Bitcoin
		self.browser.get("https://journalducoin.com/bitcoin/actualites-bitcoin/")
		articles = self.browser.find_elements_by_class_name("bloc-article-list__item")
		i = 0
		self.text_news = text.NEWS
		for article in articles :
			if i < 3 :
				self.text_news += "article numéro " + str(i) + "... " + article.text[:-16] + "..."
			i+=1

		#Etherum
		self.browser.get("https://journalducoin.com/ethereum/actualites-ethereum/")
		articles = self.browser.find_elements_by_class_name("bloc-article-list__item")
		i = 0
		self.text_news += text.NEWS2
		for article in articles :
			if i < 3 :
				self.text_news += "article numéro " + str(i) + "... " + article.text[:-16] + "..."
			i+=1


		#Altcoins
		self.browser.get("https://journalducoin.com/altcoins/actualites-altcoins/")
		articles = self.browser.find_elements_by_class_name("bloc-article-list__item")
		i = 0
		self.text_news += text.NEWS3
		for article in articles :
			if i < 2 :
				self.text_news += "article numéro " + str(i) +  "... " +article.text[:-16] + "..."
			i+=1

		#DE-FI
		self.browser.get("https://journalducoin.com/defi/actualites-defi/")
		articles = self.browser.find_elements_by_class_name("bloc-article-list__item")
		i = 0
		self.text_news += text.NEWS4
		for article in articles :
			if i < 2 :
				self.text_news += "article numéro " + str(i) + "... " + article.text[:-16] + "..." 
			i+=1

		#OUTRO
		self.text_news += text.OUTRO
		print(self.text_news)

		


	def get_text_graphs(self):
		"""A function aimed to get the text of the video"""

		#Bitcoin
		self.text += text.INTRO + text.BTC
		if self.BTC >= self.BTC_close :
			self.text += text.VERT 
		else :
			self.text += text.ROUGE
		self.text += transform(str(abs(int((self.BTC/self.BTC_close -1)*10000)/100))) + text.PRCT + text.MEAN
		if self.BTC_21 <= self.BTC :
			self.text += text.HD + "."
		else :
			self.text += text.ED + "."
		self.text += text.MA
		if self.BTC_50 <= self.BTC_21 : 
			self.text += text.HD 
		else :
			self.text += text.ED
		self.text += "et " 
		if self.BTC_50 >= self.BTC_100 : 
			self.text += text.HD1
		else :
			self.text += text.ED1 

		#Etherum
		self.text +=  text.ETH
		if self.ETH >= self.ETH_close :
			self.text += text.VERT 
		else :
			self.text += text.ROUGE
		self.text += transform(str(abs(int((self.ETH/self.ETH_close -1)*10000)/100))) + text.PRCT + text.MEAN
		if self.ETH_21 <= self.ETH :
			self.text += text.HD + "."
		else :
			self.text += text.ED + "."
		self.text += text.MA
		if self.ETH_50 >= self.ETH_21 : 
			self.text += text.HD
		else :
			self.text += text.ED 
		self.text += "et "
		if self.ETH_50 >= self.ETH_100 : 
			self.text += text.HD1
		else :
			self.text += text.ED1 

		print(self.text)
		


	def do_your_job(self):
		"""The final function that will be called in main.py, it scraps all we need"""

		self.get_graphs()
		self.get_actual_data()
		self.BTC_100, self.BTC_50, self.BTC_21, self.BTC_close = self.get_historical_data('BTCUSDT',)
		self.ETH_100, self.ETH_50, self.ETH_21, self.ETH_close =  self.get_historical_data('ETHUSDT',)
		self.get_text_graphs()
		self.get_news()
		self.get_account()
		self.get_voice(self.text)
		tm.sleep(10)
		self.get_account()
		self.get_voice(self.text_news)
		tm.sleep(20)
		move_files()
	

def screenshot(name) : 
	box = (120, 310, 2100, 1650)
	snapshot = IG.grab(box)
	save_path = "D:\\Projets\\Youtube\\img\\" + str(name) + ".jpg" 
	snapshot.save(save_path)

def move_files() :
	src = "C:\\Users\\Hadrien\\Downloads"
	dst = "D:\\Projets\\Youtube\\audio\\"
	files = os.listdir(src)
	k=0
	for file in files :
		if file.endswith('.mp3'):
			shutil.move(os.path.join(src,file),dst + str(date.today()) + "-" + str(k) + ".mp3")
			k+=1

def transform(string):
	return(string[:-3] + " virgule " + string[-2:])


def main():
	#tm.sleep(3)
	#screenshot("test")
	
	Antoine = Scraper_bot("Antoine")
	Antoine.get_news()
	Antoine.do_your_job()
	
	#move_files()
	
	"""
	Antoine = Scraper_bot("Antoine")
	Antoine.BTC_100, Antoine.BTC_50, Antoine.BTC_21, Antoine.BTC_close = Antoine.get_historical_data('BTCUSDT',)
	Antoine.ETH_100, Antoine.ETH_50, Antoine.ETH_21, Antoine.ETH_close =  Antoine.get_historical_data('ETHUSDT',)
	Antoine.get_actual_data()
	Antoine.get_text_graphs()
	print(Antoine.text)
	"""


if __name__ == '__main__':
	main()

