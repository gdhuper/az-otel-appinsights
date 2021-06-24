import os

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

exporter = AzureMonitorTraceExporter.from_connection_string(
    connection_string = os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)