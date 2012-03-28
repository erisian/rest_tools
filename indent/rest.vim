" reStructuredText indent file
" Language:	        reStructuredText
" Maintainer:	    Tadhg O'Higgins <vimrest@tadhg.com>
" Original Author:  Tadhg O'Higgins <vimrest@tadhg.com> 
" Last Change:      2010 Jan 16
" Some inspiration taken from Nikolai Weibull's rest indenter.


" if exists("b:did_indent")
"  finish
" endif
"let b:did_indent = 1

setlocal indentexpr=GetRSTIndent()
setlocal indentkeys=!^F,o,O
setlocal nosmartindent
setlocal noai

if exists("*GetRSTIndent")
  finish
endif

function GetRSTIndent()
"  let lnum = prevnonblank(v:lnum - 1)
  let lnum = prevnonblank(v:lnum)
  if lnum == 0
    return 0
  endif

  let ind = indent(lnum)
  let line = getline(lnum)

  if line =~ "::"
    let ind = ind + 4
  endif
"  if line =~ '^\s*[-*+]\s'
"    let ind = ind + 2
"  elseif line =~ '^\s*\d\+.\s'
"    let ind = ind + matchend(substitute(line, '^\s*', '', ''), '\d\+.\s\+')
"  endif
"
"  let line = getline(v:lnum - 1)
"
"  if line =~ '^\s*$'
"    execute lnum
"    call search('^\s*\%([-*+]\s\|\d\+.\s\|\.\.\|$\)', 'bW')
"    let line = getline('.')
"    if line =~ '^\s*[-*+]'
"      let ind = ind - 2
"    elseif line =~ '^\s*\d\+\.\s'
"      let ind = ind - matchend(substitute(line, '^\s*', '', ''),
"            \ '\d\+\.\s\+')
"    elseif line =~ '^\s*\.\.'
"      let ind = ind - 3
"    else
"      let ind = ind
"    endif
"  endif

  return ind
endfunction
