CREATE TABLE IF NOT EXISTS flows (
    time_received TIMESTAMP,
    src_ip INET,
    dst_ip INET,
    src_port INT,
    dst_port INT,
    protocol INT,
    bytes BIGINT,
    packets BIGINT
);
