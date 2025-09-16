import os
import logging
import json
import io
import azure.functions as func

from azure.kusto.ingest import KustoIngestClient, IngestionProperties, DataFormat
from azure.kusto.data import KustoConnectionStringBuilder

def appendData(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get the JSON data from the HTTP request body
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
             "Please pass a JSON object in the request body",
             status_code=400
        )

    # --- Kusto Ingestion Logic ---
    try:
        # The ADX cluster URI is retrieved from app settings
        cluster_uri = os.environ["KUSTO_CLUSTER_URI"]
        table_name = "CRI_DB"
        database_name = "CRI_DB"

        # Use the default Azure credential for Managed Identity
        connection_string = KustoConnectionStringBuilder.with_az_cli_authentication(cluster_uri)
        ingest_client = KustoIngestClient(connection_string)

        # Ingestion properties for a single JSON object
        ingestion_properties = IngestionProperties(
            database=database_name,
            table=table_name,
            data_format=DataFormat.MULTIJSON,
            ignore_first_record=False
        )

        # Convert the single JSON object to a stream
        json_stream = io.StringIO(json.dumps(req_body))

        # Execute the ingestion
        ingest_client.ingest_from_stream(json_stream, ingestion_properties=ingestion_properties)
        
        logging.info("Successfully ingested data into ADX.")
        return func.HttpResponse(
            "Data ingested successfully!",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Ingestion failed: {e}")
        return func.HttpResponse(
            f"Ingestion failed: {e}",
            status_code=500
        )