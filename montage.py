"""
Le bot de montage vidéo
-----------------------

Il s'occupe de monter la vidéo avec tous les éléments récupérés par le bot de scraping
"""

import os
from moviepy.editor import *
import pygame as pg 
from datetime import date


class Cutter_bot():

	def __init__(self,name):
		self.name = name
		self.audio1 = AudioFileClip("D:\\Projets\\Youtube\\audio\\" + str(date.today()) + "-0.mp3")
		self.audio2 = AudioFileClip("D:\\Projets\\Youtube\\audio\\" + str(date.today()) + "-1.mp3")
		self.full_audio = concatenate_audioclips([self.audio1,self.audio2])
		self.duration = self.full_audio.duration
		self.btc_chart = ImageClip("D:\\Projets\\Youtube\\img\\BTC_graph.jpg",duration=15)
		self.eth_chart = ImageClip("D:\\Projets\\Youtube\\img\\ETH_graph.jpg",duration=15)
		self.INTRO = ImageClip("D:\\Projets\\Youtube\\img\\INTRO.jpg",duration=6)
		self.OUTRO = ImageClip("D:\\Projets\\Youtube\\img\\INTRO.jpg",duration=18)
		self.NEWS = ImageClip("D:\\Projets\\Youtube\\img\\NEWS.jpg",duration=self.duration - 54)


	def __repr__(self) : 
		return "Bonjour, je suis " + self.name +" un bot de montage, grâce à moi les vidéos seront bien montées."

	def mount_clip(self) :
		self.full_clip = concatenate_videoclips([ \
			self.INTRO,\
			self.btc_chart,\
			self.eth_chart,\
			self.NEWS,\
			self.OUTRO])

	def add_sound(self):
		self.full_clip.audio = self.full_audio	

	def write_clip(self) :
		self.full_clip.write_videofile("D:\\Projets\\Youtube\\vid\\video-"+str(date.today())+".mp4",fps=25)

	def do_your_job(self):
		self.mount_clip()
		self.add_sound()
		self.write_clip()

def main() :
	Camille = Cutter_bot("Camille")
	Camille.mount_clip()
	Camille.add_sound()
	Camille.write_clip()



if __name__ == '__main__':
	main()
	

