#!/usr/bin/python2.7

__author__ = 'hiburn8'

import sys,os
from time import gmtime, strftime
try:
	from prettytable import *
	pretty = True
except ImportError:
	pretty = False

class bg:
    OK = '\033[92m'
    DBG = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'

search = raw_input('Enter a person, business or email: ')

date = strftime('%d_%b_%Y', gmtime())
folder = search+'-'+date
os.system('mkdir '+folder)

os.system('echo Email, Password, Hint > '+search+'.csv')
os.system('grep '+search+' cred | cut -d"|" -f3,4,5 | sed "s/,//g" | sed "s/-|-/, /g" | sed "s/-//g" >> '+search+'.csv')
print bg.OK + 'All results => '+search+'.csv' + bg.END

os.system('cut -d"," -f1 '+search+'.csv > '+search+'_emails.dic')
print bg.OK + 'Email dictionary => '+search+'_emails.dic' + bg.END

if pretty == True:
	if (raw_input('Show everything? (Y/n): ').lower() != "n"):
		fp = open(search+".csv", "r")
		pt = from_csv(fp)
		fp.close()
		print pt

os.system('echo Occurances, Password > '+search+'_passwordstats.csv')
os.system('cat '+search+'.csv | tail +2 | cut -d "," -f2  | sort | uniq -c | sort -r | sed "s/  /, /g" | cut -d"," -f2,3 | tail +2 >> '+search+'_passwordstats.csv')
print bg.OK + 'Password stats => '+search+'_passwordstats.csv' + bg.END

if pretty == True:
	if (raw_input('Show stats? (y/N): ').lower() == "y"):
		fp = open(search+"_passwordstats.csv", "r")
		pt = from_csv(fp)
		fp.close()
		print pt

#Getting password resuse
os.system('grep "^[ ]*[2-9][ ]*" '+search+'_passwordstats.csv | sed "s/ //g" | sed "s/^[0-9].//g" > tmp')
common_pass = []
os.system('echo Email, Re-Used Password, Hint > '+search+'_passwordreuse.csv')

with open('tmp', 'r') as f:
	for line in f:
		common_pass.append(line.strip())

for item in common_pass:
	os.system('grep '+item+' '+search+'.csv >> '+search+'_passwordreuse.csv')

if pretty == True:
	if (raw_input('Show reuse details? (Y/n): ').lower() != "n"):
		fp = open(search+"_passwordreuse.csv", "r")
		pt = from_csv(fp)
		fp.close()
		print pt

print bg.OK + 'Password reuse => '+search+'_passwordreuse.csv' + bg.END

get_pass = []
print 'Paste passwords for targetted search (eg. AAAAA== BBBBB== CCCCC==) or type ALL to do full recursive search:'   
mode = raw_input('=> ').lower()

if mode == 'all':
	os.system('cut -d"," -f2 '+search+'.csv | tail -n +2 |sort -u > tmp')
	
	with open('tmp', 'r') as f:
		for line in f:
			get_pass.append(line.strip())
			print 'finding '+line+' in AdobeLeak'
			os.system('grep "'+line+'" cred > '+search+'_'+line+'.txt')
else:
	get_pass = mode.split()
	os.system('echo > tmp')
	os.system('echo Email, Password, Hint > '+search+'_search.txt')
	for item in get_pass:
		print 'finding '+item+'.'
		os.system('grep -F '+item+' cred >> tmp')
	os.system('cat tmp | cut -d"|" -f3,4,5 | sed "s/-|-/, /g" | sed "s/-//g" >> '+search+'_search.txt')

	if pretty == True: 
		fp = open(search+"_search.txt", "r")
		pt = from_csv(fp)
		fp.close()
		print pt
	else:
		print 'Search results saved to '+search+'_search.txt'

raw_input('end')

#	for item in get_pass:
#		os.system('cut -d"," -f2 '+search+'.txt | tail -n +2 |sort -u')
