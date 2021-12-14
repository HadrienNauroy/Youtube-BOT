"""

		%%%%%%%%%%%%%%%%%%
		% The master bot %
		%%%%%%%%%%%%%%%%%%

Le bot qui appelle tous les autres pour concquérir le youtube game

Il y a 3 sous parties : 

	- un bot de scraping
	- un bot de montage vidéo
	- un appel au script d'upload youtube 

"""

from scraping import *
from montage import *
import subprocess
import text


Antoine = Scraper_bot("Antoine")
Antoine.do_your_job()

Camille = Cutter_bot("Camille")
Camille.do_your_job()


#subprocess.call('py upload.py')
