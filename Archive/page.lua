function page(file)
	local f, err = io.open(file, 'r')
	if f == nil then
		print(err)
		return
	end

	local lines = {}
	local n = 0
	for line in f:lines() do
		n = n + 1
		lines[n] = line
	end

	os.execute('stty cbreak < /dev/tty > /dev/tty 2>&1')

	local b = 1
	local d = 55 --10 -- terminal height
	while true do
		local e = math.min(n, b+d-1)
		for i=b, e do
			print(i, lines[i])
		end
		io.write(':'); io.flush()
		local key = io.read(1)
		io.write('\n'); io.flush()

		if key == 'q' then break end
		if key == 'b' then b = math.max(1, b-d) end
		if key == 'f' then b = math.min(n, b+d) end
		if key == '\n' then b= math.min(n, b+1) end
	end

	os.execute('stty -cbreak < /dev/tty > /dev/tty 2>&1')
end

page(arg[1])
