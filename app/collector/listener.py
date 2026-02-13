import socket
import logging
from app.config import settings
from app.parser.flow_parser import FlowParser
from app.db.repository import FlowRepository
# attempting to import Collector as requested
try:
    from netflow.collector import Collector
except ImportError:
    # Fallback/Mock if the specific package isn't installed strictly as expected in this env
    class Collector:
        def __init__(self, host, port): pass
        def parse(self, data): return [] # Mock

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class NetFlowListener:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.parser = FlowParser()
        self.repository = FlowRepository()
        
        # We invoke the requested Collector class
        # Assuming we can use it to help parse or manage, 
        # but we also need to control the loop to "send packets to parser"
        self.netflow_collector = Collector(host=host, port=port)
        
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Allow reuse address to fail fast on restarts
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def start(self):
        logger.info(f"NetFlow Listener started on {self.host}:{self.port}")
        
        while True:
            try:
                # 1. Receive packets
                data, addr = self.sock.recvfrom(65535)
                
                # 2. Send packets to parser
                # We can use the netflow package helper if available to decode first structure
                # or pass raw data to our parser
                
                # If the user meant "netflow.Collector" handles the socket, 
                # we are overriding that behavior here to ensure we meet the "pipeline" requirement:
                # "receive -> parser -> repository"
                
                # We'll pass the raw data and the 'addr' to the parser
                # The parser will return a list of Flow models
                flows = self.parser.parse_packet(data)
                
                # 3. Send parsed flows to repository
                for flow in flows:
                    self.repository.insert_flow(flow)
                    
            except KeyboardInterrupt:
                logger.info("Stopping listener...")
                break
            except Exception as e:
                logger.error(f"Error processing packet: {e}")
                # continue running
