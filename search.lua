-- Created:  Fri 23 Sep 2016
-- Modified: Fri 23 Sep 2016
-- Author:   Josh Wainwright
-- Filename: search.lua
local lfs = require('lfs')

local opts = {}
opts.oneresult = false
opts.oneperfile = false
local size_limit = 1024*1024

function find_in_file_lines(file, pattern)
	local f = io.open(file)
	if not f then return end
	local lnum = 0
	for line in f:lines() do
		lnum = lnum + 1
		if line:find(pattern) then
			io.write(file, '\n')
			return
		end
	end
end

function find_in_file(file, pattern)
	local f = io.open(file)
	if not f then return end
	local lines = f:read('*all')
	f:close()
	if lines:find(pattern) then
		io.write(file, '\n')
		return
	end
end

function recurse_dir(path, pat)
	for file in lfs.dir(path) do
		if file ~= "." and file ~= ".." then
			local f = path..'/'..file
			local attrs = lfs.attributes(f)
			if attrs.mode == "directory" then
				if file ~= '.git' then
					recurse_dir(f, pat)
				end
			elseif attrs.size < size_limit then
				find_in_file(f, pat)
			end
		end
	end
end

local path = arg[2] or '.'
if lfs.attributes(path, 'mode') == 'directory' then
	recurse_dir(path, arg[1])
else
	find_in_file(path, arg[1])
end

