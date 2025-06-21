import json
import logging
from datetime import datetime
from twisted.internet import protocol, reactor
from twisted.internet.protocol import DatagramProtocol

# Robust logging setup
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler('echoecho.log'),
            logging.StreamHandler()
        ]
    )
except Exception as e:
    print(f"[WARNING] Could not create log file: {e}\nLogging to console only.")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

class TCPEcho(protocol.Protocol):
    def connectionMade(self):
        try:
            peer = self.transport.getPeer()
            port = self.transport.getHost().port
            log_message = f"TCP Connection from {peer.host}:{peer.port} to port {port}"
            logging.info(log_message)
        except Exception as e:
            print(f"[ERROR] Exception in TCPEcho.connectionMade: {e}")

    def dataReceived(self, data):
        try:
            self.transport.write(data)
        except Exception as e:
            print(f"[ERROR] Exception in TCPEcho.dataReceived: {e}")

class UDPEcho(DatagramProtocol):
    def datagramReceived(self, data, addr):
        try:
            port = self.transport.getHost().port
            log_message = f"UDP Packet from {addr[0]}:{addr[1]} to port {port}"
            logging.info(log_message)
            self.transport.write(data, addr)
        except Exception as e:
            print(f"[ERROR] Exception in UDPEcho.datagramReceived: {e}")

def load_config(config_file='config.json'):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        if 'ports' not in config or not isinstance(config['ports'], list):
            print("[ERROR] 'ports' key missing or not a list in config.json. No servers will be started.")
            return None
        return config
    except FileNotFoundError:
        print(f"[WARNING] Config file {config_file} not found! No servers will be started.")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Error parsing config file {config_file}: {e}. No servers will be started.")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error loading config: {e}. No servers will be started.")
        return None

def start_servers():
    config = load_config()
    if not config:
        return

    for port_config in config['ports']:
        port = port_config.get('port')
        protocol_type = port_config.get('protocol', '').upper()
        if not isinstance(port, int) or protocol_type not in ('TCP', 'UDP'):
            print(f"[WARNING] Invalid port config: {port_config}. Skipping.")
            continue
        try:
            if protocol_type == 'TCP':
                factory = protocol.ServerFactory()
                factory.protocol = TCPEcho
                reactor.listenTCP(port, factory)
                print(f"Started TCP server on port {port}")
            elif protocol_type == 'UDP':
                reactor.listenUDP(port, UDPEcho())
                print(f"Started UDP server on port {port}")
        except Exception as e:
            error_msg = f"Failed to start {protocol_type} server on port {port}: {e}"
            print(error_msg)

if __name__ == '__main__':
    print("Starting Port Simulator...")
    start_servers()
    print("Servers started. Press Ctrl+C to stop.\n")
    reactor.run() 