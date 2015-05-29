#!/usr/bin/python2.7

__author__ = 'hiburn8'

import sys,os
from time import gmtime, strftime
from distutils import spawn
try:
	from prettytable import *
	pretty = True
except ImportError:
	pretty = False

class bg:
	FAIL = '\033[91m'
    OK = '\033[92m'
    DBG = '\033[93m'
    END = '\033[0m'

path = ""

q = raw_input('Enter a person, business or email: ')

date = strftime('%d_%b_%Y', gmtime())
f = q+'-'+date+'/'
os.system('mkdir '+f)

os.system('echo Email, Password, Hint > '+f+'all.csv')
pv = spawn.find_executable("pv")

if pv is not None:
	os.system('pv '+path+'cred | grep '+q+'| cut -d"|" -f3,4,5 | sed "s/,//g" | sed "s/-|-/, /g" | sed "s/-//g" >> '+f+'all.csv')
else:
	os.system('grep '+q+' '+path+'cred | cut -d"|" -f3,4,5 | sed "s/,//g" | sed "s/-|-/, /g" | sed "s/-//g" >> '+f+'all.csv')
print bg.OK + 'All results => all.csv' + bg.END

os.system('cut -d"," -f1 '+f+'all.csv > '+f+'emails.dic')
print bg.OK + 'Email dictionary => emails.dic' + bg.END

if pretty == True:
	if (raw_input('Show everything? (Y/n): ').lower() != "n"):
		fp = open(f+'all.csv', "r")
		pt = from_csv(fp)
		fp.close()
		print pt

os.system('echo Occurances, Password > '+f+'passwordstats.csv')
os.system('cat '+f+'all.csv | tail +2 | cut -d "," -f2  | sort | uniq -c | sort -r | sed "s/  /, /g" | cut -d"," -f2,3 | tail +2 >> '+f+'passwordstats.csv')
print bg.OK + 'Password stats => passwordstats.csv' + bg.END

if pretty == True:
	if (raw_input('Show stats? (y/N): ').lower() == "y"):
		fp = open(f+'passwordstats.csv', "r")
		pt = from_csv(fp)
		fp.close()
		print pt

#Getting password resuse
os.system('grep "^[ ]*[2-9][ ]*" '+f+'passwordstats.csv | sed "s/ //g" | sed "s/^[0-9].//g" > '+f+'tmp')
common_pass = []
os.system('echo Email, Re-Used Password, Hint > '+f+'passwordreuse.csv')

with open(f+'tmp', 'r') as fp:
	for line in fp:
		common_pass.append(line.strip())

for item in common_pass:
	os.system('grep '+item+' '+f+'all.csv >> '+f+'passwordreuse.csv')

if pretty == True:
	if (raw_input('Show reuse details? (Y/n): ').lower() != "n"):
		fp = open(f+'passwordreuse.csv', "r")
		pt = from_csv(fp)
		fp.close()
		print pt

print bg.OK + 'Password reuse => passwordreuse.csv' + bg.END

get_pass = []
print 'Paste passwords for targetted search (eg. AAAAA== BBBBB== CCCCC==) or type ALL to do full recursive search:'   
mode = raw_input('=> ').lower()

if mode == 'all':
	os.system('cut -d"," -f2 '+f+'all.csv | tail -n +2 |sort -u > '+f+'tmp')
	
	with open(f+'tmp', 'r') as f:
		for line in f:
			get_pass.append(line.strip())
			print 'finding '+line+' in AdobeLeak'
			os.system('grep "'+line+'" cred > '+q+'_'+line+'.txt')
else:
	get_pass = mode.split()
	os.system('echo > '+f+'tmp')
	os.system('echo Email, Password, Hint > '+q+'_search.txt')
	for item in get_pass:
		print 'finding '+item+'.'
		os.system('grep -F '+item+' cred >> '+f+'tmp')
	os.system('cat '+f+'tmp | cut -d"|" -f3,4,5 | sed "s/-|-/, /g" | sed "s/-//g" >> '+q+'_search.txt')

	if pretty == True: 
		fp = open(f+'/'+q+"_search.txt", "r")
		pt = from_csv(fp)
		fp.close()
		print pt
	else:
		print 'Search results saved to '+q+'_search.txt'

raw_input('end')

#	for item in get_pass:
#		os.system('cut -d"," -f2 '+q+'.txt | tail -n +2 |sort -u')
