source .env

az functionapp create --resource-group $RESOURCE_GROUP --consumption-plan-location $REGION --runtime python --functions-version 4 --name $FUNCTION_APP_NAME --storage-account $STORAGE_ACCOUNT_NAME --os-type Linux
#mkdir Myfunction

#func new --name Myfunction --template "HTTP trigger" --authlevel "anonymous"
# Configure as variáveis de ambiente para a Function App
az functionapp config appsettings set --name $FUNCTION_APP_NAME --resource-group $RESOURCE_GROUP --settings AZURE_STORAGE_CONNECTION_STRING=$AZURE_STORAGE_CONNECTION_STRING AZURE_COSMOS_CONNECTION_STRING=$AZURE_COSMOS_CONNECTION_STRING
#func start
func azure functionapp publish $FUNCTION_APP_NAME 

#Criacao do Api Management
az apim create --resource-group $RESOURCE_GROUP --name $API_MANAGEMENT_NAME --publisher-email "profconrad.peres@fiap.com.br" --publisher-name "Conrad Peres"

az apim api create --resource-group $RESOURCE_GROUP --service-name $API_MANAGEMENT_NAME \
  --api-id $API_NAME --display-name "My Function API" \
  --path "/myfunction" --service-url $FUNCTION_URL --protocols https


  az apim api operation create --resource-group $RESOURCE_GROUP --service-name $API_MANAGEMENT_NAME \
  --api-id $API_NAME --url-template "/" --method GET \
  --display-name "Get My Function" --response-status-code 200