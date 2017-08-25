local max_int = 2^32

-- Implementation of djb2 hash algorithm
-- http://www.cse.yorku.ca/~oz/hash.html
local function hash(str)
	local h = 5381
	for i=1, str:len() do
		h = (h*33 + str:byte(i)) % max_int
	end
	return h
end

-- Implementation of sdbm hash algorithm
-- Requires Lua >5.3
----local function hash2(str)
----	h = 0
----	for i=1, str:len() do
----		h = str:byte(i) + (h << 6) + (h << 16) - h
----	end
----	return h
----end

----------------------------------------------

local hashes = {}
local t = 0
local collisions = 0

local function test(str)
	t = t + 1
	local h = hash(str)
	if hashes[h] then
		hashes[h][#hashes[h]+1] = str
	else
		hashes[h] = {str}
	end
end

for str in io.lines('/usr/share/dict/words') do test(str) end
for str in io.lines('wordlist.txt') do test(str) end

for k,v in pairs(hashes) do
	if #v > 1 then
		io.write(k, ': ', table.concat(v, ', '), '\n')
		collisions = collisions + (#v-1)
	end
end
print('Total: ' .. t)
print('Collisions: ' .. collisions)
