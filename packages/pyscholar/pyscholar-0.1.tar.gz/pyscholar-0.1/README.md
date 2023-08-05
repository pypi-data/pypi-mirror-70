### About

The module `pyscholar` consists of functions to convert tables imported in pandas to latex or markdown format. It aso includes a function `replace_include` to replace the content of the file mentioned after `!include`.

### Installation

```
pip install pyscholar
```
### Usage

`pyscholar` is easy to use. Just import:

```python
from pyscholar import pandoc
```

#### For table conversion

Instantiate the `Table` class using: 
```python
tab = pandoc.Table(df)
```
Convert table to markdown and save as:
```python
tab.to_markdown('table.md')
```
Convert table to latex and save as:
```python
tab.to_latex('table.tex')
```

#### Replacing content of a file

To replace content of a file mentioned after `!include`, use `replace_include` function in `pandoc`.

Example:

If the file `infilename` contains the following line:
```markdown
!include table.md
```
Then, using `replace_include` will replace that line with contents of file `table.md`.

```python
from pandoc import replace_include

replace_include(infilename, outfilename)
```