from azure.storage.blob import BlobServiceClient
import pandas as pd
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import pymongo
from random import randint
import json
import os

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
# Configurações do Blob Storage

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = 'conradcontainer'
blob_name = '2015-summary.json'

# Configurações do Cosmos DB
CONNECTION_STRING = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
DB_NAME = "api-mongodb-sample-database"
UNSHARDED_COLLECTION_NAME = "unsharded-sample-collection"
SAMPLE_FIELD_NAME = "sample_field"

# Função para ler o JSON de um arquivo
def read_json_file(file_path):
    """Read a JSON file and return its contents as a list of dictionaries"""
    with open(file_path, 'r') as file:
        data = []
        for line in file:
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line.strip()}")
                raise e
    return data

# Função para baixar o blob do Azure Blob Storage
def download_blob_storage(blob_service_client, container_name, blob_name):
    """Download the JSON file from Blob Storage and return its content as an array"""
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open("downloaded.json", "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        print("Blob baixado com sucesso!")
        # Read the downloaded JSON file and return its content as an array
        return read_json_file("downloaded.json")
    except Exception as e:
        print(f"Erro ao baixar o blob: {e}")
        return []

# Função para criar o banco de dados e a coleção
def create_database_unsharded_collection(client):
    """Create sample database with shared throughput if it doesn't exist and an unsharded collection"""
    db = client[DB_NAME]

    # Create database if it doesn't exist
    if DB_NAME not in client.list_database_names():
        # Database with 400 RU throughput that can be shared across the DB's collections
        db.command({'customAction': "CreateDatabase", 'offerThroughput': 400})
        print("Created db {} with shared throughput".format(DB_NAME))
    
    # Create collection if it doesn't exist
    if UNSHARDED_COLLECTION_NAME not in db.list_collection_names():
        # Creates an unsharded collection that uses the DB's shared throughput
        db.command({'customAction': "CreateCollection", 'collection': UNSHARDED_COLLECTION_NAME})
        print("Created collection {}".format(UNSHARDED_COLLECTION_NAME))
    
    return db[UNSHARDED_COLLECTION_NAME]

# Função para salvar documentos na coleção
def save_documents(collection, documents):
    """Save a list of documents to the collection"""
    for document in documents:
        collection.insert_one(document)
        print("Inserted document:", document)
    print("Saved {} documents to the collection".format(len(documents)))

# Conectar ao Cosmos DB
client = pymongo.MongoClient(CONNECTION_STRING)
try:
    client.server_info()  # validate connection string
except pymongo.errors.ServerSelectionTimeoutError:
    raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

# Baixar o arquivo JSON do Blob Storage
documents = download_blob_storage(blob_service_client, container_name, blob_name)
print(documents)

# Criar a coleção no Cosmos DB
collection = create_database_unsharded_collection(client)
    
# Salvar os documentos na coleção
save_documents(collection, documents)

print("Dados inseridos com sucesso no Cosmos DB")