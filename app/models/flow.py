from dataclasses import dataclass

@dataclass
class Flow:
    """Represents a simplified NetFlow record."""
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: int
    bytes: int
    packets: int
