# SDK scope and product boundary

The public SDK is the customer-facing host-side interface. It contains model representation, validation, compilation, host-side transformations, UART communication and result decoding.

The FPGA hardware implementation is a separate Qubitor product. The public SDK repository must not contain RTL, XDC, Vivado project files, bitstreams, debug probes, internal firmware source or manufacturing/programming assets. Customers obtain compatible programmed FPGA hardware and its approved device setup material from Qubitor.

The SDK does not implement general-purpose MILP/MIQP, arbitrary constraints, or a general Wolfram-like mathematics environment. PUBO is transformed on the host to QUBO; the hardware receives QUBO.
