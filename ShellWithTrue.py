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
PIPE = " | "
GOODBYE = "My battery is low and it's getting dark..."

BUILTINS = [CD, PWD, JOBS, BG, FG, HISTORY, EXIT]

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

	if uinput == 'jobs':
		return

	if uinput == 'bg':
		return

	if uinput == 'fg':
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
	special_chars_list = ["|",">","<"]
	

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
	good_uin = False
	while not good_uin:
		uinput = input(PROMPT)
		if len(uinput) != 0:
			good_uin = True
	#MAKES THE LARGE ASSUMPTION THAT ANY BUILTINS ARE PASSED IN IN ISOLATION
	if uinput.split()[0] in BUILTINS:
				#run builtin function	
				p = builtins(uinput[0])
	else:
		#shlex.quote()
		p2 = subprocess.Popen(uinput, shell = True)


				
def main():
	#cmd, scpil = seperate_command()
	exec(cmd, scpil)
	#tash_loop()
	return

main()