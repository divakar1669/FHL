import azure.functions as func
import logging
import os
import logging
import json
import io
import azure.functions as func
import requests


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="cri_hack")
def cri_hack(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "~ Wishing you a great day ahead !!! ~ Divakar",
             status_code=200  
        )
    
@app.route(route="subscribe")
def subscribe(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    email = req.params.get('email')
    tags = req.params.get('tags') # this must be a comma-separated string of tags 
    if not email:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            email = req_body.get('email')

    if email:
        return func.HttpResponse(f"Subscription successful for {email}.")
    else:
        return func.HttpResponse(
            "Please provide a valid email address.",
            status_code=400
        )

# @app.route(route="test_diva")
# def appendData(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python timer trigger function started to ingest data via REST API.')

#     data_to_ingest = {
#         "id": "7e753f2c-e1c5-442d-a16f-1f061e89326f",
#         "TeamsLink": "https://teams.microsoft.com/l/message/1",
#         "MessageId": "msg_101",
#         "ChannelId": "channel_abc",
#         "AdoWorkItemUrl": "https://dev.azure.com/org/proj/_workitems/edit/101",
#         "ShortDescription": "Login page is down",
#         "CreationTime": "2025-09-15T10:00:00.000Z",
#         "Tags": "frontend",
#         "GroupTag": "WebApp"
#     }

#     # --- REST API Logic ---
#     try:
#         cluster_uri = os.environ["KUSTO_CLUSTER_URI"]
#         database_name = "CRI_DB"
#         table_name = "CRI_Data"

#         # 1. Get Authentication Token for Managed Identity
#         credential = DefaultAzureCredential()
#         # The scope must be the ADX cluster URI with a /.default suffix
#         scope = f"{cluster_uri}/.default"
#         token = credential.get_token(scope).token

#         # 2. Build the REST API URL and headers
#         # Note: The ingestion endpoint uses 'ingest-'
#         ingestion_uri = cluster_uri.replace("https://", "https://ingest-")
#         ingestion_url = f"{ingestion_uri}/v1/rest/ingest/{database_name}/{table_name}?format=json"

#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Content-Type": "application/json"
#         }

#         # 3. Send the POST request to the Ingestion API
#         response = requests.post(ingestion_url, headers=headers, json=data_to_ingest)

#         # Check the response for success
#         if response.status_code == 200:
#             logging.info("Data ingested successfully via REST API.")
#         else:
#             logging.error(f"Ingestion failed with status code {response.status_code}: {response.text}")

#     except Exception as e:
#         logging.error(f"Ingestion failed: {e}")