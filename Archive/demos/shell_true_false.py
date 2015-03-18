#!/usr/bin/env python
import subprocess
import time
import sys

cmd = "echo"
num = 100
innum = 10

for b in [True, False]:
	total = 0

	print("Shell is " + str(b))
	for j in range(1,num):

		start_time = time.time()

		for i in range(1,innum):

			p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=b)
			(output, err) = p.communicate()

		diff = time.time() - start_time
		total = total + diff
		sys.stdout.write(str(j) + '\r')
		sys.stdout.flush()

	print("\nAverage time: " + str(total/num/innum))
