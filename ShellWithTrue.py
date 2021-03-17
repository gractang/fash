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
JOBS = "jobs"
BG = "bg"
FG = "fg"
HISTORY = "prev"
HIST_FILENAME = "history.txt"
PIPE = " | "
GOODBYE = "My battery is low and it's getting dark..."
BACKGROUND = "&"
BUILTINS = [CD, PWD, JOBS, BG, FG, HISTORY, EXIT]
#All the current running background jobs will be stored here
processes = []
running_foregeound_process = None

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
		try:
			os.chdir(uinput[1])
		except Exception as e:
			print("something went wrong :( there's probably no filepath. exception: ", e)
		return os.getcwd()
	
	if uinput[0] == PWD:
		print(os.getcwd())
		return os.getcwd()

	if uinput[0] == JOBS:
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
		builtins([JOBS], 0)
		for x in range(0, len(processes)):
			if str(processes[x][0].pid) == uinput[1]:
				processes[x][0].send_signal(signal.SIGSTOP)
				#exec call? would be nicer...
				processes[x] = (subprocess.Popen(processes[x][1], shell = True), processes[x][1])
		return

	if uinput[0] == FG:
		global fg
		#refreshes the list of processes
		builtins([JOBS], 0)
		for x in range(0, len(processes)):
			if str(processes[x][0].pid) == uinput[1]:
				processes[x][0].send_signal(signal.SIGSTOP)
				#exec call? would be nicer...
				restarted_cmd = processes[x][1]
				processes.pop(x)
				fg = subprocess.Popen(restarted_cmd, shell = True).wait()
				fg = None
		return

def exec(user_input, background_status):
	global processes
	global running_foregeound_process
	#MAKES THE LARGE ASSUMPTION THAT ANY BUILTINS ARE PASSED IN IN ISOLATION
	if user_input.split()[0] in BUILTINS:
				#run builtin function	
				p = builtins(user_input.split())
	else:
		#if the process is a background process
		if background_status:
			print("I am a backgrund process!")
			p = subprocess.Popen(user_input, shell = True)
			processes.append((p, user_input))
		else:
			#The process is a foreground process
			running_foregeound_process = subprocess.Popen(user_input, shell = True).wait()
			running_foregeound_process = None
	return
		
def get_user_input():
	background_process = False
	#Initially assuming that the user will ask for a  
	#process incorrectly
	good_user_input = False
	while not good_user_input:
		user_input = input(PROMPT)
		#Just checking to see if the user even entered a string
		if len(user_input) >= 2:
			good_user_input = True
	#seeing if the command is a background process
	if user_input[-1] == "&" and user_input[-2] == " ":
		background_process = True
		user_input = user_input[:-2]
	return (user_input, background_process)

#def kill_foreground_process_SIGSTOP(signal_received, frame):
	#if running_foregeound_process != None:
		#os.kill(running_foregeound_process.pid,signal.SIGSTOP)
	#return

def main():
	global running_foregeound_process
	#signal.signal(signal.SIGSTOP, kill_foreground_process_SIGSTOP)
	
	while(True):
		try:
			user_input, background_status = get_user_input()
			exec(user_input, background_status)
		except KeyboardInterrupt:
			if running_foregeound_process != None:
				print("is this reached?")
				os.kill(running_foregeound_process.pid, signal.SIGINT)
				running_foregeound_process = None
	return

main()