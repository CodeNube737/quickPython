# QR Code Maker CLI

This repository now includes a small Python command-line tool that turns text or a URL into a QR code PNG file.

## Project structure

- `src/` - application code
- `docs/` - brief project documentation
- `tests/` - automated tests
- `requirements.txt` - Python dependencies

## 1) Create a `.venv`

From the repository root:

```bash
python -m venv .venv
```

If your system uses `python3` instead of `python`, use:

```bash
python3 -m venv .venv
```

## 2) Activate the `.venv`

### macOS / Linux (bash, zsh)

```bash
source .venv/bin/activate
```

### fish

```fish
source .venv/bin/activate.fish
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```bat
.venv\Scripts\activate.bat
```

## 3) Install dependencies from `requirements.txt`

From the repository root:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4) Run the program from the repository root

The command format is:

```bash
python -m src.qr_code_maker "your text or URL" "output.png"
```

Example:

```bash
python -m src.qr_code_maker "https://example.com" "example-qr.png"
```

You can also change the QR size settings:

```bash
python -m src.qr_code_maker "Hello from quickPython" "hello.png" --box-size 12 --border 5
```

If you want to save into a folder, create that folder first. Example:

```bash
mkdir -p output
python -m src.qr_code_maker "https://example.com" "output/example.png"
```

PowerShell version:

```powershell
New-Item -ItemType Directory -Force output
python -m src.qr_code_maker "https://example.com" "output/example.png"
```

## 5) Run tests from the repository root

```bash
python -m unittest discover -s tests -v
```

## CLI help

You can see the built-in help with:

```bash
python -m src.qr_code_maker --help
```
