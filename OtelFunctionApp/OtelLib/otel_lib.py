import os
from typing import Optional

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

OTEL_CLIENT = Optional[AzureMonitorTraceExporter]

def _init_client(environ_key: str) -> Optional[AzureMonitorTraceExporter]:
    key = os.environ[environ_key]
    if key is None:
        return None
    exporter = AzureMonitorTraceExporter.from_connection_string(
        connection_string = key
    )
    return exporter

def get_otel_client() -> Optional[AzureMonitorTraceExporter]:
    global OTEL_CLIENT
    if not OTEL_CLIENT:
        OTEL_CLIENT = _init_client("APPLICATIONINSIGHTS_CONNECTION_STRING")
    return OTEL_CLIENT