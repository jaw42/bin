-- Created:  Tue 21 Feb 2017
-- Modified: Tue 21 Feb 2017
-- Author:   Josh Wainwright
-- Filename: get_year.lua

local seconds = os.time()
local n = 1e6

local years = {}

years[1] = os.date('*t', seconds).year

years[2] = tonumber(os.date('%Y', seconds))

local tmp = seconds/31557600 + 1970.5
years[3] = tmp - tmp%1

print(seconds, table.concat(years, ', '))

local x = os.clock()
for i=1, n do
	local year = os.date('*t', seconds).year
end
print('date table:', os.clock() - x .. ' seconds')

local x = os.clock()
for i=1, n do
	local year = tonumber(os.date('%Y', seconds))
end
print('date tonumber:', os.clock() - x .. ' seconds')

local x = os.clock()
for i=1, n do
	-- 31557600 = 60*60*24*365.25 = Secs in a year
	local year = seconds / 31557600 + 1970.5
	year = year - (year % 1)
end
print('manual calc:', os.clock() - x .. ' seconds')
