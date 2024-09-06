This project provides a quick start guide for integrating a Python application with Azure Cosmos DB using the MongoDB API. It also demonstrates the creation and deployment of an Azure Function that interacts with Cosmos DB.

Summary

Environment Variable Management

This project uses environment variables to configure connections to Cosmos DB and the Storage Account. These variables can be configured both locally and in the Azure environment.

• Introduction
• Prerequisites
• Project Setup
• Local Execution
• Azure Deployment
• Environment Variable Management
• Additional Resources
• Contribution
• License

Introduction

This repository is a basic example to help you get started with developing Python applications that use Azure Cosmos DB with the MongoDB API. It includes an Azure Function that can be published to Azure and run in a consumption environment.

Prerequisites

Before you begin, make sure you have the following:

• Azure CLI installed and configured.
• Active Azure account.
• Python 3.11+ installed.
• Azure Functions Core Tools installed.
• Git installed.

Project Setup

1. Clone this repository:
Additional Resources

git clone https://github.com/conradperes/azure-cosmos-db-mongodb-python-getting-started-main.git
cd azure-cosmos-db-mongodb-python-getting-started-main

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate

Install Python dependencies:

'''
      sh setup-venv.sh

3.1 Run the setup file to install the Resource Group, Storage Account, Blob storage, upload the summary-2014.json to the blob storage, create the Cosmos DB account, create the database, and then create the collection:

'''
      sh setup.sh

Set the environment variables in .env:

'''
      FUNCTION_APP_NAME="my-function-app-172394009"
      RESOURCE_GROUP="myResourceGroup3"
      STORAGE_ACCOUNT_NAME="mystorageaccountunique2"
      REGION="brazilsouth"
      NAME_COSMOSDB_ACCOUNT="conradcosmosdb"    
      AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query connectionString --output tsv)
      AZURE_COSMOS_CONNECTION_STRING=$(az cosmosdb keys list --name $NAME_COSMOSDB_ACCOUNT --resource-group $RESOURCE_GROUP --type connection-strings --query "connectionStrings[0].connectionString" -o tsv)
      API_MANAGEMENT_NAME="apimanagementconrad"
      API_NAME="myfunctionap"
      FUNCTION_URL=https://$FUNCTION_APP_NAME.azurewebsites.net/api/myfunction
      API_PATH=/myfunction



• Azure Cosmos DB Documentation
• Azure Functions Documentation
• MongoDB API Example in Cosmos DB

Before running locally, please run the Shell script to create the function and deploy it to Azure Functions:

sh setup-functions.sh

This way, the Azure CLI will create the function, build it, and then deploy it. To test if everything is working correctly before spending unnecessary money on Azure, let's test it locally by following the steps below:

Local Execution

To run the project locally, follow the steps below:

Start the Azure Function locally:

func start

Test the function by accessing the locally generated endpoint.

Azure Deployment

Create a Function App resource in Azure:
This deployment is only necessary if everything works correctly locally. If so, execute a command similar to this:

all the steps are in the same shell script file:

'''
      sh setup-functions.sh



Publish the Azure Function: If you need to change the code and republish it.

func azure functionapp publish <Your-Function-App-Name>

Environment Variable Management

This project uses environment variables to configure connections to Cosmos DB and the Storage Account. These variables can be configured both locally and in the Azure environment.

Additional Resources

• Azure Cosmos DB Documentation
• Azure Functions Documentation
• MongoDB API Example in Cosmos DB

Contribution

Contributions are welcome! Feel free to open issues and pull requests.

License

This project is licensed under the MIT License. See the LICENSE file for more details.