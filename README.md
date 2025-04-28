# BeliefRev
Python based software that implement a belief revision mechanisim based on a belief based implementation.
# usage
```bash
pip install -r requirements.txt
python main.py
```
## commands
`a` - add formula to the belief base. each propositional variable should be a single letter capital letter
```
Input Command: a
Formula: Q & ~P
```
### operator precedence
### NOT SURE IF THIS IS TRUE ANYMORE
the high operaters are up on this list, the higher precedence they have, meaning they will be parsed before the ones below them
- `(<formula>)` - innermost sets of parentheses parsed first
- `~` - not
- `&` - and
- `|` - or
- `>>` - if ... then
- `<>` - if and only if
operators are the same precedence are parsed from left to right
