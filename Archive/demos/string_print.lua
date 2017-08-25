local start
local n = 1000000

for i=1, 1001, 1000 do
	local str = ('a'):rep(i)
	print('str lenght = ' .. str:len())
	
	io.write('Immediate write: ')
	start = os.clock()
	for i=1, n do
		io.stderr:write(str, '\n')
	end
	print(os.clock() - start)
	
	io.write('Table collect then write: ')
	start = os.clock()
	local t = {}
	for i=1, n do
		t[#t+1] = str
	end
	io.stderr:write(table.concat(t, '\n'), '\n')
	print(os.clock() - start)
	print()
end