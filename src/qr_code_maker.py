from __future__ import annotations

import argparse
from pathlib import Path

import qrcode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a QR code PNG file from text or a URL."
    )
    parser.add_argument("content", help="Text or URL to encode in the QR code.")
    parser.add_argument("output", help="PNG file path to save the QR code image.")
    parser.add_argument(
        "--box-size",
        type=int,
        default=10,
        help="Pixel size of each QR box (default: 10).",
    )
    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="Border width in boxes (default: 4).",
    )
    return parser


def validate_output_path(output_path: Path) -> None:
    if output_path.exists() and output_path.is_dir():
        raise ValueError("Output path points to a directory, not a file.")

    if output_path.suffix.lower() != ".png":
        raise ValueError("Output file must use the .png extension.")

    if not output_path.parent.exists():
        raise ValueError(
            f"Output directory does not exist: {output_path.parent}"
        )


def create_qr_code(
    content: str, output_path: Path | str, box_size: int = 10, border: int = 4
) -> Path:
    cleaned_content = content.strip()
    if not cleaned_content:
        raise ValueError("Input text cannot be empty.")

    if box_size <= 0:
        raise ValueError("Box size must be greater than 0.")

    if border < 0:
        raise ValueError("Border must be 0 or greater.")

    destination = Path(output_path)
    validate_output_path(destination)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(cleaned_content)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    image.save(destination, format="PNG")
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        saved_path = create_qr_code(
            content=args.content,
            output_path=args.output,
            box_size=args.box_size,
            border=args.border,
        )
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=__import__("sys").stderr)
        return 1

    print(f"QR code saved to {saved_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
