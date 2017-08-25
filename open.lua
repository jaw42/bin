#!/usr/bin/lua
-- Created:  Thu 19 Jan 2017
-- Modified: Fri 20 Jan 2017
-- Author:   Josh Wainwright
-- Filename: open.lua
local mappings_file = os.getenv('HOME') .. '/Bin/open.dl'

-- Exit with error
local function error(str)
	io.stderr:write(str, '\n')
	os.exit(1)
end

-- Run command, including expanding env vars of form $EDITOR
local function run_cmd(cmd, file)
	cmd = cmd:gsub('%$(%u+)', os.getenv)
	local fullcmd = cmd .. ' "' .. file .. '"'
	io.stderr:write(fullcmd, '\n')
	os.execute(fullcmd)
end

-- Add a new mapping at the start of the list
local function new_mapping(mappings, pat, cmd)
	local conf = io.open(mappings_file, 'w')
	conf:write('-- Modified: ', os.date('%Y-%m-%d'), '\n')

	conf:write('return {\n')

	-- Write the given mapping first so it has highest priority
	conf:write(('\t{%q, %q},\n'):format(pat, cmd))

	for i=1, #mappings do
		local pat, cmd = mappings[i][1], mappings[i][2]
		conf:write(('\t{%q, %q},\n'):format(pat, cmd))
	end

	conf:write('}\n')
end

local mappings = dofile(mappings_file)
local modify = false
local cmd, file

if not os.execute() then error('OS shell not available') end

if #arg == 2 then
	if arg[1]:sub(1,1) == '-' then
		if arg[1]:find('m') then
			modify = true
		end
	else
		cmd = arg[1]
	end
	file = arg[2]
elseif #arg == 1 then
	file = arg[1]
else
	error('Wrong number of arguments')
end

local i = 1
while (not cmd) and i <= #mappings do
	if file:match(mappings[i][1]) then
		cmd = mappings[i][2]
	end
	i = i + 1
end

if (not modify) and cmd then
	run_cmd(cmd, file)

else
	local ext = file:match('([^.]+)$')
	io.stderr:write('Mapping not found: ', ext, '\n')
	io.stderr:write('Pattern [%.', ext, '$]: ')
	local pat = io.read('*line')
	if pat == '' then
		pat = '%.' .. ext .. '$'
	end

	io.stderr:write('Command : ')
	local cmd = io.read('*line')
	run_cmd(cmd, file)

	io.stderr:write('Add mapping: "', pat, '" -> "', cmd, '"? [Yn] ')
	local resp = io.read('*line')
	if resp == '' or resp == 'y' or resp == 'Y' then
		io.stderr:write('Adding\n')
		new_mapping(mappings, pat, cmd)
	else
		io.stderr:write('Not adding\n')
	end
end
