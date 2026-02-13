import datetime
from app.db.connection import get_db_connection
from app.models.flow import Flow

class FlowRepository:
    def __init__(self):
        self.conn = get_db_connection()
        self.create_table()

    def create_table(self):
        """Creates the flows table if it doesn't exist."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS flows (
                        time_received TIMESTAMPTZ,
                        src_ip INET,
                        dst_ip INET,
                        src_port INT,
                        dst_port INT,
                        protocol INT,
                        bytes BIGINT,
                        packets BIGINT
                    );
                """)
            self.conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")
            self.conn.rollback()

    def insert_flow(self, flow: Flow):
        """Inserts a single flow record into the database."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO flows (
                        time_received, src_ip, dst_ip, src_port, dst_port, protocol, bytes, packets
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        datetime.datetime.now(datetime.timezone.utc),
                        flow.src_ip,
                        flow.dst_ip,
                        flow.src_port,
                        flow.dst_port,
                        flow.protocol,
                        flow.bytes,
                        flow.packets
                    )
                )
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting flow: {e}")
            self.conn.rollback()
            # Simple reconnection logic could go here if connection is lost
