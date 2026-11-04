"""Run with: python examples/maxcut_demo.py /dev/ttyUSB0"""
import sys
from qubif_sdk import build_maxcut, decode_maxcut, AnnealerClient

port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"

edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
J, h = build_maxcut(edges, n_nodes=4)

client = AnnealerClient(port=port)
spins, energy = client.solve(J, h, n=4, problem_type=0, num_sweeps=4000)
client.close()

print("Spins:", spins)
print("Energy:", energy)
print("Cut:", decode_maxcut(spins, edges))
