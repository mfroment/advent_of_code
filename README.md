## Advent of Code

The inputs are for when logged into AoC site with that GitHub account!

### Setup poetry environment
poetry install

### Setup daily problem
```shell
mkdir y_YYYY
cd y_YYYY
# Enter venv
poetry shell
# Boilerplate code
../boiler/init.sh $(date +%d)
# Populate input using aocd - https://github.com/wimglenn/advent-of-code-data
aocd > input/d_$(date +%d).txt
```


### Power tools
- Graphs: `networkx`
- Input conversions: `eval` (unsafe), `ast.literal_eval` (safer)
- Sort: `functools.cmp_to_key` to use custom comparator: `[...].sort(key=cmp_to_key(my_cmp))`
