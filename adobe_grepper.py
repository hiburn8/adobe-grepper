#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__author__ = 'hiburn8'

import sys,os
from time import gmtime, strftime
from distutils import spawn
try:
	from prettytable import *
	pretty = True
except ImportError:
	pretty = False

pv = spawn.find_executable("pv")
if pv is not None:
	lbars = True
else:
	lbars = False

class bg:
	FAIL = '\033[91m'
	OK = '\033[92m'
	DBG = '\033[93m'
	END = '\033[0m'


print bg.FAIL+"           _       _          " + bg.END                                    
print bg.FAIL+"  __ _  __| | ___ | |__   ___ " + bg.END+" __ _ _ __ ___ _ __  _ __   ___ _ __ "
print bg.FAIL+" / _` |/ _` |/ _ \| '_ \ / _ \\" + bg.END+"/ _` | '__/ _ \ '_ \| '_ \ / _ \ '__|"
print bg.FAIL+"| (_| | (_| | (_) | |_) |  __/" + bg.END+" (_| | | |  __/ |_) | |_) |  __/ |   "
print bg.FAIL+" \__,_|\__,_|\___/|_.__/ \___|" + bg.END+"\__, |_|  \___| .__/| .__/ \___|_|   "
print bg.FAIL+"                              " + bg.END+"|___/         |_|   |_|              "
print '''
 ---------------------------------------------------------------------
	Version: 1.1
	Coded By: Hiburn8
 ----------------------------------------------------------------------'''
if (pretty is True):
	print 'prettytable module found -> showTables=YES'+bg.END
else:
	print bg.FAIL+'prettytable module not found -> showTables=YES'+bg.END
if (lbars is True):
	print 'pv binary found -> showLoadingBars=YES'+bg.END
else:
	print bg.FAIL+'pv binary not found -> showLoadingBars=NO'+bg.END


path = ""
print '\nEnter a person, business or email (or h for help):'
q = raw_input('=> ')

if (q.lower() == "h"):
	print '''
	In 2014 Adobe suffered a data breach which subsequently resulted in a datebase 
	of over 140 millions credentials being leaked onto the internet. 
	
	The tool aids mining local copies of that leaked dataset. It is designed to 
	help penetration testing and can be used to find credential information in a 
	passive manner.
	What this tool is NOT designed to do is aid attackers in resolving password data 
	from victims of the breach en-mass. This tool is a scalpel, not a hammer.

	Searches work best with input like the following:

	company-name: example
	website: example.com
	email-scheme: @mail.example.com
	person: bob
	exact email: bob@example.com
	hint information: davinci
	'''
else:

	date = strftime('%d_%b_%Y', gmtime())
	f = q+'-'+date+'/'

	os.system('mkdir '+f)

	#Get initial
	os.system('echo Email, Password, Hint > '+f+'all.csv')

	print bg.FAIL+'\nBe patient. If you are not using an SSD, go get a drink.'+bg.END
	if (lbars is True):
		os.system('pv '+path+'cred | grep '+q+'| cut -d"|" -f3,4,5 | sed "s/,//g" | sed "s/-|-/, /g" | sed "s/-//g" >> '+f+'all.csv')
	else:
		os.system('cat '+path+'cred | grep '+q+' | cut -d"|" -f3,4,5 | sed "s/,//g" | sed "s/-|-/, /g" | sed "s/-//g" >> '+f+'all.csv')
	print bg.OK + 'All results => all.csv' + bg.END

	#Get email dictionary
	os.system('cut -d"," -f1 '+f+'all.csv > '+f+'emails.dic')
	print bg.OK + 'Email dictionary => emails.dic' + bg.END

	if pretty == True:
		if (raw_input('Show everything? (Y/n): ').lower() != "n"):
			fp = open(f+'all.csv', "r")
			pt = from_csv(fp)
			fp.close()
			print pt

	#Get password stats
	os.system('echo Occurances, Password > '+f+'passwordstats.csv')
	os.system('cat '+f+'all.csv | tail +2 | cut -d "," -f2  | sort | uniq -c | sort -r | sed "s/  /, /g" | cut -d"," -f2,3 | tail +2 >> '+f+'passwordstats.csv')
	print bg.OK + 'Password stats => passwordstats.csv' + bg.END

	if pretty == True:
		if (raw_input('Show stats? (y/N): ').lower() == "y"):
			fp = open(f+'passwordstats.csv', "r")
			pt = from_csv(fp)
			fp.close()
			print pt

	#Get password resuse
	os.system('cat '+f+'passwordstats.csv | grep -E "^[ ]*([2-9]|[1-9][0-9]+)" | sed "s/ //g" | sed "s/^.*,//g" > '+f+'tmp')
	common_pass = []
	os.system('echo Email, Re-Used Password, Hint > '+f+'passwordreuse.csv')

	with open(f+'tmp', 'r') as fp:
		for line in fp:
			common_pass.append(line.strip())
		os.system('rm '+f+'tmp')

	for item in common_pass:
		os.system('cat '+f+'all.csv | grep '+item+' >> '+f+'passwordreuse.csv')

	if pretty == True:
		if (raw_input('Show reuse details? (Y/n): ').lower() != "n"):
			fp = open(f+'passwordreuse.csv', "r")
			pt = from_csv(fp)
			fp.close()
			print pt

	print bg.OK + 'Password reuse => passwordreuse.csv\n' + bg.END

	#Targeted mode
	if (raw_input('Enter targeted Mode? (y/N): ').lower() == "y"):

		get_pass = []
		print 'Type space-separated targets, eg. "CatHbW= L8qbA=", or "ALL" to do everything (Slow):'   
		mode = raw_input('=> ')

		print bg.FAIL+'\nBe patient again. If you typed ALL, go play outside.'+bg.END

		if mode == 'all':
			os.system('cut -d"," -f2 '+f+'all.csv | tail -n +2 |sort -u > '+f+'tmp')
			
			with open(f+'tmp', 'r') as f:
				for line in f:
					get_pass.append(line.strip())
					print 'finding '+line+''
					os.system('cat cred | grep "'+line+'" > '+q+'_'+line+'.txt')
		else:
			get_pass = mode.split()
			os.system('echo Email, Password, Hint > '+f+q+'_target.csv')
			for item in get_pass:
				print 'finding '+item
				if (lbars is True):
					os.system('pv '+path+'cred | grep -F '+item+' > '+f+'tmp')
				else:
					os.system('cat '+path+'cred | grep -F '+item+' > '+f+'tmp')

			
			os.system('cat '+f+'tmp | cut -d"|" -f3,4,5 | sed "s/,//g" | sed "s/-|-/, /g" | sed "s/-//g" >> '+f+q+'_target.csv')
			os.system('rm '+f+'tmp')

			print bg.OK + 'Search results saved to '+f+q+'_target.csv' + bg.END

		if pretty == True:
			if (raw_input('Show targeted details? (Y/n): ').lower() != "n"):
				fp = open(f+q+"_target.csv", "r")
				pt = from_csv(fp)
				fp.close()
				print pt

		raw_input('end')
