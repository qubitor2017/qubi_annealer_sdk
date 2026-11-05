"""Legacy qubif_sdk-compatible Max-Cut example. Defaults to the CPU mock backend.

Run on hardware explicitly: python examples/legacy_maxcut_demo.py --backend n512 --port /dev/ttyUSB0
"""
import argparse
from qubif_sdk import build_maxcut, decode_maxcut, AnnealerClient

parser = argparse.ArgumentParser()
parser.add_argument('--backend', choices=['mock_exact', 'n512', 'n1024'], default='mock_exact')
parser.add_argument('--port', default='/dev/ttyUSB0')
args = parser.parse_args()
edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
J, h = build_maxcut(edges, n_nodes=4)
client = AnnealerClient(port=args.port, backend=args.backend)
try:
    spins, energy = client.solve(J, h, n=4, problem_type=0, num_sweeps=4000)
finally:
    client.close()
print('Spins:', spins)
print('Energy:', energy)
print('Cut:', decode_maxcut(spins, edges))
