-- Created:  Wed 07 Dec 2016
-- Modified: Wed 07 Dec 2016
-- Author:   Josh Wainwright
-- Filename: date2secs.lua
local function using_match(date)
	local hours, mins, secs = date:match('(%d%d)(%d%d)(%d%d)')
	return tonumber(hours)*3600 + tonumber(mins)*60 + tonumber(secs)
end

local function using_match2(date)
	local hours, mins, secs = date:match('(..)(..)(..)')
	return tonumber(hours)*3600 + tonumber(mins)*60 + tonumber(secs)
end

local function using_sub(date)
	local hours = tonumber(date:sub(1,2))
	local mins = tonumber(date:sub(3,4))
	local secs = tonumber(date:sub(5,6))
	return hours*3600 + mins+60 + secs
end

local function test(func, var, n)
	local start = os.clock()
	for i=1, n do
		func(var)
	end
	io.write(string.format("%.3f\n", os.clock() - start))
end

local n = 1000000
io.write('n = ', n, '\n')
io.write('Match: ')
test(using_match,  '20161207', n)
io.write('Match2: ')
test(using_match2, '20161207', n)
io.write('Sub: ')
test(using_sub,    '20161207', n)
