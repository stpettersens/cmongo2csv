# cmongo2csv
<!-- [![Build Status](https://travis-ci.org/stpettersens/cmongo2sql.svg?branch=master)](https://travis-ci.org/stpettersens/cmongo2sql) [![Build status](https://ci.appveyor.com/api/projects/status/github/stpettersens/cmongo2sql?branch=master&svg=true)](https://ci.appveyor.com/project/stpettersens/cmongo2sql) -->

Utility to convert a MongoDB JSON dump to a CSV file.

Usage: `cmongo2csv -f data.json -o data.csv`

Tested with:
* Python 2.7.9 and PyPy 2.5.1 (works)
* IronPython 2.7.5 (use IPY tweaked version): 
* `ipy cmongo2csv.ipy.py -f data.json -o data.csv`).
* Jython 2.5.3 (use Jython tweaked version with [Jyson](http://opensource.xhaus.com/projects/jyson)): 
* `jython jcmongo2csv.py -f data.json -o data.csv`)
