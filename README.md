## Advent of Code

The inputs are for when logged into AoC site with that GitHub account!

### Setup poetry environment
poetry install

### Setup daily problem
```shell
_init/run.sh   # optional: _init/run.sh [day] [year]
```
This generates:
- `y_<year>/d_<day>.py`
- `y_<year>/input/d_<day>.txt`
- `y_<year>/tests/test_<day>.py`
- `y_<year>/tests/input/d_<day>.py`

Note: this uses []`aocd`](https://github.com/wimglenn/advent-of-code-data) to generate input file, test code and test data. Test files are almost always not directly usable (if only because the example result of part 2 is not known outright).

Run code and tests:
```shell
python y_<year>/d_<day>.py
pytest y_<year>    # alt. y_<year>/tests/test_<day>.py
```


### Power tools
- Graphs: `networkx`
- Input conversions: `eval` (unsafe), `ast.literal_eval` (safer)
- Sort: `functools.cmp_to_key` to use custom comparator: `[...].sort(key=cmp_to_key(my_cmp))`
