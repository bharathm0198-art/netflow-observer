import socket
import json
import time
import random

# Configuration
COLLECTOR_IP = "127.0.0.1"
COLLECTOR_PORT = 2055

def generate_random_ip():
    """Generates a random IP address like 192.168.X.X"""
    return f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_flow():
    """Creates a dictionary representing a flow record."""
    return {
        "IPV4_SRC_ADDR": generate_random_ip(),
        "IPV4_DST_ADDR": generate_random_ip(),
        "L4_SRC_PORT": random.randint(1024, 65535),
        "L4_DST_PORT": 80 if random.random() > 0.5 else 443,  # Mostly HTTP/HTTPS
        "PROTOCOL": 6,  # TCP
        "IN_BYTES": random.randint(100, 10000),
        "IN_PKTS": random.randint(1, 50)
    }

def main():
    print(f"Starting Traffic Generator -> {COLLECTOR_IP}:{COLLECTOR_PORT}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while True:
            # 1. Generate a flow
            flow_data = generate_flow()
            
            # 2. Serialize to JSON (Simulating a packet payload)
            # In real NetFlow v9, this would be a binary template+data set.
            # For this test, we send JSON so our parser can easily read it.
            payload = json.dumps(flow_data).encode('utf-8')
            
            # 3. Send to Collector
            sock.sendto(payload, (COLLECTOR_IP, COLLECTOR_PORT))
            
            print(f"Sent flow: {flow_data['IPV4_SRC_ADDR']} -> {flow_data['IPV4_DST_ADDR']}")
            
            # Sleep a bit to simulate traffic arrival
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping generator.")

if __name__ == "__main__":
    main()
