"""
Test

Host:               iana.org
Ports found:        21, 80
Average runtime:    2 sec 87 ms
Conclusion:         Fast but not powerful enough (missed port 443 in the test)
"""

# Import necessary modules
import threading
import socket
import argparse


# Functions
def get_args():
    """
    Get command-line arguments.

    Returns:
        Parsed command-line arguments containing target IP and protocol.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="IP Address")
    parser.add_argument("-p", "--protocol", dest="protocol", choices=["tcp", "udp"], default="tcp", help="Protocol (TCP/UDP)")
    options = parser.parse_args()
    if not options.target:
        parser.error("IP address missing! Use '--help' for more details.")
    return options


# Single UDP Scanning
def tcp_scan(ip, port):
    """
    Scan single TCP port.
    
    Args:
        ip:     Target IP address/domain name.
        port:   Target port number.
    """
    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        response = s.connect_ex((ip, port))
        if response == 0:       # 0 -> Open , 1 -> Closed
            print(f"{port} ---------- OPEN")
    except Exception as e:
        print(f"Error occured while scanning port {port}\n{e}")
    finally:
        s.close()


# Single UDP Scanning
def udp_scan(ip, port):
    """
    Scan single UDP port.
    
    Args:
        ip:     Target IP address/domain name.
        port:   Target port number.
    """
    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    try:
        # Send an empty packet to the specified port on the IP address.
        # Then wait for a response.
        s.sendto(b"", (ip, port))
        s.recvfrom(1024)        # This will block if no response is recieved.
        print(f"{port} ---------- OPEN")
    except socket.error:
        # If we get a socket error, then the port is closed.
        pass
    except Exception as e:
        print(f"Error occured while scanning port {port}\n{e}")
    finally:
        s.close()


# Multi Scanning
def multi_scan(ip, start_port, end_port, protocol):
    """
    Scan multiple ports simultaneously.
    
    Args:
        ip:             Target IP address/domain name.
        start_port:     Scan starting from this port.
        end_port:       Scan ending at this port (included).
        protocol:       Scan protocol.
    """
    threads = []
    for port in range(start_port, end_port + 1):
        if protocol == "tcp":
            # Create a thread for TCP scanning.
            thread = threading.Thread(target=tcp_scan, args=(ip, port))
        elif protocol == "udp":
            # Create a thread for UDP scanning.
            thread = threading.Thread(target=udp_scan, args=(ip, port))
        threads.append(thread)
        thread.start()
    # Wait for all threads to finish.
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    options = get_args()
    target_ip = options.target
    protocol = options.protocol
    print("-" * 70)
    print(f"Target: {target_ip}\t\tPort Range: 1-65535\t\tProtocol: {protocol}")
    print("-" * 70)
    multi_scan(target_ip, 1, 65535, protocol)