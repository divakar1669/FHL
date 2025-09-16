import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

TEAM_ID = os.getenv("TEAM_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

GRAPH_API_BASE = os.getenv("GRAPH_API_BASE", "https://graph.microsoft.com/v1.0")


# Load Azure OpenAI env variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")


KUSTO_CLUSTER_URI = os.getenv("KUSTO_CLUSTER_URI")

