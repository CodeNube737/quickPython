from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from src.qr_code_maker import create_qr_code, main


class QrCodeMakerTests(unittest.TestCase):
    def test_create_qr_code_writes_png_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "sample.png"

            saved_path = create_qr_code("https://example.com", output_path)

            self.assertEqual(saved_path, output_path)
            self.assertTrue(output_path.exists())
            self.assertGreater(output_path.stat().st_size, 0)
            self.assertEqual(output_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_main_returns_success_for_valid_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "cli.png"
            stdout = io.StringIO()

            with redirect_stdout(stdout):
                exit_code = main(["hello world", str(output_path)])

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())
            self.assertIn("QR code saved to", stdout.getvalue())

    def test_main_returns_error_for_missing_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_path = Path(temp_dir) / "missing" / "qr.png"
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                exit_code = main(["hello world", str(missing_path)])

            self.assertEqual(exit_code, 1)
            self.assertIn("Output directory does not exist", stderr.getvalue())

    def test_main_rejects_blank_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "blank.png"
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                exit_code = main(["   ", str(output_path)])

            self.assertEqual(exit_code, 1)
            self.assertIn("Input text cannot be empty", stderr.getvalue())

    def test_missing_required_arguments_raise_system_exit(self) -> None:
        stderr = io.StringIO()

        with redirect_stderr(stderr), self.assertRaises(SystemExit) as context:
            main([])

        self.assertEqual(context.exception.code, 2)
        self.assertIn("usage:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
