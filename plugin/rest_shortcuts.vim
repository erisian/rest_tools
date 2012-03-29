" reST-specific settings
:let g:restfts="rest"
" em dash:
exe "au FileType " . g:restfts . " :inoremap <buffer> -- —"
" en dash:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;- –"
" minus sign:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;m −"
" ellipsis:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;; …"
" open double quotation:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;q “"
" close double quotation:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;Q ”"
" close single quotation:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;' ’"
" bullet dot:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;o •"
" degree symbol:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;0 °"
" euro:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;e €"
" footnote:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;f \\ [*]_"
" numbered footnote:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;n \\ [#]_"
" rx sign:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;r ℞"
" cents:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;c ¢"
" pound currency:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;l £"
" therefore:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;t ∴"
" copyright:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;C ©"
" registered trademark:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;R ®"
" down arrow:
exe "au FileType " . g:restfts . " :inoremap <buffer> -_ ↓"
" right arrow:
exe "au FileType " . g:restfts . " :inoremap <buffer> -> →"
" up arrow:
exe "au FileType " . g:restfts . " :inoremap <buffer> -^ ↑"
" left arrow:
exe "au FileType " . g:restfts . " :inoremap <buffer> -< ←"
" alternative en dash shortcut:
exe "au FileType " . g:restfts . " :inoremap <buffer> -; –"
" alternative en dash shortcut 2:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;d –"
exe "au FileType " . g:restfts . " :set wm=0"
exe "au FileType " . g:restfts . " :setl colorcolumn=0"
exe "au FileType " . g:restfts . " :set spell"
" surround script to make e.g. yswq surround a word with curly quotes:
exe "au FileType " . g:restfts . " :let b:surround_113 = '“\r”'"
" surround script to make e.g. yswe surround a word with asterisks (emphasis):
exe "au FileType " . g:restfts . " :let b:surround_101 = '*\r*'"
" surround script to make e.g. yswl surround a word with reST link format:
exe "au FileType " . g:restfts . " :let b:surround_108 = '`\r`_'"
" surround script to make e.g. ysws surround a word with double asterisks (strong):
exe "au FileType " . g:restfts . " :let b:surround_115 = '**\r**'"
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

" Call rest_get_refs.py
function! RestGetReferences(rng1, rng2)
    let path = expand("<sfile>:p:h:h") . "/rest_get_refs/rest_get_refs.py"
    exe a:rng1 . "," . a:rng2 . "!" . path
endfunction
command! -range=% Grefs call RestGetReferences(<line1>, <line2>)
" /Call rest_get_refs.py
