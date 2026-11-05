# Hardware connection

1. Obtain a compatible Qubitor FPGA device from Qubitor.
2. Use the device-specific connection and driver instructions supplied with that device.
3. Identify the correct serial port (for example `/dev/ttyUSB0` on Linux or `COM4` on Windows).
4. Install the SDK serial dependency with `python -m pip install -e '.[serial]'`.
5. Select the backend explicitly: `n512` or `n1024`.
6. Start with a small known-answer test and independently validate the returned assignment and objective.

The N=512 dense and N=1024 sparse backends are not interchangeable. The SDK does not identify the board or confirm the loaded bitstream. Do not run a backend against an unverified device/bitstream combination. Hardware execution has not been certified by CPU-only package tests.
