#!/usr/bin/env python

import re
import sys
import os
import string

#file_prev = str(sys.argv[1])
#file_now = str(sys.argv[2])
users ={}
users_process_s ={}
users_process_cpu = {}
users_process_mem = {}

users_new = {}
users_process_new={}
users_process_cpu_now = {}
users_process_mem_now = {}

increased_mem ={}
increased_cpu ={}
def prev(file_prev):
	f1 = open(file_prev, "r")
	c = 0	

	for line in f1:
		#print line
		c = c + 1
		if c <= 7 :
			ds = 0
		else :
			line=line.strip().lower()
			arr=line.split()	
			list2 = [x for x in arr if x != []] # remove all columns that are empty
			
			user = list2[1]
			procs = list2[11]
			cpu = float(list2[8])
			mem = float(list2[9])
			if user in users :
				do_nothing = ""
			else :
				users[user] = 0
			users_process = str(user) + "|" + procs
			
			users_process_s[users_process] = 0
			
			users_process_cpu[users_process] = cpu
			users_process_mem[users_process] = mem		
	#print len(users_process_cpu)
	#print len(users_process_mem)	

def now(file_now):
	f1 = open(file_now, "r")
	c = 0

	for line in f1:
		c = c + 1
		if c <= 7 :
			ds = 0
		else :
			line=line.strip().lower()
			arr=line.split()	
			list2 = [x for x in arr if x != []] # remove all columns that are empty			
			user = list2[1]
			procs = list2[11]
			cpu = float(list2[8])
			mem = float(list2[9])
			if user in users :
				do_nothing = ""
			else :
				users_new[user] = 0
			users_process = str(user) + "|" + procs
			
			if users_process in users_process_s :
				do_nothing = ""
			else :
				users_process_new[user] = 0

			for k, v in users_process_s.items():
	    			if cpu > users_process_cpu[k] :
					increased_cpu[k] = cpu
				if mem > users_process_mem[k] :
					increased_mem[k] = mem
					
	#print len(users_process_cpu)
	#print len(users_process_mem)

def _main_():
	file_prev = str(sys.argv[1])
	file_now = str(sys.argv[2])	
	prev(file_prev)
	now(file_now)
	
	for k, v in users_new.items():
	    print(k,v)
	for k, v in users_process_new.items():
            print(k,v)
	for k, v in increased_mem.items():
            print(k,v)
	for k, v in increased_cpu.items():
            print(k,v)
	
_main_()
