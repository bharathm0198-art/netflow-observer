import logging
from app.models.flow import Flow

logger = logging.getLogger(__name__)

class FlowParser:
    """
    Parses incoming NetFlow records into Flow models.
    """
    
    def parse_packet(self, packet_data) -> list[Flow]:
        """
        Transforms raw export packet data into a list of Flow objects.
        """
        flows = []

        # 1. Handle raw bytes (if passed directly from socket)
        if isinstance(packet_data, bytes):
            logger.debug("Received bytes, attempting to parse...")
            try:
                import json
                # Try to parse as JSON (Test Mode)
                # This allows us to use traffic_generator.py for verification
                data = json.loads(packet_data.decode('utf-8'))
                
                # If valid JSON, treat it as a single record mock
                if isinstance(data, dict):
                    # Wrap in list to reuse loop below
                    raw_flows = [data]
                    # continue to processing loop at step 2...
                    
            except Exception:
                # Not JSON, invalid or real binary that we can't parse yet
                logger.warning("Received invalid binary data (not JSON test data).")
                return []
        else:
            # 2. Handle parsed objects (list of flows or export packet object)
            raw_flows = getattr(packet_data, 'flows', []) if hasattr(packet_data, 'flows') else packet_data
            
        # Ensure raw_flows is iterable
        if not isinstance(raw_flows, list):
             raw_flows = [raw_flows] if raw_flows else []

        for record in raw_flows:
            try:
                # Attempt to extract fields. Mapping common V9 fields.
                # Support both dict-like and object-like access.
                def get_val(obj, key, default=None):
                    if isinstance(obj, dict):
                        return obj.get(key, default)
                    return getattr(obj, key, default)

                # RFC 3954 standard field types or common names
                # We try string keys first, then integers.
                
                src_ip = get_val(record, 'IPV4_SRC_ADDR') or get_val(record, 8) or '0.0.0.0'
                dst_ip = get_val(record, 'IPV4_DST_ADDR') or get_val(record, 12) or '0.0.0.0'
                src_port = get_val(record, 'L4_SRC_PORT') or get_val(record, 7) or 0
                dst_port = get_val(record, 'L4_DST_PORT') or get_val(record, 11) or 0
                protocol = get_val(record, 'PROTOCOL') or get_val(record, 4) or 0
                bytes_count = get_val(record, 'IN_BYTES') or get_val(record, 1) or 0
                packets_count = get_val(record, 'IN_PKTS') or get_val(record, 2) or 0
                
                # Create Flow object
                flow = Flow(
                    src_ip=str(src_ip),
                    dst_ip=str(dst_ip),
                    src_port=int(src_port),
                    dst_port=int(dst_port),
                    protocol=int(protocol),
                    bytes=int(bytes_count),
                    packets=int(packets_count)
                )
                flows.append(flow)
            
            except Exception as e:
                logger.error(f"Error parsing flow record: {e}")
                continue

        return flows
