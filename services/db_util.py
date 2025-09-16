import logging
import json
import io
import azure.functions as func

from azure.kusto.ingest import IngestionProperties, QueuedIngestClient 
from azure.kusto.data import KustoConnectionStringBuilder

from azure.kusto.data import DataFormat



def insertData(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing Kusto ingestion request.')

    try:
        # Your data
        data_to_ingest = [ {
            "id": "7e753f2c-e1c5-442d-a16f-132234",
            "TeamsLink": "https://teams.microsoft.com/l/message/1",
            "MessageId": "msg_101",
            "ChannelId": "channel_abc",
            "AdoWorkItemUrl": "https://dev.azure.com/org/proj/_workitems/edit/101",
            "ShortDescription": "Login page is down",
            "CreationTime": "2025-09-15T10:00:00.000Z",
            "Tags": "frontend",
            "GroupTag": "WebApp"
        }] 
        
        logging.info("starting data preparation for ingestion. Data: %s", data_to_ingest)


        json_data_list = data_to_ingest

        compressed_stream = io.StringIO('\n'.join(json.dumps(record) for record in json_data_list))
        logging.info("Data prepared for ingestion.")

        # Kusto configuration
        cluster_uri = "https://ingest-cri-db.centralindia.kusto.windows.net"
        database_name = "CRI_DB"
        table_name = "CRI_Data"
        client_id = "7674cdd0-a013-4768-8368-ad99caa5c4af"
        client_secret = "4T68Q~Uo3uOkvKn6moGfytqLkvltxzXaJMOcVb_k"
        tenant_id = "47cff186-6705-46a6-9834-685413ada769"

        # Authentication
        kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
            cluster_uri, client_id, client_secret, tenant_id
        )

        # Create ingestion client
        ingest_client = QueuedIngestClient(kcsb)

        logging.info("Ingestion client created.")

        # Ingestion properties
        ingestion_props = IngestionProperties(
            database=database_name,
            table=table_name,
            data_format=DataFormat.JSON,
        )

        logging.info(f"Ingestion properties set. {ingestion_props} Starting ingestion... {compressed_stream}")
        logging.info(f"Starting ingestion of compressed data...")


        # Ingest data
        ingest_client.ingest_from_stream(compressed_stream, ingestion_properties=ingestion_props)

        return func.HttpResponse(f"Data ingested successfully into {table_name}!", status_code=200)

    except Exception as e:
        logging.error(f"Ingestion failed: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)