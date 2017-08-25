local a = {'one ', 'two ', 'three ', 'four ', 'five'}
local l
local n = 1000000
local start

print('n = ' .. n)

io.write('String concat: ')
start = os.clock()
	for i=1, n do
		l = a[1] .. a[2] .. a[3] .. a[4] .. a[5]
	end
print(os.clock() - start)

io.write('Table concat: ')
start = os.clock()
	local concat = table.concat
	for i=1, n do
		l = concat(a, '')
	end
print(os.clock() - start)

io.write('String format: ')
start = os.clock()
	local fmt = '%s%s%s%s%s'
	for i=1, n do
		l = fmt:format(a[1], a[2], a[3], a[4], a[5])
	end
print(os.clock() - start)
