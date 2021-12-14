"""A bot to have some views, and maybe somme money"""


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.opera import OperaDriverManager
from selenium.webdriver import ActionChains as A
from selenium.webdriver.common.keys import Keys as K
from selenium.webdriver.support.ui import Select
import os 
import time as tm 
import random as rd



#suppression des affichages de webdriver-manager
os.environ['WDM_LOG_LEVEL'] = '0'
os.environ['WDM_PRINT_FIRST_LINE'] = 'False'



#For chrome, we keep it for learning purpose
#boutons = driver.find_elements_by_css_selector(\
#"yt-formatted-string#text.style-scope.ytd-button-renderer.style-primary.size-default")


class Viewer_bot() : 


	def __init__(self) : 

		#Here we do not use webdriver manager so we can use OperaDriver with the VPN (so Youtube counts each of the views)

		#scraping with selenium
		self.options = webdriver.ChromeOptions()
		self.options.add_argument("--start-maximized")
		self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.opera_profile = r'C:\\Users\\hadrien\\AppData\\Roaming\\Opera Software\\Opera Stable' 
		self.options._binary_location = r'C:\\Users\\hadrien\\AppData\\Local\\Programs\\Opera\\opera.exe'
		self.options.add_argument('user-data-dir=' + self.opera_profile)
		
		self.options2 = webdriver.ChromeOptions()
		self.options2.add_argument("--start-maximized")
		self.options2.add_argument('headless')
		self.options2.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.opera_profile2 = r'C:\\Users\\hadrien\\AppData\\Roaming\\Opera Software\\Opera Stable2'
		self.options2._binary_location = r'C:\\Users\\hadrien\\AppData\\Local\\Programs\\Opera\\opera.exe'
		self.options2.add_argument('user-data-dir=' + self.opera_profile2)	
		
	def watch(self) : 

		success = True
		try :
		
			driver = webdriver.Opera(executable_path=r'C:\\operadriver_win64\\operadriver.exe',options=self.options)
			driver.get("https://www.youtube.com/results?search_query=banou_coach")
			tm.sleep(rd.randint(2,5))

			#search the channel, this process is longer than direct link but better for 
			#the youtube algorithm
			research = driver.find_elements_by_class_name("yt-simple-endpoint")
			for elem in research : 
				if elem.text == "Séance ABDOMINAUX à la maison - Tapis et haltères - Routine abdos - Pour des abdos dessinés - Femme" :
					elem.click()
					break
		


			driver2 = webdriver.Opera(executable_path=r'C:\\operadriver_win64\\operadriver.exe',options=self.options2)
			driver2.get("https://www.youtube.com/results?search_query=banou_coach")
			tm.sleep(rd.randint(2,5))

			#search the channel, this process is longer than direct link but better for 
			#the youtube algorithm
			research = driver2.find_elements_by_class_name("yt-simple-endpoint")
			for elem in research : 
				if elem.text == "Séance ABDOMINAUX à la maison - Tapis et haltères - Routine abdos - Pour des abdos dessinés - Femme" :
					elem.click()
					break

		except :
			print("An error ocurred, trying again")
			sucess = False


		if success :
			tm.sleep(1100)
		
		else :
			pass 

		try : 
			driver.close()
			driver2.close()
			
		except :
			pass

		return success


if __name__ == "__main__" :

	os.system("cls")
	print("Let's watch some videos !\n\n")
	nb_iter = 0
	while True :

		bot = Viewer_bot()
		success = bot.watch()
		if success :
			nb_iter +=1
			print("number of views : ", 2 * nb_iter)

		else:
			pass 

