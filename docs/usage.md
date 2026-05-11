# QR Code Maker CLI

## What it does

This small command-line app converts text or a URL into a QR code image and saves it as a PNG file.

## Basic command

Run this from the repository root:

```bash
python -m src.qr_code_maker "https://example.com" "example.png"
```

## Optional size settings

You can change the QR box size and border:

```bash
python -m src.qr_code_maker "Hello world" "hello.png" --box-size 12 --border 5
```

## Notes

- The output file must end with `.png`.
- If you save into a subfolder, create that folder first.
- Use `python -m src.qr_code_maker --help` to see all options.
