local n = 1e7

-- Function call (math.min, math.max)
local x = os.clock()

local min, max = 9e9, 0
for i=10, n do
	min = math.min(min, i)
	max = math.max(max, i)
end

print('Func global', os.clock()-x, min, max)

-- Function call (stored local)
local x = os.clock()

local fmin, fmax = math.min, math.max
local min, max = 9e9, 0
for i=10, n do
	min = fmin(min, i)
	max = fmax(max, i)
end

print('Func local', os.clock()-x, min, max)

-- Approximate ternary expression
local x = os.clock()

local min, max = 9e9, 0
for i=10, n do
	min = i < min and i or min
	max = i > max and i or max
end

print('Ternary  ', os.clock()-x, min, max)

-- Explicit comparison if then end
local x = os.clock()

local min, max = 9e9, 0
for i=10, n do
	if i < min then min = i end
	if i > max then max = i end
end

print('Comparison', os.clock()-x, min, max)
