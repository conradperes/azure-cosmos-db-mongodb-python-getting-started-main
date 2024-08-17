az group create --name myResourceGroup3 --location brazilsouth
az storage account create --name mystorageaccountunique2 --resource-group myResourceGroup3 --location brazilsouth --sku Standard_LRS
az storage container create --account-name mystorageaccountunique2 --name conradcontainer
az storage blob upload --account-name mystorageaccountunique2 --container-name conradcontainer --name 2015-summary.json --file 2015-summary.json
az cosmosdb create --name conradcosmosdb --resource-group myResourceGroup3 --kind MongoDB --locations regionName=brazilsouth failoverPriority=0 isZoneRedundant=False
az cosmosdb mongodb database create \
--account-name conradcosmosdb \
--name mydatabase \
--resource-group myResourceGroup3
az cosmosdb mongodb collection create --account-name conradcosmosdb --database-name mydatabase --name mycollection --resource-group ResourceGroup3 --shard 'key' --throughput 400
