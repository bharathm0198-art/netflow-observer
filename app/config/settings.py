import os

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Mahesh@22")

# Collector Configuration
COLLECTOR_HOST = "0.0.0.0"
COLLECTOR_PORT = int(os.getenv("COLLECTOR_PORT", 2055))
