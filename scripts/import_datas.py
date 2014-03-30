#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv	
import os
import sys
import glob
import smtplib
from datetime import *
from antibiobank.models import *



#=====================================================

def inject_datas(filename):

	file    = open(filename,'rb')
	total   = len(file.readlines())
	current = 0.00


	file.seek(0)
	csvreader = csv.reader(file,delimiter=";")
	headers = csvreader.next()

	# for name in headers[7:]:
	# 	Antibiotic.objects.get_or_create(name = name)



	for row in csvreader:


		recId    = row[0]
		name     = row[1]
		service  = row[2]
		specimen = row[5]
		bacterie = os.path.splitext(os.path.basename(filename))[0]

		try:
			date = datetime.strptime(row[3],"%d/%m/%Y")
		except:
			date = None

		try:
			birthday = datetime.strptime(row[4],"%d/%m/%Y")
		except:
			birthday = None
		
		try:
			g_name = bacterie.split("_")[0]
			s_name = bacterie.split("_")[1]
		except IndexError:
			print("your filename should be like 'species_gender.csv'")

		service_item  = Service.objects.get_or_create(name=service)
		specimen_item = Specimen.objects.get_or_create(name=specimen)
		bacterie_item = Bactery.objects.get_or_create(generic_name=g_name,specific_name=s_name)


		record  = Record.objects.get_or_create(  
										service  = service_item[0], 
										bactery  = bacterie_item[0],
										specimen = specimen_item[0],
										date     = date,
										birthday = birthday,
										id       = recId)


		for name in headers[7:]:
			index = headers.index(name)
			if bool(row[index])  and row[index] not in "NL":
				atb_item = Antibiotic.objects.get_or_create(name = name)
				if row[index] in ("S","I","R"):
					Resistance.objects.create(record = record[0], 
										  antibiotic = atb_item[0],
										  value = row[index])
				
		
		# print("\r%.02f%% %s, " % (round(current/total*100,2),recId))	



		percent = current/total

		current += 1.00
		if current + 1 >= total:
			percent = 1
			
		hashes = '#' * int(round(percent * 20))
		spaces  = " " * (20 - len(hashes))
		

		output = "\r{2:30}:[{0}] {1}%".format(hashes + spaces,round(percent*100,2), bacterie)
		sys.stdout.write(output)
		sys.stdout.flush()

	sys.stdout.write("\n")





#=====================================================
	
def run():		
	
	print "---------------------------------------------"
	print "Start datas injections at {}".format(datetime.today())
	print "---------------------------------------------"
	start_date = datetime.today()



	for file in glob.glob("datas/utf8/*.csv"):
		inject_datas(file)
#		server = smtplib.SMTP("localhost")
#		server.sendmail("antibiobank@labsquare.org","istdasklar@gmail.com", file+" imported")	

	end_date  = datetime.today()

	diff = end_date - start_date 

	print "---------------------------------------------"
	print "End of injection in {}".format(diff)
#	server.sendmail("antibiobank@labsquare.org", "istdasklar@gmail.com", "Insertion des datas terminé")
#	server.quit()

