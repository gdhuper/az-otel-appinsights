import logging, os, time
import azure.functions as func
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Declare OpenTelemetry as enabled tracing plugin for Azure SDKs
from azure.core.settings import settings
from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan

from azure.storage.queue import QueueClient

settings.tracing_implementation = OpenTelemetrySpan


exporter = AzureMonitorTraceExporter.from_connection_string(
    conn_str=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)


def get_queue_client(name):
    # Retrieve the connection string from an environment
    # variable named AZURE_STORAGE_CONNECTION_STRING
    connect_str = os.environ["AZURE_STORAGE_CONNECTION_STRING"]

    # Create a unique name for the queue
    q_name = "otel-queue"

    # Instantiate a QueueClient object which will
    # be used to create and manipulate the queue
    print("Creating queue: " + q_name)
    queue_client = QueueClient.from_connection_string(connect_str, q_name)
    return queue_client

def send_message(message, queue_client):
    print("Adding message to queue: " + message)
    res = queue_client.send_message(message)
    print("insertion id:" + res.id)

def peek_queue(queue_client):
    messages = queue_client.peek_messages()
    for peeked_message in messages:
        print("Peeked message: " + peeked_message.content)

def main(req: func.HttpRequest, que: func.Out[str]) -> func.HttpResponse:
    with tracer.start_as_current_span("OtelHttpfn"):
        #logging.info("Python HTTP trigger function processed a request.")
        print("Python HTTP trigger function received a request")

        queue_name = "otel-queue"
        with tracer.start_as_current_span("Creating queue client"):
            time.sleep(2)
            queue_client = get_queue_client(queue_name)

            name = req.params.get("name")
            if not name:
                try:
                    req_body = req.get_json()
                except ValueError:
                    pass
                else:
                    name = req_body.get("name")

            if name:
                message = name
                with tracer.start_as_current_span("Adding a message to the queue"):
                    print("Adding message: " + message)
                    time.sleep(1)
                    queue_client.send_message(message)
                    time.sleep(2)
                    with tracer.start_as_current_span("message added"):
                        time.sleep(1)
                        with tracer.start_as_current_span(
                            "returning response"
                        ):
                            return func.HttpResponse(
                                f"Hello, {name}. This HTTP triggered function executed successfully."
                            )
            else:
                with tracer.start_as_current_span("Get request responding..."):
                    print("This HTTP triggered function executed successfully.")
                # Peek at the first message
                return func.HttpResponse(
                    "This HTTP triggered function executed successfully.", status_code=200
                )
