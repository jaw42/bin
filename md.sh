#!/bin/bash
# Created:  Fri 13 Feb 2015
# Modified: Wed 13 May 2015
# Author:   Josh Wainwright
# Filename: md.sh

# Configuration for building  markdown (Discount)
# ./configure.sh --enable-all-features --with-tabstops=4 --with-fenced-code --with-dl=Both --with-id-anchor

exists() {
	command -v "$@" > /dev/null
}

exists markdown || exit 1

poem=false
cssfile=""
[ "x$1" == "x-p" ] && poem=true && shift
[ "x$1" == "x-c" ] && shift && cssfile="$1"

input="$@"
mdfile=$(sed 's/£/\&pound;/' "$input")
htmlfile="${input%.*}.html"

if $poem; then
	mdfile=$(sed -e '2,$s#^#<br/>#' -e '/^<br\/>$/{N;s#<br/>##g}' <<< "$mdfile")
fi

if [ -z "$cssfile" ]; then
	repl="###########"
	cssfile=$(sed "1,/############$repl/d" "$0")
else
	cssfile=$(cat $cssfile)
fi

tmp=$(printf "%s\n%s\n" "$cssfile" "$mdfile")

markdown -S <<< "$tmp" > "$htmlfile"

exit 0
# # # # # # # # # # # #
### START .CSS FILE ###
#######################
<style type="text/css">
    * {
        margin: 0;
        padding: 0;
    }
    body {
        font: 13.34px helvetica, arial, freesans, clean, sans-serif;
        color: black;
        line-height: 1.4em;
        background-color: #F8F8F8;
        padding: 0.7em;
    }
    p {
        margin: 1em 0;
        line-height: 1.5em;
    }
    table {
        font-size: inherit;
        font: 100%;
        margin: 1em;
    }
    table th {
        border-bottom: 1px solid #bbb;
        padding: .2em 1em;
    }
    table td {
        border-bottom: 1px solid #ddd;
        padding: .2em 1em;
    }
    input[type=text], input[type=password], input[type=image], textarea {
        font: 99% helvetica, arial, freesans, sans-serif;
    }
    select, option {
        padding: 0 .25em;
    }
    optgroup {
        margin-top: .5em;
    }
    pre, code {
        font: 12px Menlo, Monaco, "DejaVu Sans Mono", "Bitstream Vera Sans Mono", monospace;
    }
    pre {
        margin: 1em 0;
        font-size: 12px;
        background-color: #eee;
        border: 1px solid #ddd;
        padding: 5px;
        line-height: 1.5em;
        color: #444;
        overflow: auto;
    }
    pre code {
        padding: 0;
        font-size: 12px;
        background-color: #eee;
        border: none;
    }
    code {
        font-size: 12px;
        background-color: #f8f8ff;
        color: #444;
        padding: 0 .2em;
        border: 1px solid #dedede;
    }
    img {
        border: 0;
        max-width: 100%;
    }
    abbr {
        border-bottom: none;
    }
    a {
        color: #4183c4;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    a code, a:link code, a:visited code {
        color: #4183c4;
    }
    h2, h3 {
        margin: 1em 0;
    }
    h1 {
        font-size: 170%;
        padding-top: .5em;
        margin-top: 1.5em;
    }
    h2 {
        font-size: 150%;
        margin-top: 1.5em;
        padding-top: .5em;
    }
    h3 {
        margin-top: 1em;
    }
    hr {
        border: 1px solid #ddd;
    }
    ul {
        margin: 1em 0 1em 2em;
    }
    ol {
        margin: 1em 0 1em 2em;
    }
    ul li, ol li {
        margin-top: .5em;
        margin-bottom: .5em;
    }
    ul ul, ul ol, ol ol, ol ul {
        margin-top: 0;
        margin-bottom: 0;
    }
    blockquote {
        margin: 1em 0;
        border-left: 5px solid #ddd;
        padding-left: .6em;
        color: #555;
    }
    dt {
        font-weight: bold;
        margin-left: 1em;
    }
    dd {
        margin-left: 2em;
        margin-bottom: 1em;
    }
    sup {
        font-size: 0.83em;
        vertical-align: super;
        line-height: 0;
    }
    @media screen and (min-width: 914px) {
        body {
            width: 854px;
            margin: 0 auto;
        }
    }
    @media print {
        body {
            background-color: #ffffff
        }
        table,
        pre {
            page-break-inside: avoid;
        }
        pre {
            word-wrap: break-word;
        }
    }
</style>
