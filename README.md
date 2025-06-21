# EchoEcho

**EchoEcho** is a lightweight port simulator for testing and monitoring TCP and UDP connections. It listens on user-defined ports, logs all incoming connections, and echoes received data. Useful for network troubleshooting, automated testing, or simulating service availability.

---

## Features

- ✅ Support for both **TCP** and **UDP**
- 🛠 Configuration via simple `config.json`
- 📜 Logs activity to console and a log file
- 🔁 Echoes back all incoming data
- 🪟 Optional Windows executable build via PyInstaller

---

## Requirements

- Python 3.8 or later
- Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Configuration

Define the ports and protocols to monitor by creating a `config.json` file. Use the example below:

```json
{
  "ports": [
    {
      "port": 80,
      "protocol": "TCP"
    },
    {
      "port": 3000,
      "protocol": "UDP"
    }
  ]
}
```

For convenience, see the included `config.json.example`.

---

## Usage

### Run in Development Mode

```bash
python echoecho.py
```

### Build Executable (Windows)

```bash
pyinstaller --onefile echoecho.py
```

The `.exe` file will be created in the `dist/` directory.

### Using the Executable

1. Place `echoecho.exe` and `config.json` in the same folder
2. Run `echoecho.exe`
3. Logs will be saved to `echoecho.log`

---

## Testing Tools

You can test open ports using:

- **PowerShell**
  ```bash
  Test-NetConnection -ComputerName localhost -Port 80
  ```

- **nmap**
  ```bash
  nmap -p 80,3000 localhost
  ```

- **telnet**
  ```bash
  telnet localhost 80
  ```

---

## Logging

Connection attempts are logged with timestamps to:

- Standard output (console)
- `echoecho.log` in the current directory

---

## Acknowledgments

- [Twisted](https://twistedmatrix.com/trac/) – Event-driven networking engine for Python
- [PyInstaller](https://www.pyinstaller.org/) – Bundle Python applications into standalone executables

---

## License

This project is licensed under the [MIT License](LICENSE).
