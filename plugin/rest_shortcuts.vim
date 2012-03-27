" reST-specific settings
" em dash:
au FileType rest :inoremap <buffer> -- —
" en dash:
au FileType rest :inoremap <buffer> ;- –
" minus sign:
au FileType rest :inoremap <buffer> ;m −
" ellipsis:
au FileType rest :inoremap <buffer> ;; …
" open double quotation:
au FileType rest :inoremap <buffer> ;q “
" close double quotation:
au FileType rest :inoremap <buffer> ;Q ”
" close single quotation:
au FileType rest :inoremap <buffer> ;' ’
" bullet dot:
au FileType rest :inoremap <buffer> ;o •
" degree symbol:
au FileType rest :inoremap <buffer> ;0 °
" euro:
au FileType rest :inoremap <buffer> ;e €
" footnote:
au FileType rest :inoremap <buffer> ;f \ [*]_
" numbered footnote:
au FileType rest :inoremap <buffer> ;n \ [#]_
" rx sign:
au FileType rest :inoremap <buffer> ;r ℞
" cents:
au FileType rest :inoremap <buffer> ;c ¢
" pound currency:
au FileType rest :inoremap <buffer> ;l £
" therefore:
au FileType rest :inoremap <buffer> ;t ∴
" copyright:
au FileType rest :inoremap <buffer> ;C ©
" registered trademark:
au FileType rest :inoremap <buffer> ;R ®
" down arrow:
au FileType rest :inoremap <buffer> -_ ↓
" right arrow:
au FileType rest :inoremap <buffer> -> →
" up arrow:
au FileType rest :inoremap <buffer> -^ ↑
" left arrow:
au FileType rest :inoremap <buffer> -< ←
" alternative en dash shortcut:
au FileType rest :inoremap <buffer> -; –
" alternative en dash shortcut 2:
au FileType rest :inoremap <buffer> ;d –
au FileType rest :set wm=0
au FileType rest :setl colorcolumn=0
au FileType rest :set spell
" surround script to make e.g. yswq surround a word with curly quotes:
au FileType rest :let b:surround_113 = "“\r”"
" surround script to make e.g. yswe surround a word with asterisks (emphasis):
au FileType rest :let b:surround_101 = "*\r*"
" surround script to make e.g. yswl surround a word with reST link format:
au FileType rest :let b:surround_108 = "`\r`_"
" surround script to make e.g. ysws surround a word with double asterisks (strong):
au FileType rest :let b:surround_115 = "**\r**"
" /reST-specific settings

" Expand headings, used with header snippets.
function! RestHeading(char)
   let current_line = getline(".")
   " let len_prev_line = len(getline(line(".") - 1)) <- this fails for
   " multibyte characters, hence the following fix:
   let len_prev_line = strlen(substitute(getline(line(".") - 1), ".", "x", "g"))
   let ntimes = repeat(a:char, len_prev_line)
   return ntimes
endfunction
" /Expand headings
