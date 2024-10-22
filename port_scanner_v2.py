# Import necesary modules
from tqdm import tqdm
import asyncio
import aiodns
import socket
import sys


async def resolve_host(resolver, host):
    """
    Resolve the given host to its IP address using asynchronous DNS resolution.

    Args:
        resolver:       The DNS resolver instance.
        host:           The hostname to resolve.
    Returns:
        The resolved IP address or None if an error occurs.
    """
    try:
        # Check if the host is a valid IP address.
        socket.inet_aton(host)
        return host
    except socket.error:
        try:
            # Query for A record (IPv4 address).
            result = await resolver.query(host, "A")
            # Return the first resolved IP address.
            return result[0].host
        except Exception as e:
            print(f"Error resolving {host}\n{e}")
            return None


async def port_scanner(host, start_port, end_port):
    """
    Scan the specified range of ports on the given host to check for open ports.

    Args:
        host:           The hostname to scan.
        start_port:     The starting port number.
        end_port:       The ending port number.
    Returns:
        A list of open ports found on the host.
    """
    # Create a DNS resolver instance.
    resolver = aiodns.DNSResolver()
    # Resolve the host to an IP address.
    ip_address = await resolve_host(resolver, host)
    if ip_address is None:
        return
    
    open_ports = []
    tasks = []
    for port in range(start_port, end_port + 1):
        tasks.append(asyncio.create_task(check_port(ip_address, port)))
    
    done, pending = await asyncio.wait(tasks)
    for r in done:
        if r.result():      # If the result is not None, the port is open.
            open_ports.append(r.result())
    
    return open_ports


async def check_port(ip_address, port):
    """
    Check if a specific port is open on the given IP address.

    Args:
        ip_address:         The IP address to check.
        port:               The port number to check.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        await asyncio.get_event_loop().run_in_executor(None, s.connect, (ip_address, port))
        s.close()
        return port
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        s.close()
        return None


def save_to_file(filename, data):
    """
    Save the list of open ports to a specified file.

    Args:
        filename:       The name of the file to save the data to.
        data:           The list of open ports to save.
    """
    with open(filename, 'w') as f:
        for line in data:
            f.write(f"{line}\n")


if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python port_scanner_v2.py <host> <start_port> <end_port> [save_to_file]")
        sys.exit(1)
    
    host = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
    save_to_file_flag = False
    if len(sys.argv) == 5:
        if sys.argv[4] == "save_to_file":
            save_to_file_flag = True
    # Get the current event loop for asynchronous operations.
    loop = asyncio.get_event_loop()
    # Run the port scanner coroutine until it completes and get the list of open ports.
    open_ports = loop.run_until_complete(port_scanner(host, start_port, end_port))

    if open_ports:
        print(f"\nOpen ports on {host} in the range {start_port}-{end_port}:")

        if save_to_file_flag:
            # If the save_to_file flag is set, write the open ports to a file.
            with open("port_scan_report.txt", 'w') as f:
                for port in open_ports:
                    f.write(f"{port}\t\t----------\t\tOPEN\n")
        else:
            # If not saving to a file, print the open ports to the console with a progress bar.
            for port in tqdm(open_ports, leave=True):
                print(f"{port}\t\t----------\t\tOPEN")
    else:
        print(f"No open ports found on host {host}")
