#!/usr/bin/python2.7

import sys,os
from time import gmtime, strftime
try:
	from prettytable import *
	pretty = True
except ImportError:
	pretty = False

os.system('printf "\033c"')
search = raw_input('Enter a person, business or email: ')

date = strftime('%d_%b_%Y', gmtime())
folder = search+'-'+date
os.system('mkdir '+folder)

#os.system('echo Email, Password, Hint > '+search+'.txt')
#os.system('grep '+search+' cred | cut -d"|" -f3,4,5 | sed "s/-|-/, /g" | sed "s/-//g" >> '+search+'.txt')

#is there an issue?
#os.system('cat results.txt | cut -d"," -f4 | uniq -c >> err.lst')

os.system('cut -d"," -f1 '+search+'.txt > '+search+'_users.txt')

fp = open(search+".txt", "r")
pt = from_csv(fp)
fp.close()
print pt

#find password re-use
os.system('cut -d "," -f2 '+search+'.txt | sort | uniq -c | sort | grep "^......[2-9]" | sed "s/ //g" | sed "s/^[0-9].//g" > tmp')

common_pass = []
os.system('echo Email, Re-Used Password, Hint > '+search+'_common.txt')

with open('tmp', 'r') as f:
	for line in f:
		common_pass.append(line.strip())

for item in common_pass:
	os.system('grep '+item+' '+search+'.txt >> '+search+'_common.txt')


fp = open(search+"_common.txt", "r")
pt = from_csv(fp)
fp.close()

print pt

get_pass = []
print 'Paste passwords for targetted search (eg. AAAAA== BBBBB== CCCCC==) or type ALL to do full recursive search:'   
mode = raw_input('=> ').lower()

if mode == 'all':
	os.system('cut -d"," -f2 '+search+'.txt | tail -n +2 |sort -u > tmp')
	
	with open('tmp', 'r') as f:
		for line in f:
			get_pass.append(line.strip())
			print 'finding '+line+' in AdobeLeak'
			os.system('grep "'+line+'" cred > '+search+'_'+line+'.txt')
else:
	get_pass = mode.split()
#	os.system('echo > tmp')
#	os.system('echo Email, Password, Hint > '+search+'_search.txt')
	for item in get_pass:
		print 'finding '+item+'.'
#		os.system('grep -F '+item+' cred >> tmp')
#	os.system('cat tmp | cut -d"|" -f3,4,5 | sed "s/-|-/, /g" | sed "s/-//g" >> '+search+'_search.txt')

	fp = open(search+"_search.txt", "r")
	pt = from_csv(fp)
	fp.close()
	print pt


raw_input('end')

#	for item in get_pass:
#		os.system('cut -d"," -f2 '+search+'.txt | tail -n +2 |sort -u')
