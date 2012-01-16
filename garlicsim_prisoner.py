### @export "imports"
from garlicsim_lib.simpacks import prisoner
import csv
import garlicsim
import json

### @export "constants"
NUMBER_OF_PLAYERS = 100
NUMBER_OF_STEPS = 100

### @export "setup-csv"
csv_filename = "dexy--sim-output.csv"
csv_file = open(csv_filename, "w")
data_writer = csv.writer(csv_file)

data_writer.writerow(["step", "agent", "points", "strategy"])

### @export "init-sim"
state = prisoner.State.create_messy_root(NUMBER_OF_PLAYERS)
i = -1

### @export "def-collect-data"
def collect_data():
    for j, agent in enumerate(state.players):
        strategy = agent.__class__.__name__
        data_writer.writerow([i, j, agent.points, strategy])

### @export "run"
collect_data()

for i in range(NUMBER_OF_STEPS):
    state = garlicsim.simulate(state)
    collect_data()

### @export "cleanup"
csv_file.close()

