# 🔍 netscan - Modern Network Scanner

A fast, beautiful network discovery tool for identifying SSH, SNMP, and MySQL services.
Built with modern Python (3.12+) and designed for the 2026 era.

```bash
# Quick scan
netscan scan 192.168.1.0/24

# Save results
netscan scan 10.0.0.0/24 -o report.json

# Scan single host
netscan scan 192.168.1.1 --verbose
```

## ✨ Features

- **🚀 Fast** - Async concurrent scanning with semaphore-based rate limiting
- **🎨 Beautiful** - Rich terminal output with progress bars and colorful tables
- **📦 Simple** - Single file, minimal dependencies, zero configuration
- **🔧 Modern** - Python 3.12+, type hints, match/case statements
- **📊 Flexible Output** - JSON, CSV, or terminal table

## 🚀 Installation

### Using uv (recommended)
```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install netscan
uv tool install .

# Or run directly
uv run netscan scan 192.168.1.0/24
```

### Using pip
```bash
pip install -e .
```

### Requirements
- Python 3.12 or later
- nmap (must be installed on system)

```bash
# Install nmap
# macOS
brew install nmap

# Ubuntu/Debian
sudo apt install nmap

# Fedora/RHEL
sudo dnf install nmap
```

## 📖 Usage

### Basic Scan
```bash
# Scan network
netscan scan 192.168.1.0/24

# Scan single host
netscan scan 192.168.1.1
```

### Output Options
```bash
# Save as JSON
netscan scan 192.168.1.0/24 -o results.json

# Save as CSV
netscan scan 192.168.1.0/24 -o results.csv

# Specify format explicitly
netscan scan 192.168.1.0/24 -o output.txt --format json
```

### Advanced Options
```bash
# Verbose logging
netscan scan 192.168.1.0/24 --verbose

# Quiet mode (no table, only file output)
netscan scan 192.168.1.0/24 -o results.json --quiet

# Show version
netscan version
```

## 🎨 Example Output

```
🔍 Network Scan Results (5 alive hosts)
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ IP Address    ┃ Hostname     ┃  SSH  ┃ SNMP  ┃ MySQL  ┃ Status ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ 192.168.1.1   │ router.local │   ✅   │   ❌   │   ❌    │   UP   │
│ 192.168.1.10  │ server.local │   ✅   │   ✅   │   ✅    │   UP   │
│ 192.168.1.20  │ nas.local    │   ✅   │   ✅   │   ❌    │   UP   │
│ 192.168.1.50  │ -            │   ❌   │   ❌   │   ❌    │   UP   │
│ 192.168.1.100 │ printer      │   ❌   │   ✅   │   ❌    │   UP   │
└───────────────┴──────────────┴───────┴───────┴────────┴────────┘

Summary:
  • SSH servers: 3
  • SNMP devices: 3
  • MySQL servers: 1
```

## 🏗️ Architecture

### Why the Rewrite?

The original version was over-engineered with:
- 3,500 lines across 20 files
- 6 architectural layers (DDD/Clean Architecture)
- 13 dependencies for a simple port scanner
- Abstract interfaces with only 1 implementation
- Missing core functionality (scanner methods not implemented!)

### Modern Version

- **400 lines** in a single file
- **3 dependencies** (nmap, rich, typer)
- **Actually works** (implements all scanner methods!)
- Clean, maintainable, modern Python

```
netscan.py           # Everything in one beautiful file
pyproject.toml       # Modern dependency management
README.md            # You are here
```

## 🔬 How It Works

1. **Parse Network** - Convert CIDR or single IP to list of IPs
2. **Concurrent Scan** - Scan up to 50 hosts simultaneously
3. **Service Detection** - Check ports 22 (SSH), 161 (SNMP), 3306 (MySQL)
4. **Beautiful Output** - Display results in rich terminal table
5. **Export** - Optionally save to JSON or CSV

## 🛠️ Development

### Setup
```bash
# Clone and install
git clone https://github.com/thomasvincent/python-network-discovery-tool
cd python-network-discovery-tool

# Install with dev dependencies using uv
uv sync --dev

# Or with pip
pip install -e ".[dev]"
```

### Linting & Formatting
```bash
# Ruff does it all (replaces black, isort, flake8, pylint)
ruff check .           # Lint
ruff check --fix .     # Auto-fix
ruff format .          # Format
```

### Testing
```bash
# Run tests
pytest

# With coverage
pytest --cov=. --cov-report=html
```

## 📝 What Changed from v1.x?

| Feature | v1.x (Old) | v2.0 (New) |
|---------|-----------|-----------|
| **Lines of Code** | 3,500 | 400 |
| **Files** | 20 | 1 |
| **Dependencies** | 13 | 3 |
| **Architecture** | 6-layer DDD | Flat |
| **Scanner** | ❌ Broken | ✅ Works |
| **Terminal UI** | Basic | Rich/Beautiful |
| **Python** | 3.10+ | 3.12+ |
| **Linting** | black+isort+flake8 | ruff |
| **Package Manager** | pip/setuptools | uv/hatch |

## 🤝 Contributing

Contributions welcome! This is a learning project demonstrating modern Python practices.

## 📜 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Credits

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Uses [python-nmap](https://github.com/savon-noir/python-nmap) for network scanning
- CLI powered by [Typer](https://github.com/tiangolo/typer)
- Rewritten in 2026 with ❤️ and Claude Code

## 🔗 Links

- [GitHub Repository](https://github.com/thomasvincent/python-network-discovery-tool)
- [Issue Tracker](https://github.com/thomasvincent/python-network-discovery-tool/issues)
- [Original Version (Deprecated)](https://github.com/thomasvincent/python-network-discovery-tool/tree/v1.x)
