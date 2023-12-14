#!/bin/bash

SCRIPT_PATH="$(realpath $0)"
SCRIPT_DIR="$(dirname $SCRIPT_PATH)"
PROJECT_DIR="$SCRIPT_DIR/.."
TEMPLATE_DIR="$SCRIPT_DIR/cookiecutter"
OUTPUT_DIR="$PROJECT_DIR"


# Default to current day and year if no arguments are provided
DAY=$(TZ="America/New_York" date +%d)
YEAR=$(TZ="America/New_York" date +%Y)

# Override day and year if arguments are provided
if [ $# -ge 1 ]; then
    DAY=$(printf "%02d" $1)
fi

if [ $# -eq 2 ]; then
    YEAR=$2
fi

# Fetch puzzle input and example input
PUZZLE_INPUT=$(aocd $DAY $YEAR)
EXAMPLE=$(aocd $DAY $YEAR --example)

# Extract answers from example input
EXAMPLE_ANSWER_A=$(echo "$EXAMPLE" | grep 'answer_a:' | awk '{print $2}')
EXAMPLE_ANSWER_B=$(echo "$EXAMPLE" | grep 'answer_b:' | awk '{print $2}')
EXAMPLE_INPUT=$(echo "$EXAMPLE" | perl -e '$is_data = 0; while (<>) { if (/^-{31} Example data 1\/1 -{31}$/){ $is_data = 1; } elsif (/^-{80}$/) { $is_data = 0; } elsif ($is_data) { print; }  }')

# Never overwrite tha main py file:
MAIN_PY_FILE="$OUTPUT_DIR/y_$YEAR/d_$DAY.py"
TEMP_PY_FILE="$OUTPUT_DIR/y_$YEAR/d_$DAY.py.temp"
INPUT_FILE="$OUTPUT_DIR/y_$YEAR/input/d_$DAY.txt"

# Check if the main Python file exists and rename it temporarily if it does
if [ -f "$MAIN_PY_FILE" ]; then
    mv "$MAIN_PY_FILE" "$TEMP_PY_FILE"
fi

cookiecutter --no-input --overwrite-if-exists --output-dir $OUTPUT_DIR \
    $TEMPLATE_DIR \
    year=$YEAR day=$DAY puzzle_input="$PUZZLE_INPUT" example_input="$EXAMPLE_INPUT" example_answer_a="$EXAMPLE_ANSWER_A" example_answer_b="$EXAMPLE_ANSWER_B" \

# Check if the temporary file exists and move it back
if [ -f "$TEMP_PY_FILE" ]; then
    mv "$TEMP_PY_FILE" "$MAIN_PY_FILE"
fi

code "$INPUT_FILE" "$MAIN_PY_FILE"
code --goto "${MAIN_PY_FILE}:11:1"