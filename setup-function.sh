FUNCTION_APP_NAME=my-function-app-$(date +%s)
RESOURCE_GROUP=myResourceGroup3
STORAGE_ACCOUNT_NAME=mystorageaccountunique2
REGION=brazilsouth
az functionapp create --resource-group $RESOURCE_GROUP --consumption-plan-location $REGION --runtime python --functions-version 4 --name $FUNCTION_APP_NAME --storage-account $STORAGE_ACCOUNT_NAME --os-type Linux
#mkdir Myfunction
cd ..
cd Myfunction
func new --name MyFunction --template "HTTP trigger" --authlevel “anonymous"
func start
func azure functionapp publish $FUNCTION_APP_NAME