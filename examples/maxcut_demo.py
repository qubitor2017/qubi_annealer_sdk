"""Four-node Max-Cut example. Defaults to CPU mock backend; hardware is explicit."""
import argparse
import qubitor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["mock_exact", "n512", "n1024"], default="mock_exact")
    parser.add_argument("--port", default="/dev/ttyUSB0")
    parser.add_argument("--scale", type=float, default=1.0)
    args = parser.parse_args()

    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    model = qubitor.build_maxcut(edges, n_nodes=4)
    kwargs = {"port": args.port, "scale": args.scale} if args.backend in ("n512", "n1024") else {}
    result = qubitor.solve(model, backend=args.backend, **kwargs)
    print("Backend:", result.backend)
    print("Bits:", result.solution)
    print("QUBO energy:", result.objective)
    print("Cut value:", qubitor.decode_maxcut(result.solution, edges))
    print("Status:", result.status)


if __name__ == "__main__":
    main()
