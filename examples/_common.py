"""Shared runner for the Qubitor SDK 2.0 industry examples."""
from __future__ import annotations
import argparse
import json
import qubitor


def run(model, title, *, backend=None, port=None, scale=None, penalty=100.0, details=None):
    parser = argparse.ArgumentParser(description=title)
    parser.add_argument('--backend', choices=['mock_exact', 'n512', 'n1024'], default=backend or 'mock_exact')
    parser.add_argument('--port', default=port, help='Serial port for FPGA, e.g. /dev/ttyUSB0 or COM4')
    parser.add_argument('--scale', type=float, default=scale, help='FPGA coefficient scale')
    parser.add_argument('--penalty', type=float, default=penalty, help='Equality-constraint penalty')
    args = parser.parse_args()
    result = qubitor.solve(model, backend=args.backend, port=args.port, scale=args.scale,
                           penalty=args.penalty)
    print(f'\n{title}')
    print('=' * len(title))
    print('backend :', result.backend)
    print('status  :', result.status)
    print('energy  :', result.objective)
    print('bits    :', result.solution)
    if details:
        try:
            print('decoded :', json.dumps(details(result.solution), indent=2, default=str))
        except Exception as exc:
            print('decode error:', exc)
    if result.metadata:
        print('metadata:', json.dumps(result.metadata, indent=2, default=str))
    if args.backend == 'mock_exact':
        print('\nNote: mock_exact exhaustively solves small examples for learning/testing; it is not an FPGA benchmark.')
    else:
        print('\nNote: FPGA result is a candidate. Recompute the original objective and check constraints independently.')
    return result


def one_hot_decode(bits, width):
    return [next((j for j, v in enumerate(bits[i*width:(i+1)*width]) if v), None)
            for i in range(len(bits)//width)]
