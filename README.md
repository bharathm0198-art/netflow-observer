# NetFlow Observer

A minimal, production-style NetFlow v9 collector and visualization pipeline.

## Purpose

This application listens for NetFlow v9 traffic (UDP port 2055), parses the packets to extract key metrics (Source/Dest IP, Ports, Protocol, Bytes, Packets), and stores them in a PostgreSQL database. It includes a pre-configured Grafana instance for visualizing network traffic in real-time.

**Key Features:**
- **Ingestion**: High-performance UDP listener.
- **Storage**: Structured PostgreSQL storage.
- **Visualization**: Grafana dashboards.
- **Testing**: Included traffic generator for development without a physical router.

## Architecture

1.  **Router / Generator** -> UDP 2055 -> **Collector (Python)**
2.  **Collector** -> Parse & Insert -> **PostgreSQL (Local)**
3.  **Grafana** -> Query -> **PostgreSQL**

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (only for running the traffic generator)

### 1. Start the Services

Start the collector and Grafana services:

```bash
docker compose up --build
```
- **Collector**: Listening on `0.0.0.0:2055` (UDP)
- **Grafana**: Available at `http://localhost:3000`

### 2. Generate Traffic (Optional)

If you don't have a real router sending NetFlow packets, use the included generator script to simulate traffic:

1.  Open a new terminal window.
2.  Run the generator:
    ```bash
    python traffic_generator.py
    ```
3.  You should see logs indicating flows are being sent. Note: This clears after restart, ensure the database is running first.

### 3. Visualize in Grafana

1.  **Login**: Go to [http://localhost:3000](http://localhost:3000).
    -   **User**: `admin`
    -   **Password**: `admin`

2.  **Add Data Source**:
    -   Navigate to **Connections** -> **Data Sources** -> **Add data source**.
    -   Select **PostgreSQL**.
    -   **Connection Settings**:
        -   **Host**: `host.docker.internal:5432` (Connects to your host's Postgres)
        -   **Database**: `postgres`
        -   **User**: `postgres`
        -   **Password**: `bharath@123`
        -   **TLS/SSL Method**: `Disable`
    -   Click **Save & test**.

3.  **Create a Dashboard**:
    -   Go to **Dashboards** -> **New dashboard**.
    -   Add a **Visualization**.
    -   Select the **PostgreSQL** data source (should be named "PostgreSQL" or "postgres").
    -   Use the following SQL query to see traffic over time:
        ```sql
        SELECT
          time_received as "time",
          bytes as "Bytes"
        FROM flows
        WHERE $__timeFilter(time_received)
        ORDER BY time_received ASC
        ```
    -   Click **Run query** and **Apply**.

## Database Schema

The data is stored in the `flows` table in the `public` schema:

| Column | Type | Description |
|--------|------|-------------|
| `time_received` | TIMESTAMPTZ | UTC Timestamp of ingestion |
| `src_ip` | INET | Source IP Address |
| `dst_ip` | INET | Destination IP Address |
| `src_port` | INT | Source Port |
| `dst_port` | INT | Destination Port |
| `protocol` | INT | IP Protocol (e.g., 6=TCP, 17=UDP) |
| `bytes` | BIGINT | Total bytes in flow |
| `packets` | BIGINT | Total packets in flow |
