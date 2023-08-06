# Veazy
*Visualize your python code eazily*

`veazy` generates callgraphs for your python codebase by parsing the abstract syntax tree (its static, so it doesn't run your code).
Callgraphs can be convoluted, so `veazy` automagically determines a convenient complexity which you can then tweak. 

# Installation
`$ pip install veazy`

For `svg` output, you need graphviz:
`$ apt-get graphviz `

# Usage 
`cd` into where your code lives. 
The (automatic) pruning requires the option `-r ROOT_FILE` that allows to determine a relative depth with the `-c` option:
`veazy -r main.py -c -3`
![](examples/c_minus_3.svg)

For exclusion purposes, you may specify the SRC to be included:
`veazy -r main.py tag_*.py`

## Other options
| **Option**                     | **Description** |
|--------------------------------|------|
|-r, --root-file PATH            | A top-level entry from where relative depth is determined. |
|-o, --output-file PATH          | Write to this file. If None, svgs go to graph.svg. |
|-c, --complexity-offset INTEGER | To adjust the automatic depth. When depth is passed, this value is ignored. |
|-d, --depth INTEGER			 | Use an absolute depth.	 |
|-t, --output-type [dot\|svg]     | Output format. For svg, you need to have graphviz installed. |
|--version                       | Show the version and exit. |
|--help                          | Help yourself and exit. |


# Note
The version of pyan3 used in Veazy is mirrored from https://github.com/Technologicat/pyan.

# [License](https://gitlab.com/janscholten/veazy/-/blob/master/LICENCE)
