local str1 = [[
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam fermentum felis vel eros commodo sagittis. Fusce mi eros, vulputate in ornare eu, accumsan in eros. Ut fringilla, felis vitae vehicula tempor, enim dolor interdum ligula, vitae facilisis leo nisl vel magna. Suspendisse ullamcorper rhoncus mi a commodo. Ut ut felis quis est ornare maximus. Nulla facilisi. Donec et posuere nulla, vel sodales purus. Maecenas id orci arcu. Morbi rutrum ipsum nec nisi interdum tincidunt. Fusce ornare mattis justo, nec fermentum ligula consequat varius. Vestibulum eu diam tortor. Vestibulum et sollicitudin diam. Suspendisse eu nunc vehicula, vulputate libero non, semper tortor. Phasellus pretium justo vitae pulvinar fermentum.

Donec congue semper tellus, et mattis metus elementum et. Duis vel eleifend est. Morbi pharetra consequat sapien vitae cursus. Donec porttitor ornare magna, non tincidunt dolor ullamcorper nec. Duis a leo sagittis eros laoreet bibendum quis quis massa. Sed lacinia magna non fringilla ornare. Quisque luctus nec diam eget vestibulum. Quisque aliquet lectus at lorem blandit eleifend. Ut massa orci, imperdiet et nisl ut, pellentesque suscipit quam. Nulla sit amet dui pellentesque, aliquet nulla id, commodo nunc. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus scelerisque est quis mauris sollicitudin, sed congue ex cursus. Ut interdum condimentum dolor, sit amet eleifend ipsum congue nec.

Mauris pharetra sagittis eros, vel euismod nunc semper quis. Fusce porttitor, erat convallis elementum volutpat, ligula nisl congue ex, et eleifend urna ligula sit amet nulla. Suspendisse non risus et nibh ultricies ornare sed quis odio. Nunc augue lectus, interdum eu urna et, condimentum porttitor turpis. Nulla eu ex a turpis efficitur dictum. Nulla lobortis ipsum lectus, sed sollicitudin ipsum sodales ac. Sed rutrum elit sit amet dui rutrum suscipit. Donec nisl velit, rhoncus id porta vitae, aliquam at risus. Morbi purus risus, iaculis vitae tincidunt eu, ultrices in nunc. Praesent vulputate vitae metus eu scelerisque. Sed vitae erat molestie, pulvinar arcu a, ornare arcu. Donec sollicitudin velit in pellentesque venenatis.

Quisque semper congue auctor. Aenean commodo fermentum orci, eget scelerisque est feugiat at. Donec posuere, risus id lacinia tincidunt, tellus diam fringilla justo, vel interdum enim turpis vitae turpis. Duis sit amet metus vestibulum, scelerisque purus egestas, condimentum diam. Aenean lacinia, sem nec aliquam feugiat, enim justo iaculis metus, non aliquet nulla urna pellentesque nunc. Duis eget rutrum est. Mauris mollis neque ut augue scelerisque dignissim. Maecenas scelerisque ligula semper, sagittis est nec, sagittis odio. Sed turpis dolor, dignissim at fermentum a, blandit at lacus.

Suspendisse non placerat lorem, at sodales felis. Duis nisi enim, posuere vel aliquet condimentum, ullamcorper vel ipsum. Nullam dignissim hendrerit fermentum. Vivamus at augue in nisl faucibus cursus vel sed libero. Donec quis ligula vestibulum, pulvinar mauris ut, elementum sem. Aenean finibus pharetra faucibus. Duis fermentum orci at nibh faucibus, sed placerat quam tincidunt. Donec bibendum, tortor ac consequat laoreet, urna tellus tincidunt ipsum, a lacinia nisi augue vitae nisl. Integer id mi et odio porta placerat eu eu purus. Phasellus gravida est non velit tincidunt, sed iaculis erat porta. Suspendisse fringilla felis nibh, id faucibus ligula tristique nec.
]]

local str2 = [[Lorem ipsum dolor sit amet]]

local funcs = {}

-- for loop
funcs['for loop'] = function(str)
	local len = 0
	for i=1, #str do
		local c = str:sub(i,i)
		len = len + 1
	end
	return len
end

-- gmatch
funcs['gmatch  '] = function(str)
	local len = 0
	for c in str:gmatch('.') do
		len = len + 1
	end
	return len
end

-- gsub
funcs['gsub    '] = function(str)
	local len = 0
	str:gsub(".", function(c)
		len = len + 1
	end)
	return len
end

for name, func in pairs(funcs) do
	local x = os.clock()
	local len
	for n=1, 10000 do
		len = func(str1)
	end
	print(name, os.clock()-x, len)
end
