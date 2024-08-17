import logging
from azure.storage.blob import BlobServiceClient
import pymongo
import json
import os
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="HttpTriggerFunction")
@app.route(route="httptrigger", methods=["GET", "POST"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Configurações do Blob Storage
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = 'conradcontainer'
    blob_name = '2015-summary.json'

    # Configurações do Cosmos DB
    CONNECTION_STRING = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
    logging.info(f"Azure Storage Connection String: {connection_string}")
    logging.info(f"Cosmos DB Connection String: {CONNECTION_STRING}")
    DB_NAME = "api-mongodb-sample-database"
    UNSHARDED_COLLECTION_NAME = "unsharded-sample-collection"
    SAMPLE_FIELD_NAME = "sample_field"

    # Função para ler o JSON de um arquivo
    def read_json_file(file_path):
        with open(file_path, 'r') as file:
            data = []
            for line in file:
                try:
                    data.append(json.loads(line.strip()))
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON on line: {line.strip()}")
                    raise e
        return data

    # Função para baixar o blob do Azure Blob Storage
    def download_blob_storage(blob_service_client, container_name, blob_name):
        try:
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            with open("/tmp/downloaded.json", "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            logging.info("Blob baixado com sucesso!")
            return read_json_file("/tmp/downloaded.json")
        except Exception as e:
            logging.error(f"Erro ao baixar o blob: {e}")
            return []

    # Função para criar o banco de dados e a coleção
    def create_database_unsharded_collection(client):
        db = client[DB_NAME]
        if DB_NAME not in client.list_database_names():
            db.command({'customAction': "CreateDatabase", 'offerThroughput': 400})
            logging.info("Created db {} with shared throughput".format(DB_NAME))

        if UNSHARDED_COLLECTION_NAME not in db.list_collection_names():
            db.command({'customAction': "CreateCollection", 'collection': UNSHARDED_COLLECTION_NAME})
            logging.info("Created collection {}".format(UNSHARDED_COLLECTION_NAME))
        return db[UNSHARDED_COLLECTION_NAME]

    import time

    def save_documents(collection, documents):
        for document in documents:
            retries = 5
            while retries > 0:
                try:
                    collection.insert_one(document)
                    logging.info("Inserted document: %s", document)
                    break
                except pymongo.errors.WriteError as e:
                    if e.code == 16500:  # TooManyRequests (429)
                        retries -= 1
                        wait_time = int(e.details.get("RetryAfterMs", 1000)) / 1000
                        logging.warning(f"TooManyRequests error, retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        logging.error(f"Failed to insert document: {document} with error: {e}")
                        raise e
            if retries == 0:
                logging.error(f"Failed to insert document after retries: {document}")
        logging.info("Saved {} documents to the collection".format(len(documents)))

    client = pymongo.MongoClient(CONNECTION_STRING)
    try:
        client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

    documents = download_blob_storage(blob_service_client, container_name, blob_name)
    collection = create_database_unsharded_collection(client)
    save_documents(collection, documents)
    
    return func.HttpResponse("Dados inseridos com sucesso no Cosmos DB", status_code=200)