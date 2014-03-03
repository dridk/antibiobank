#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv	
import os
from datetime import *
from antibiobank.models import *


def inject_datas(filename):
	file    = open(filename,'rb')
	total   = len(file.readlines())
	current = 0.0


	file.seek(0)
	csvreader = csv.reader(file,delimiter=";")
	headers = csvreader.next()

	# for name in headers[7:]:
	# 	Antibiotic.objects.get_or_create(name = name)



	for row in csvreader:

		recId    = row[0]
		name     = row[1]
		service  = row[2]
		date     = datetime.strptime(row[3],"%d/%m/%Y")
		birthday = datetime.strptime(row[4],"%d/%m/%Y")
		specimen = row[5]
		bacterie = os.path.splitext(os.path.basename(filename))[0]
		
		try:
			g_name = bacterie.split("_")[0]
			s_name = bacterie.split("_")[1]
		except IndexError:
			print("your filename should be like 'species_gender.csv'")


		service_item  = Service.objects.get_or_create(name=service)
		specimen_item = Specimen.objects.get_or_create(name=specimen)
		bacterie_item = Bactery.objects.get_or_create(generic_name=g_name,specfic_name=s_name)


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
				Resistance.objects.create(record = record[0], 
										  antibiotic = atb_item[0],
										  value = row[index])
				
		
		print("[%s %%] ave Record %s" % (round(current/total*100,2),recId))		
		current += 1	

		# break
	
		



r = inject_datas("datas/Staphylococcus_aureus_atb.csv")
