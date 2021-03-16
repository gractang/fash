from signal import SIGINT, SIGCONT, SIGSTOP
import signal
from sys import exit
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
FOREGROUND = "}"
BUILTINS = [CD, PWD, JOBS, BG, FG, HISTORY, EXIT]
processes = []
fg = None

def tash_cd(file_path):
	try:
		os.chdir(file_path)
	except Exception as e:
		print("something went wrong :( there's probably no filepath. exception: ", e)
	return os.getcwd()

def builtins(uinput, temp = 1):
	if uinput[0] == EXIT:
		print(GOODBYE)
		sys.exit(0)
		return

	if uinput[0] == CD:
		return tash_cd(uinput[1])

	if uinput[0] == PWD:
		print(os.getcwd())
		return os.getcwd()

	if uinput[0] == 'jobs!':
		
		global processes
		running_processes = []
		for entry in processes:
			if entry[0].poll() == None:
				
				running_processes.append(entry)
		if temp == 1:
			print("pid", "cmd")
			for i in running_processes:
			
				print(i[0].pid, i[1])
		processes = running_processes
		return
	
	if uinput[0] == BG:
		#refreshes the list of processes
		builtins(["jobs!"], 0)
		for x in range(0, len(processes)):
			if str(processes[x][0].pid) == uinput[1]:
				processes[x][0].send_signal(signal.SIGSTOP)
				#exec call? would be nicer...
				processes[x] = (subprocess.Popen(processes[x][1], shell = True), processes[x][1])
		return

	if uinput[0] == FG:
		global fg
		#refreshes the list of processes
		builtins(["jobs!"], 0)
		for x in range(0, len(processes)):
			if str(processes[x][0].pid) == uinput[1]:
				processes[x][0].send_signal(signal.SIGSTOP)
				#exec call? would be nicer...
				restarted_cmd = processes[x][1]
				processes.pop(x)
				fg = subprocess.Popen(restarted_cmd, shell = True).wait()
				fg = None
		return

#ignore
def exec():
	global processes
	bg_proc = True
	good_uin = False
	while not good_uin:
		uinput = input(PROMPT)
		if len(uinput) != 0:
			good_uin = True

	if uinput[-1] == FOREGROUND and uinput[-2] == " ":
		print("hello")
		uinput = uinput[:-2]
		bg_proc = False
	#print(uinput)
	#MAKES THE LARGE ASSUMPTION THAT ANY BUILTINS ARE PASSED IN IN ISOLATION
	if uinput.split()[0] in BUILTINS:
				#run builtin function	
				p = builtins(uinput.split())
	else:
		if bg_proc:
			p = subprocess.Popen(uinput, shell = True)
			processes.append((p, uinput))
		else:
			print("9f")
			p = subprocess.Popen(uinput, shell = True).wait()
	return
		#print(p.pid)
				
def kill_foreground_process(signal_received, frame):
	global fg
	if fg != None:
		print("can i gwt uh")
		os.kill(fg.pid,signal.SIGINT)
	return

def main():
	signal.signal(signal.SIGCONT, kill_foreground_process)
	while(True):
		exec()
	
	return

main()