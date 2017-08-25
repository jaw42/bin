-- Created:  Wed 15 Mar 2017
-- Modified: Wed 15 Mar 2017
-- Author:   Josh Wainwright
-- Filename: string_find.lua

local n = 1e7

local str = [[
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnoprstuvwxyz
abcdefghijklmnopqrstuvwxyz
abcdefghijklmnopqrstuvwxyz
]]

local x = os.clock()

local pos = 0
for i=1, n do
	pos = str:find('mnopq', 1, false)
end

print('Patterns enabled', os.clock() - x)

local x = os.clock()

local pos = 0
for i=1, n do
	pos = str:find('mnopq', 1, true)
end

print('Patterns disabled', os.clock() - x)
