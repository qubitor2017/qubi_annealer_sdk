"""UART adapters for the Qubitor FPGA protocol family.

N=1024 protocol is based on the supplied N=1024 PORT_PROTOCOL.md.
N=512 protocol is aligned to the supplied N_512/rtl/qubi_f2026_uart.sv:
uint16 little-endian row/column, int32 little-endian payload, stored as signed
int16 in BRAM. Hardware testing is still required to validate the programmed bitstream.
"""
from __future__ import annotations
import struct, time
from .base import Backend
from ..result import SolveResult

class SerialProtocolError(RuntimeError): pass

class SerialFPGA:
    def __init__(self, port, baudrate=115200, timeout=3.0, serial_obj=None):
        if serial_obj is None:
            try: import serial
            except ImportError as exc: raise ImportError('Install pyserial: pip install qubitor-sdk[serial]') from exc
            serial_obj = serial.Serial(port, baudrate=baudrate, timeout=timeout, write_timeout=timeout)
            time.sleep(0.15)
            serial_obj.reset_input_buffer(); serial_obj.reset_output_buffer()
        self.ser = serial_obj

    def _write(self, data):
        self.ser.write(data); self.ser.flush()

    def _read_exact(self, n):
        data = self.ser.read(n)
        if len(data) != n: raise SerialProtocolError(f'UART timeout: expected {n} bytes, received {len(data)}.')
        return data

    def _ack(self):
        b = self._read_exact(1)
        if b != b'\x2a': raise SerialProtocolError(f'Unexpected ACK byte: {b.hex()}')

    def diagnostic(self):
        self._write(b'D')
        reply = self._read_exact(5)
        if reply != bytes.fromhex('d012345678'):
            raise SerialProtocolError(f'UART diagnostic mismatch: {reply.hex()}')
        return True

    def clear(self):
        self._write(b'R'); self._ack()

    def read_q(self, i, j):
        """Read one N=512 coefficient through the N=512 M diagnostic command."""
        if not (0 <= int(i) < 512 and 0 <= int(j) < 512):
            raise ValueError("N=512 read indices must be in 0..511")
        self._write(b'M' + struct.pack('<HH', int(i), int(j)))
        p = self._read_exact(5)
        if p[0] != 0xA7:
            raise SerialProtocolError(f'Unexpected memory-read packet: {p.hex()}')
        return struct.unpack('<i', p[1:5])[0]

    def set_cooling(self, value):
        self._write(b'T' + struct.pack('<I', int(value))); self._ack()

    def set_seed(self, value):
        self._write(b'V' + struct.pack('<I', int(value) & 0xffffffff)); self._ack()

    def start(self):
        self._write(b'S'); self._ack()

    def status(self):
        self._write(b'P')
        p = self._read_exact(16)
        if p[0] != 0xA5: raise SerialProtocolError(f'Unexpected status packet: {p.hex()}')
        return {'busy':bool(p[1]), 'done':bool(p[2]), 'objective':struct.unpack('<q',p[3:11])[0],
                'temperature':p[11], 'iterations':struct.unpack('<I',p[12:16])[0]}

    def result(self, n):
        self._write(b'G')
        packed_len = (n + 7) // 8
        p = self._read_exact(1 + 8 + packed_len + 1 + 4)
        if p[0] != 0xA6: raise SerialProtocolError(f'Unexpected result packet header: {p[0]:02x}')
        objective = struct.unpack('<q',p[1:9])[0]
        packed = p[9:9+packed_len]
        sol = [(packed[i // 8] >> (i % 8)) & 1 for i in range(n)]
        temp_off = 9+packed_len
        temp = p[temp_off]
        iterations = struct.unpack('<I',p[temp_off+1:temp_off+5])[0]
        return objective, sol, temp, iterations

class Dense512Backend(Backend):
    """Dense N=512 adapter aligned to the supplied N=512 UART RTL.

    Q payload: row uint16 LE, column uint16 LE, signed int32 LE.
    RTL stores coefficients in signed 16-bit BRAM, so scaled coefficients
    outside [-32768, 32767] are rejected before any Q writes are sent.
    """
    name = 'fpga_n512_dense'
    max_variables = 512
    supports_sparse = False

    def __init__(self, port=None, serial_obj=None, scale=1.0, timeout=3.0, cooling=1, seed=0xACE12026):
        self.link = SerialFPGA(port, timeout=timeout, serial_obj=serial_obj)
        self.scale, self.cooling, self.seed = float(scale), int(cooling), int(seed)

    def solve(self, model, **kwargs):
        model.validate(max_variables=self.max_variables, require_symmetric=True)
        # Preflight every coefficient before clearing or modifying FPGA memory.
        entries = []
        for (i, j), value in sorted(model.Q.items()):
            qv = _to_i32(value, self.scale)
            if not -32768 <= qv <= 32767:
                raise OverflowError(
                    f'N=512 BRAM stores signed int16 coefficients; Q[{i},{j}]={qv} '
                    'is outside [-32768, 32767]. Reduce scale or rescale the model.'
                )
            entries.append((i, j, qv))
        self.link.diagnostic(); self.link.clear()
        for i, j, qv in entries:
            self.link._write(b'Q' + struct.pack('<HHi', i, j, qv)); self.link._ack()
        self.link.set_cooling(kwargs.get('cooling', self.cooling))
        self.link.set_seed(kwargs.get('seed', self.seed))
        self.link.start()
        _wait_done(self.link, kwargs.get('max_wait', 120.0))
        obj, sol, temp, iters = self.link.result(self.max_variables)
        sol = sol[:model.n]
        return SolveResult(sol, model.energy(sol), 'completed', self.name, obj, temp, iters,
                           {'scale':self.scale, 'protocol':'n512-u16-u16-i32le-stored-int16',
                            'coefficient_storage_bits':16})

class Sparse1024Backend(Backend):
    name = 'fpga_n1024_sparse'
    max_variables = 1024
    supports_sparse = True
    max_directed_entries = 65535

    def __init__(self, port=None, serial_obj=None, scale=1.0, timeout=3.0, cooling=1, seed=0xACE12026):
        self.link = SerialFPGA(port, timeout=timeout, serial_obj=serial_obj)
        self.scale, self.cooling, self.seed = float(scale), int(cooling), int(seed)

    def solve(self, model, **kwargs):
        model.validate(max_variables=self.max_variables, require_symmetric=True)
        entries = [(i,j,v) for (i,j),v in model.Q.items() if v != 0]
        if len(entries) > self.max_directed_entries:
            raise ValueError(f'{len(entries)} directed entries exceed N=1024 capacity {self.max_directed_entries}.')
        self.link.diagnostic(); self.link.clear()
        # Q commands are row-major; row pointers are uploaded after coefficients.
        entries.sort(key=lambda e:(e[0],e[1]))
        row_counts = [0] * model.n
        for i,j,v in entries:
            qv = _to_i32(v, self.scale)
            self.link._write(b'Q' + struct.pack('<HHI', i, j, qv & 0xffffffff)); self.link._ack()
            row_counts[i] += 1
        ptr = 0
        for row in range(1025):
            self.link._write(b'H' + struct.pack('<HH', row, ptr)); self.link._ack()
            if row < model.n: ptr += row_counts[row]
        self.link.set_cooling(kwargs.get('cooling', self.cooling))
        self.link.set_seed(kwargs.get('seed', self.seed))
        self.link.start()
        _wait_done(self.link, kwargs.get('max_wait', 120.0))
        obj, sol, temp, iters = self.link.result(1024)
        sol = sol[:model.n]
        return SolveResult(sol, model.energy(sol), 'completed', self.name, obj, temp, iters,
                           {'scale':self.scale, 'nnz_directed':len(entries), 'protocol':'n1024-sparse'})

def _to_i32(value, scale):
    v = int(round(float(value)*scale))
    if not -(2**31) <= v < 2**31: raise OverflowError(f'Coefficient {value} * scale {scale} exceeds signed int32.')
    return v

def _wait_done(link, max_wait):
    deadline = time.monotonic() + float(max_wait)
    while time.monotonic() < deadline:
        s = link.status()
        if s['done'] and not s['busy']: return s
        time.sleep(0.05)
    raise TimeoutError(f'FPGA did not finish within {max_wait} seconds.')
