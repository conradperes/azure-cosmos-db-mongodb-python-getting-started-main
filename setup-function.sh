export FUNCTION_APP_NAME=my-function-app-1723940095
export RESOURCE_GROUP=myResourceGroup3
export STORAGE_ACCOUNT_NAME=mystorageaccountunique2
export REGION=brazilsouth
export NAME_COSMOSDB_ACCOUNT=conradcosmosdb
export AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query connectionString --output tsv)
export AZURE_COSMOS_CONNECTION_STRING=$(az cosmosdb keys list --name $NAME_COSMOSDB_ACCOUNT --resource-group $RESOURCE_GROUP --type connection-strings --query "connectionStrings[0].connectionString" -o tsv)

az functionapp create --resource-group $RESOURCE_GROUP --consumption-plan-location $REGION --runtime python --functions-version 4 --name $FUNCTION_APP_NAME --storage-account $STORAGE_ACCOUNT_NAME --os-type Linux
#mkdir Myfunction
deactivate
python3.11 -m venv venv
source venv/bin/activate
Pip install -r requirements.txt
func new --name Myfunction --template "HTTP trigger" --authlevel "anonymous"
# Configure as variáveis de ambiente para a Function App
az functionapp config appsettings set --name my-function-app-1723940095 --resource-group $RESOURCE_GROUP --settings AZURE_STORAGE_CONNECTION_STRING=$AZURE_STORAGE_CONNECTION_STRING AZURE_COSMOS_CONNECTION_STRING=$AZURE_COSMOS_CONNECTION_STRING
#func start
func azure functionapp publish my-function-app-1723940095