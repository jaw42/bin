-- Created:  Thu 14 Sep 2017
-- Modified: Thu 14 Sep 2017
-- Author:   Josh Wainwright
-- Filename: Bin/Archive/demos/neighbours.lua

--[[
  Simple demo using an algorithm to generate a set of random coordinates
  that are evenly spaced apart from each other. Generates a number of
  trail points, then works out which of those is the furthest away from
  all of the existing points that have so been accepted.

  numCandidates sets how many trail points should be created.
  fraction sets the fraction of the total space to populate.

  Uses the current size of the terminal window if accessible.
--]]

local numCandidates = 10
local fraction = 0.03

local samples = {}
local width = tonumber(os.getenv('COLUMNS')) or 80
local height = tonumber(os.getenv('LINES'))-1 or 30
local pointsCount = width*height*fraction

local function distance(a, b)
	return math.sqrt((a[1] - b[1])^2 + (a[2] - b[2])^2)
end

local function findClosest(set, newPoint)
	local closestPoint = newPoint
	local minDistance = 9e9
	for i=1, #set do
		local point = set[i]
		local dist = distance(point, newPoint)
		if dist < minDistance then
			closestPoint = point
			minDistance = dist
		end
	end
	return closestPoint
end

local function sample()
	local bestCandidate
	local bestDistance = -1
	for i=1, numCandidates do
		local c = {math.random(width), math.random(height)}
		local d = distance(findClosest(samples, c), c)
		if d > bestDistance then
			bestDistance = d
			bestCandidate = c
		end
	end
	return bestCandidate
end

while true do
	io.read()
	math.randomseed(os.time())
	local startClock = os.clock()

	local mapping = {}
	for i=1, pointsCount do
		local p = sample()
		samples[i] = p
		mapping[p[1]..':'..p[2]] = true
	end

	local output = {}
	local count = 0
	for i=1, height do
		local row = {}
		for j=1, width do
			local bool = mapping[j..':'..i]
			row[j] = bool and '#' or ' '
			count = count + (bool and 1 or 0)
		end
		output[i] = table.concat(row)
	end
	local duration = os.clock() - startClock
	local status = ('%i x %i, %i points, %.4f seconds'):format(width, height, count, duration)
	output[#output+1] = status
	io.write(table.concat(output, '\n'))
end
