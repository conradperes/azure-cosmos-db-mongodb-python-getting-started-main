FUNCTION_APP_NAME=my-function-app-$(date +%s)
RESOURCE_GROUP=myResourceGroup3
STORAGE_ACCOUNT_NAME=mystorageaccountunique2
REGION=brazilsouth
AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query connectionString --output tsv)
AZURE_COSMOS_CONNECTION_STRING=$(az cosmosdb list-connection-strings --name conradcosmosdb --resource-group $RESOURCE_GROUP --query connectionStrings[0].connectionString --output tsv)
az functionapp create --resource-group $RESOURCE_GROUP --consumption-plan-location $REGION --runtime python --functions-version 4 --name $FUNCTION_APP_NAME --storage-account $STORAGE_ACCOUNT_NAME --os-type Linux
#mkdir Myfunction

cd ..
cd Myfunction
func new --name MyFunction --template "HTTP trigger" --authlevel “anonymous"
# Configure as variáveis de ambiente para a Function App
az functionapp config appsettings set --name $FUNCTION_APP_NAME --resource-group $RESOURCE_GROUP --settings AZURE_STORAGE_CONNECTION_STRING=$AZURE_STORAGE_CONNECTION_STRING AZURE_COSMOS_CONNECTION_STRING=$AZURE_COSMOS_CONNECTION_STRING
func start
func azure functionapp publish $FUNCTION_APP_NAME