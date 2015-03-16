#!/bin/python
# Created:  Mon 16 Mar 2015
# Modified: Mon 16 Mar 2015
# Author:   Josh Wainwright
# Filename: amr_python.py

import os.path
import sys, getopt
import subprocess

isverbose = False
just_list = False
ignore=set(["plugged", "trunk", "repo_discount", "repo_parallel"])
include=["home"]
ispull_all = False
ispush_all = False
number_pulled = 0
number_pushed = 0
cmd_always = False
start_shell = False

# function run
def run(cmd, fail=1):
	cmd = cmd.split(' ')
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False)
	(output, err) = p.communicate()
	p_status = p.wait()
	if fail:
		if p_status == 0:
			return output.decode("utf-8")
		else:
			raise OSError
	else:
		return output.decode("utf-8")
# end function run

# function verbose
def verbose(pnt_str):
	if isverbose:
		print(pnt_str)
# end function verbose

# function indent
def indent(var, num=1):
	tabs = '\t' * int(num)
	var = var.replace("\n", "\n"+tabs).rstrip()
	print("%s%s" % (tabs, var))

# function get_git_repos
def get_git_repos():
	git_list = []
	home_path = os.path.expanduser("~/")
	if os.path.isfile(home_path + ".folders"):
		verbose("Using .folders file to locate git repos.")
		git_list = run("grep -E \.git$ " + home_path + ".folders", 0).split()
	else:
		try:
			verbose("Using locate to locate git repos.")
			git_list = run("locate -br \.git$").split()
		except:
			verbose("Command locate not availible. Using find instead.")
			git_list = run("find " + home_path + " -name .git").split()

	# only include each item if it doesn't match an item in ignore
	for ig_str in ignore:
		git_list = [ g for g in git_list if not ig_str in g ]

	# only include each item if it matches an item in include
	for inc_str in include:
		git_list = [ g for g in git_list if inc_str in g ]

	git_list = [ os.path.dirname(g) for g in git_list ]

	return git_list
# end function get_git_repos

# function pull_all
def pull_all():
	if ispull_all:
		run("git fetch origin", 0)
		log = run("git log --color=always HEAD..origin/master --oneline", 0)
		if log != "":
			indent(log)
			indent(run("git -c color.merge=always merge origin/master"))
			global number_pulled
			number_pulled = number_pulled + 1
# end function pull_all

# function push_all
def push_all():
	if ispush_all:
		if run("git remote").replace("\n") > 0:
			indent(run("git -c color.push=always push"))
			global number_pushed
			number_pushed = number_pushed + 1

# function options
def options(argv):
	try:
		opts, args = getopt.getopt(argv, "hvldux:i:r:sSaR")
	except getopt.GetoptError:
		usage()
		sys.exit(0)
	for opt, arg in opts:
		if opt in ["-h", "--help"]:
			usage()
			sys.exit(0)
		elif opt in ["-v", "--verbose"]:
			global isverbose
			isverbose = True
		elif opt in ["-l", "--list"]:
			global just_list
			just_list = True
		elif opt in ["-d", "--pull"]:
			global ispull_all
			ispull_all = True
		elif opt in ["-u", "--push"]:
			global ispush_all
			ispush_all = True
		elif opt in ["-x", "--ignore"]:
			global ignore
			ignore.append(arg)
		elif opt in ["-i", "--include"]:
			global include
			include.append(arg)
		elif opt in ["-r", "--run"]:
			global custom_cmd
			custom_cmd = arg
		elif opt in ["-s", "--shell"]:
			global start_shell
			start_shell = True
		elif opt in ["-S", "--summary"]:
			global summary
			summary = True
		elif opt in ["-a", "--always"]:
			global cmd_always
			cmd_always = True
		elif opt in ["-R", "--reset"]:
			ignore = []
			include = []
# end function options

options(sys.argv[1:])

if isverbose:
	print("Ignore List:")
	for ig in ignore: print("\t%s" % ig)
	print("Include List:")
	for ig in include: print("\t%s" % ig)
	print()

if just_list:
	for git_dir in get_git_repos():
		print(git_dir)
	sys.exit(0)

current_dir = os.getcwd()

for git_dir in get_git_repos():
	add_nl = False
	try:
		os.chdir(git_dir)
	except OSError:
		print("\033[0;31m%s: Folder not found.\033[0m" % git_dir)

	print("%s" % git_dir)
	status_output = run("git -c color.status=always status --ignore-submodules --short")
	number_lines = status_output.count("\n")

	if number_lines > 0:
		print("\tChanged %s" % number_lines)
		indent(status_output, 1)
		add_nl = True

	# custom command
	# start shall
	if start_shell:
		if number_lines != 0 or cmd_always:
			subprocess.call(['zsh', '-i'])

	ahead_output = run("git log --color=always --branches --not --remotes --oneline")
	number_ahead = ahead_output.count("\n")
	if number_ahead > 0:
		print("\tAhead: %s" %  (number_ahead) )
		indent(ahead_output, 1)
		push_all()
		add_nl = True

	pull_all()

	if add_nl: print()

if ispull_all:
	print("Number of repos pulled: %s" % number_pulled)
if ispush_all:
	print("Number of repos pushed: %s" % number_pushed)

os.chdir(current_dir)
