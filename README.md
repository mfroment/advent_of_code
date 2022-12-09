## Advent of Code

The inputs are for when logged into AoC site with that GitHub account!

### Setup poetry environment
poetry install

### Setup daily problem
```shell
mkdir y_YYYY
cd y_YYYY
# Boilerplate code
../boiler/init.sh $(date +%d)
# Populate input using aocd - https://github.com/wimglenn/advent-of-code-data
poetry run aocd > input/d_$(date +%d).txt
```
