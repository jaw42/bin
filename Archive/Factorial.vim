" Created:  Fri 12 Feb 2016
" Modified: Thu 23 Jun 2016
" Author:   Josh Wainwright
" Filename: Fact.vim

set maxfuncdepth=10000

" Iteration
function! Fact_iter(n) abort
	let n = a:n
	let a = 1
	while n > 0
		let a = a * n
		let n = n - 1
	endwhile
	return a
endfunction

" Standard Recursion
function! Fact_rec(n) abort
	if a:n == 0
		return 1
	endif
	return a:n * Fact_rec(a:n - 1)
endfunction

" Tail Recursion
function! Fact_tail_aux(n, sum) abort
	if a:n == 0
		return a:sum
	endif
	return Fact_tail_aux(a:n - 1, a:sum * a:n)
endfunction

function! Fact_tail(n)
	return Fact_tail_aux(a:n, 1)
endfunction

function! N(fn, n)
	for i in range(0, 1000)
		call call(a:fn, [a:n])
	endfor
	return call(a:fn, [a:n])
endfunction

for func in ['Fact_iter', 'Fact_rec', 'Fact_tail']
	let start = reltime()
	echo func N(func, 100.0)
	echo reltimestr(reltime(start))
endfor
