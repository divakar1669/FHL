import logging
import azure.functions as func
from azure.kusto.data import KustoConnectionStringBuilder
from azure.kusto.ingest import QueuedIngestClient, IngestionProperties, DataFormat
import io
import json


def ingest_data_to_kusto():
    logging.info('Processing Kusto ingestion request.')

    try:
        # Your data
        data_to_ingest = {
            "id": "7e753f2c-e1c5-442d-a16f-1f061e89326f",
            "TeamsLink": "https://teams.microsoft.com/l/message/1",
            "MessageId": "msg_101",
            "ChannelId": "channel_abc",
            "AdoWorkItemUrl": "https://dev.azure.com/org/proj/_workitems/edit/101",
            "ShortDescription": "Login page is down",
            "CreationTime": "2025-09-15T10:00:00.000Z",
            "Tags": "frontend",
            "GroupTag": "WebApp"
        }

        # Convert to JSON bytes stream
        json_str = json.dumps([data_to_ingest])  # wrap in list for JSON ingestion
        json_bytes = io.BytesIO(json_str.encode('utf-8'))

        # Kusto configuration
        cluster_uri = "https://cri-db.centralindia.kusto.windows.net"
        database_name = "CRI_DB"
        table_name = "CRI_Data"
        client_id = "<client_id>"
        client_secret = "<client_secret>"
        tenant_id = "<tenant_id>"

        # Authentication
        kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
            cluster_uri, client_id, client_secret, tenant_id
        )

        # Create ingestion client
        ingest_client = QueuedIngestClient(kcsb)

        # Ingestion properties
        ingestion_props = IngestionProperties(
            database=database_name,
            table=table_name,
            data_format=DataFormat.JSON
        )

        # Ingest data
        ingest_client.ingest_from_stream(json_bytes, ingestion_properties=ingestion_props)

        return func.HttpResponse(f"Data ingested successfully into {table_name}!", status_code=200)

    except Exception as e:
        logging.error(f"Ingestion failed: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)