import sys
import os
import subprocess
import shlex
import time

PROMPT = "$ "
EXIT = "exit"
CD = "cd"
PWD = "pwd"
JOBS = "jobs!"
BG = "bg"
FG = "fg"
HISTORY = "prev"
HIST_FILENAME = "history.txt"
PIPE = " | "
GOODBYE = "My battery is low and it's getting dark..."
BUILTINS = [CD, PWD, JOBS, BG, FG, HISTORY, EXIT]
processes = []

def tash_cd(file_path):
	try:
		os.chdir(file_path)
	except Exception as e:
		print("something went wrong :( there's probably no filepath. exception: ", e)
	return os.getcwd()

def builtins(uinput):
	if uinput == EXIT:
		print(GOODBYE)
		sys.exit(0)
		return

	if uinput == CD:
		return tash_cd(uinput[1])

	if uinput == PWD:
		print(os.getcwd())
		return os.getcwd()

	if uinput == 'jobs!':
		running_processes = [("pid", "cmd")]
		for entry in processes:
			if entry[0].poll() == None:
				#ok so this plus one looks super arbitrary, but it is here for a reason
				running_processes.append((entry[0].pid + 1, entry[1]))
		for i in running_processes:
			print(i)
		return
	if uinput == 'bg':
		return

	if uinput == 'fg':
		return

#ignore
def exec():
	good_uin = False
	while not good_uin:
		uinput = input(PROMPT)
		if len(uinput) != 0:
			good_uin = True
	#print(uinput)
	#MAKES THE LARGE ASSUMPTION THAT ANY BUILTINS ARE PASSED IN IN ISOLATION
	if uinput.split()[0] in BUILTINS:
				#run builtin function	
				p = builtins(uinput.split()[0])
	else:
		#commented out bc it kills subprocess commands
		#shlex.quote()
		p = subprocess.Popen(uinput, shell = True)
		
		global processes
		processes.append((p, uinput))
		#print(p.pid)
				
def main():
	while(True):
		exec()
	
	return

main()