" reST-specific settings
:let g:restfts="rest"
" Set filetype to rest:
nnoremap <Leader>r :set ft=rest<CR>
" em dash:
exe "au FileType " . g:restfts . " :inoremap <buffer> -- —"
" en dash:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;- –"
" minus sign:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;m −"
" multiplication sign:
exe "au FileType " . g:restfts . " :inoremap <buffer> ;x ×"
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
let s:path = expand("<sfile>:p:h:h") . "/rest_get_refs/rest_get_refs.py"
function! RestGetReferences(rng1, rng2)
    exe a:rng1 . "," . a:rng2 . "!" . s:path
endfunction
command! -range=% Grefs call RestGetReferences(<line1>, <line2>)
" /Call rest_get_refs.py

" Take a definition list indented by n spaces and sort it by dt alphabetical
" The core of this was written by Seth Milliken; I made minor tweaks to cover
" some edge cases.
function! SortDefinitionList(rng1, rng2)
    let limit = match(getline(a:rng1), "[^[:space:]]")
    let newline = "<SortDefinitionListNL>"
    let doublenewline = "<SortDefinitionListDOUBLE>"
    let marker = "<SortDefinitionListGROUP>"
    let items = join(getline(a:rng1, a:rng2), newline)
    let items = substitute(items, newline . newline, doublenewline, 'g')
    let items = substitute(items, newline . '\ze\s\{' . limit . '}\S', marker, 'g')
    let items = substitute(items, doublenewline, newline . newline, 'g')
    let itemlist = split(items, marker)
    let itemlist = sort(itemlist)
    let result = []
    for group in itemlist
        call extend(result, split(group, newline))
    endfor
    for line in range(a:rng1, a:rng2)
        call setline(line, result[line - a:rng1])
    endfor
endfun
command! -range=% Sortdl call SortDefinitionList(<line1>, <line2>)
" /Sort definition list
