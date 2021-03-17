from signal import SIGINT, SIGCONT, SIGSTOP, SIGKILL
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
zombie_processes = []
running_foreground_process = None

"""
Handles all the builtin functions; includes:
- exit (exits and prints a sad exit message)
- cd (changes the working directory)
- pwd (prints the working directory)
- jobs (prints the process id and the command per background process)
- bg (restarts the job as a background process)
- fg (restarts the job)
"""
def builtins(uinput, usr = 1):

	if uinput[0] == EXIT:
		print(GOODBYE)
		sys.exit(0)
		return 0

	if uinput[0] == CD:
		# try changing directory; otherwise catch exception
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

		# find running background processes
		global zombie_processes
		running_processes = []
		for entry in processes:
			#if process is still runnings
			if entry[0].poll() == None:
				#print("bdhh")
				running_processes.append(entry)
			else:
				#print("fgeun")
				zombie_processes.append(entry)
		
		for x in zombie_processes:
			sig = x[0].poll() 
			
			if sig != 0:
				print("A signal terminated this shell. The offending signal number was: " + str(sig))
			x[0].terminate()
			#os.kill(x[0].pid, signal.SIGKILL)
		zombie_processes = []
		
		# the user is calling jobs, not fg or bg, then print
		if usr == 1:
			print("pid ", "cmd")
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
				processes[x] = (subprocess.Popen(processes[x][1], shell = True, start_new_session = True), processes[x][1])
		return

	if uinput[0] == FG:
		global fg
		#refreshes the list of processes
		builtins([JOBS], 0)
		for x in range(0, len(processes)):
			if str(processes[x][0].pid) == uinput[1]:
				processes[x][0].send_signal(signal.SIGSTOP)
				restarted_cmd = processes[x][1]
				processes.pop(x)
				fg = subprocess.Popen(restarted_cmd, shell = True).wait()
				fg = None
		return

def exec(user_input, background_status):
	global processes
	global running_foreground_process
	#MAKES THE LARGE ASSUMPTION THAT ANY BUILTINS ARE PASSED IN IN ISOLATION
	if user_input.split()[0] in BUILTINS:
				#run builtin function	
				p = builtins(user_input.split())
	else:
		#if the process is a background process
		if background_status:
			p = subprocess.Popen(user_input, shell = True, start_new_session = True)
			processes.append((p, user_input))
		else:
			#The process is a foreground process
			running_foreground_process = subprocess.Popen(user_input, shell = True).wait()
			running_foreground_process = None
	return
		
def get_user_input():
	

	background_process = False
	#Initially assuming that the user will ask for a  
	#process incorrectly
	good_user_input = False
	while not good_user_input:
		builtins([JOBS], 0)
		user_input = input(PROMPT)
		#Just checking to see if the user even entered a string
		if len(user_input) >= 2:
			good_user_input = True
	#seeing if the command is a background process
	if user_input[-1] == BACKGROUND and user_input[-2] == " ":
		background_process = True
		user_input = user_input[:-2]
	return (user_input, background_process)

#def kill_foreground_process_SIGSTOP(signal_received, frame):
	#if running_foreground_process != None:
		#os.kill(running_foreground_process.pid,signal.SIGSTOP)
	#return

#def kill_foreground_process_SIGSTOP(signal_received, frame):
	#if running_foreground_process != None:
		#os.kill(running_foreground_process.pid,signal.SIGSTOP)
	#return



def main():
	global zombie_processes
	#signal.signal(SIGSTOP, kill_foreground_process_SIGSTOP)


	global running_foreground_process
	#signal.signal(signal.SIGSTOP, kill_foreground_process_SIGSTOP)
	
	while(True):
		#builtins([JOBS], 0)
		try:
			user_input, background_status = get_user_input()
			exec(user_input, background_status)
			#builtins([JOBS], 0)

		except KeyboardInterrupt:
			if running_foreground_process != None:
				print("is this reached?")
				os.kill(running_foreground_process.pid, signal.SIGINT)
				running_foreground_process = None
	return

main()