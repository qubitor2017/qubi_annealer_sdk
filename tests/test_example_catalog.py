"""Smoke-test every runnable example on the CPU mock backend in-process."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import runpy
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples'

class ExampleCatalogSmokeTests(unittest.TestCase):
    def test_all_examples_run_locally(self):
        scripts = sorted(p for p in EXAMPLES.rglob('*.py') if p.name != '_common.py')
        self.assertGreaterEqual(len(scripts), 40)
        sys.path.insert(0, str(ROOT))
        sys.path.insert(0, str(EXAMPLES))
        failures = []
        original_argv = sys.argv[:]
        try:
            for script in scripts:
                sys.argv = [str(script)]
                output = StringIO()
                try:
                    with redirect_stdout(output):
                        runpy.run_path(str(script), run_name='__main__')
                except Exception as exc:
                    failures.append(f'{script.relative_to(ROOT)}: {exc}\n{output.getvalue()}')
        finally:
            sys.argv = original_argv
        self.assertFalse(failures, '\n\n'.join(failures))

if __name__ == '__main__':
    unittest.main()
