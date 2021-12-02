import os

SUM=2020
input=dict()
input_file = os.path.join(os.path.dirname(__file__), "input")
with open(input_file, mode="r") as f:
  while True:
    v = f.readline()
    if not v:
      break
    v = int(v)
    if v in input:
      print(f"{v}*{SUM-v}={v*(SUM-v)}")
      exit()
    input[SUM-v]=v

print("No solution found")