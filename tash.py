import sys
import os
import subprocess

PROMPT = "$ "
EXIT = "exit"
CD = "cd"
PWD = "pwd"
JOBS = "jobs"
BG = "bg"
FG = "fg"
HISTORY = "prev"
HIST_FILENAME = "history.txt"
PIPE = "|"
INPUT = "<"
OUTPUT = ">"
BACKGROUND = "&"
SPACE = " "
GOODBYE = "My battery is low and it's getting dark..."

BUILTINS = [CD, PWD, JOBS, BG, FG, HISTORY, EXIT]
bg_processes = []
fg = None

def tash_cd(file_path):
	try:
		os.chdir(file_path)
	except Exception as e:
		print("something went wrong :( there's probably no filepath. exception: ", e)
	return os.getcwd()

def tash_prev():
	with open(HIST_FILENAME) as f:
		for line in f:
			pass
	return line

def check_if_bg(uinput):
	if len(uinput) < 2:
		return False
	if uinput[-1] == BACKGROUND and uinput[-2] == SPACE:
		#print("hello")
		uinput = uinput[:-2]
		bg_proc = False

# executes the given command
def exc(uinput):
	try:
		commands = uinput.split(PIPE)
		#run each command and give its output to the next process
		prev_out = None
		#commands at this point is two lists on either side of a "|"
		num_commands = len(commands)
		for i in range(0, num_commands):
			commands[i] = commands[i].split()
			#if command is a builtin
			if commands[i][0] in BUILTINS:
				#run builtin function	
				p = builtins(commands[i])
			elif i == num_commands-1:
				#run execute function
				p = subprocess.Popen(commands[i], stdin = prev_out).wait()
			else:
				p = subprocess.Popen(commands[i], stdin = prev_out, stdout = subprocess.PIPE)
				prev_out = p.stdout

		bg_processes.append((p, uinput))

	except Exception as e:
		print("something went wrong :( there's probably no such command. exception: ", e)
	return 0

# loop to ask for user input
def tash_loop():
	signal.signal(signal.SIGINT, kill_foreground_process)
	f = open(HIST_FILENAME, 'w').close()
	while True:
		# check to make sure that user input is not blank
		good_uin = False
		while not good_uin:
			uin = input(PROMPT)
			if len(uin) != 0:
				good_uin = True
		f = open(HIST_FILENAME, 'a')
		f.write(uin)
		f.write("\n")
		exc(uin)

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

	if uinput == JOBS:
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

	if uinput == BG:
		return

	if uinput == FG:
		return

	# i want to do the thing where the up arrow triggers
	# but too lazy to figure out how to implement
	if uinput[0] == HISTORY:
		prev = tash_prev()
		print(prev)
		return exc(prev)

#ignore
def seperate_command():
	good_uin = False
	while not good_uin:
		uinput = input(PROMPT)
		if len(uinput) != 0:
			good_uin = True

	special_chars = []
	command_segments = []
	#all the flagged charecters
	special_chars_list = [PIPE, INPUT, OUTPUT]
	
	command_set = []
	for x in range(0, len(uinput)):
		if x == len(uinput) -1:
			command_set.append(uinput[x])
			command_segments.append("".join(command_set).strip())
		elif uinput[x] not in special_chars_list:
			command_set.append(uinput[x])
		else:
			command_segments.append("".join(command_set).strip())
			command_set = []
			special_chars.append(uinput[x])
	return command_segments, special_chars

#ignore
def exec(commands, flags):
	#MAKES THE LARGE ASSUMPTION THAT ANY BUILTINS ARE PASSED IN IN ISOLATIONs
	if commands[0] in BUILTINS:
				#run builtin function	
				p = builtins(commands[0])
	elif len(flags) == 0:
		p = subprocess.Popen(commands[0].split())
		print(p.communicate()[0])
	else:
		prev_out = None
		for entry in range(0, len(flags)):
			if flags[entry] == PIPE:
				p = subprocess.Popen(commands[entry].split(), stdin = prev_out, stdout = subprocess.PIPE)
				prev_out = p.stdout
				p2 = subprocess.Popen(commands[entry+1].split(), stdin = prev_out).wait()
			# redirecting output
			elif flags[entry] == OUTPUT:
				p = subprocess.Popen(commands[entry].split(), stdout = open(commands[entry+1], "w")).wait()
				#prev_out = p.stdout
			elif flags[entry] == INPUT:
				p = subprocess.Popen(commands[entry].split(), stdin = open(commands[entry+1], "r"))

				p = subprocess.Popen(commands[entry].split(), stdin = open(commands[entry+1], "r")).wait()

				
def main():
	cmd, scpil = seperate_command()
	exec(cmd, scpil)
	#tash_loop()
	return

main()