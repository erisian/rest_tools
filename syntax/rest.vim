" reStructuredText syntax file
" Language:	        reStructuredText
" Maintainer:	    Tadhg O'Higgins <github@tadhg.com>
" Original Author:  Tadhg O'Higgins <guthub@tadhg.com> 
" Last Change:      2012-03-25

if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

syn case ignore

syn region restSubstitutionTarget matchgroup=Boolean start="|" skip="\\|" end="|" oneline concealends
syn region restEmphasis matchgroup=Underlined start=/\*/ end=/\*/ oneline concealends
syn region restStrong matchgroup=Structure start=/\*\*/ end=/\*\*/ oneline concealends
syn region restLinkWithTitle matchgroup=LineNr start=/\^/ end=/\^/ oneline concealends
syn region restSpecialRole matchgroup=Function start=/\~/ end=/\~/ oneline concealends
syn region restInterpretedText matchgroup=restLink start=/`/ end=/`/ oneline concealends
syn match  restLink /`[^`]\+`_\{1,2\}/
syn match  restExplicitLink /[a-z]\+\:\/\/[^ ]\+/ contains=@NoSpell
syn match  restExplicitLink2 /<[^>]\+>/ms=s+1,me=e-1 contains=@NoSpell
syn region restInlineLiteral matchgroup=Constant start="``" end="``" oneline concealends
syn region restLiteralBlock start=/^[^ ]\+.*::\zs\n/ end=/\n\ze[^ ]\{1\}/ contains=@NoSpell
syn region restLiteralBlock2 start=/^::\zs\n/ end=/\n\ze[^ ]\{1\}/ contains=@NoSpell
syn region restLiteralBlock3 start=/^[ ]\{4\}[^ ]\+.*::\zs\n/ end=/\n\ze[ ]\{4\}[^ ]\{1\}/ contains=@NoSpell
syn region restLiteralBlock4 start=/^[ ]\{8\}[^ ]\+.*::\zs\n/ end=/\n\ze[ ]\{8\}[^ ]\{1\}/ contains=@NoSpell
syn region restLiteralBlock5 start=/^[ ]\{12\}[^ ]\+.*::\zs\n/ end=/\n\ze[ ]\{12\}[^ ]\{1\}/ contains=@NoSpell
syn match  restSectionTitle /^[ ]*[=\-~`#"^\+\*\:]\{3,\}$/
syn match  restSimpleTable /^[ ]*[=]\{2,\} [= ]\+/
syn region restComment start=/^\.\. .*/ end=/\n\S/me=e-1
syn region restComment2 start=/^    \.\. .*/ end=/\n[ ]\{,4}\S/me=e-1
syn region restSubstitutionSource start=/[ ]*\.\. |[^|]\+|/ end=/$/ contains=@NoSpell
syn match  restDirective /^[ ]*\.\.\s[A-z][A-z0-9-_]\+::/ contains=@NoSpell
syn match  restDirectiveCodeContent /^[ ]*\.\. \(class\|container\|include\)::.*/ contains=@NoSpell
syn region restLinkSource start=/[ ]*\.\. _.*/ end=/$/
syn match  restCitation /\[[A-z][A-z0-9_-]*\]_/
syn match  restNumberFootnote /\[[0-9#]\+\]_/
syn match  restSymbolFootnote /\[\*\]_/
syn region restCitationSource start=/[ ]*\.\. \[[A-z][A-z0-9_-]*\]/ end=/$/ contains=@restContained
syn region restNumberFootnoteSource start=/[ ]*\.\. \[[0-9#]\+\]/ end=/$/ contains=@restContained
syn region restSymbolFootnoteSource start=/[ ]*\.\. \[\*\]/ end=/$/ contains=@restContained
syn match  restField /:[A-z][A-z0-9 	=\s\t_\-\/;`<>\^]*:/
syn match restListBullet /+   /
syn match restListNumber /#.  /
syn match restDefinitionTitle /^[A-z0-9@\/]\{1\}.*\n[ ]\{4}\S\{1\}/me=e-5
syn match restDefinitionTitle2 /^[ ]\{4\}[A-z0-9@\/]\{1\}.*\n[ ]\{8\}\S\{1\}/me=e-9
syn match restDefinitionTitle3 /^[ ]\{8\}[A-z0-9@\/]\{1\}.*\n[ ]\{12\}\S\{1\}/me=e-13
syn match restDefinitionTitle4 /^[ ]\{12\}[A-z0-9@\/]\{1\}.*\n[ ]\{16\}\S\{1\}/me=e-17
syn region restGridTable start=/\n\n\s*+[\-=]\+.*\n/ end=/\n\s*+[\-=]\+.*\n\n/ contains=restGridTableCell
syn match restLitLine /\s*| /
syn match  restEmDash /—/
syn match  restEnDash /–/
syn match  restMinusSign /−/
syn region restDoubleQuotes start="“" end="”" contains=@restContained
syn region restSingleQuotes start="‘" end="’" contains=@restContained
syn cluster restContained contains=restEmphasis,restStrong,restLinkWithTitle,restSpecialRole,restInterpretedText,restLink,restEmDash,restEnDash,restMinusSign,restDoubleQuotes,restSingleQuotes,restBreakSpace,restSubstitutionTarget,restInlineLiteral,restNumberFootnote,restSymbolFootnote
syn region restParens matchgroup=restParens start="(" end=")" contains=@restContained,restParens2
syn region restParens2 matchgroup=restParens2 start="(" end=")" contained contains=@restContained
syn match  restEOL / $/ containedin=ALL
syn match restBreakSpace /\\ / conceal

highlight link restCitation Conditional
highlight link restCitationSource Conditional
highlight link restComment Comment
highlight link restComment2 Comment
highlight link restDefinitionTitle Label
highlight link restDefinitionTitle2 restDefinitionTitle
highlight link restDefinitionTitle3 restDefinitionTitle
highlight link restDefinitionTitle4 restDefinitionTitle
highlight link restDirective Function
highlight link restDirectiveCodeContent Function
highlight link restDoubleQuotes String
highlight link restEmDash Number
highlight link restEmphasis Underlined
highlight link restEnDash Keyword
highlight link restExplicitLink Keyword
highlight link restExplicitLink2 Keyword
highlight link restField Structure
highlight link restFootnote Keyword
highlight link restGridTable Conditional
highlight link restGridTableCell Normal
highlight link restInlineLiteral Constant
highlight link restInterpretedText Define
highlight link restLink Keyword
highlight link restLinkWithTitle LineNr
highlight link restLinkSource Keyword
highlight link restListBullet Keyword
highlight link restListNumber Keyword
highlight link restLiteralBlock Constant
highlight link restLiteralBlock2 Constant
highlight link restLiteralBlock3 Constant
highlight link restLiteralBlock4 Constant
highlight link restLiteralBlock5 Constant
highlight link restLitLine Keyword
highlight link restMinusSign LineNr
highlight link restNumberFootnote Repeat
highlight link restNumberFootnoteSource Repeat
highlight link restParens Label
highlight link restParens2 LineNr
highlight link restSectionTitle Keyword
highlight link restSimpleTable Constant
highlight link restSingleQuotes Type
highlight link restSpecialRole Function
highlight link restStrong Structure
highlight link restSubstitutionSource Boolean
highlight link restSubstitutionTarget Boolean
highlight link restSymbolFootnote Type
highlight link restSymbolFootnoteSource Type
