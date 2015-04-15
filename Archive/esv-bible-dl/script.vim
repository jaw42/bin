function! CleanBible()
	silent %s/<.\{-}>/ /ge
	silent %s/&#8220;/"/ge
	silent %s/&#8221;/"/ge
	silent %s/&#8216;/'/ge
	silent %s/&#8217;/'/ge
	silent %s/&#8212;/--/ge
	silent %s/&#9668;//ge
	silent %s/&#9658;//ge
	silent %s/'"/' "/ge
	silent $s/Footnotes.*$//e
	silent %s/   \a    / /ge
	silent 1s/Bible  >  ESV  > //e
	silent 1s/ESV//e
	silent 1s/English Standard Version//e
	/\d \{3,4}\S/
	normal gg0dnI   jk
	silent %s/^.\{-} \{3}\ze \{3}\d\+ \{4}//e
	silent %s/ \+/ /ge
	silent %s/ $//e
	silent %s/ \([,.:;!]\)//e
	silent %s/^ \+\(\d\) \+/ \1 /e
	silent %s/^ \+\(\d\d\) \+/\1 /e
	let chapter = expand('%:t:r:s/.*_//')
	let book = expand('%:s/.\{-}_//:s/_.\{-}$//:s/\<./\u&/g')
	exe 'silent %s/^/[' . chapter . '] /e'
	silent %s/^\[0\([1-9]\+\)\]/[ \1]/e
	silent %s/^\[00\([1-9]\+\)\]/[  \1]/e
	silent %s/^\[.\{-}\] \+\zs \a.\{-}\ze\d\d//e
	silent %s/^\[.\{-}\] \+\zs\a.\{-}\ze\d//e
	g/^\[/put _
	
	if chapter == 01
		exe 'normal ggO#jko# ' . book . 'jko#'
		put _
	endif
	1
endfunction
