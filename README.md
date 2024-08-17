Este projeto fornece um guia de início rápido para a integração de um aplicativo Python com o Azure Cosmos DB usando a API MongoDB. Ele também demonstra a criação e publicação de uma Azure Function que interage com o Cosmos DB.

Sumário

Gerenciamento de Variáveis de Ambiente

Este projeto utiliza variáveis de ambiente para configurar as conexões com o Cosmos DB e o Storage Account. Essas variáveis podem ser configuradas tanto localmente quanto no ambiente do Azure.

•	  Introdução
•	  Pré-requisitos
•	  Configuração do Projeto
•	  Execução Local
•	  Publicação no Azure
•	  Gerenciamento de Variáveis de Ambiente
•	  Recursos Adicionais
•	  Contribuição
•	  Licença
Introdução

Este repositório é um exemplo básico para ajudar você a começar a desenvolver aplicativos Python que utilizam o Azure Cosmos DB com a API MongoDB. Ele inclui uma Azure Function que pode ser publicada no Azure e executada em um ambiente de consumo.

Pré-requisitos

Antes de começar, certifique-se de ter o seguinte:

•	Azure CLI instalado e configurado.
•	Conta Azure ativa.
•	Python 3.11+ instalado.
•	Azure Functions Core Tools instaladas.
•	Git instalado.
Configuração do Projeto

1.	Clone este repositório:
Recursos Adicionais

git clone https://github.com/conradperes/azure-cosmos-db-mongodb-python-getting-started-main.git
cd azure-cosmos-db-mongodb-python-getting-started-main
Crie e ative um ambiente virtual:

python3 -m venv venv source venv/bin/activate # No Windows use venv\Scripts\activate

Instale as dependências do Python:

pip install -r requirements.txt

3.1 Rode o arquivo de setup para instalara o Resource Group, Storage Account, BLob storage e para subir o summary-2014.json para o blob storage e depois criar a conta de banco cosmos db e criar o banco e depois a collection:

sh setup.sh
Defina as variáveis de ambiente:

export AZURE_COSMOS_CONNECTION_STRING="sua-string-de-conexao-do-cosmos-db"
export AZURE_STORAGE_CONNECTION_STRING="sua-string-de-conexao-do-storage-account"
• Documentação do Azure Cosmos DB • Documentação do Azure Functions • Exemplo de API MongoDB no Cosmos DB

Antes de fazer a execuçao local, por favor rode o Shell script para criar a funcao e deploya-la no azure functions:

sh setup-functions.sh
Assim o azure cli fara a criacao da function, e depois buildara e em seguida a implantacao. Para que possamos testar se esta tudo ok antes de gastar dinheiro sem necessidade na azure, testemos localmente, para tanto sigas os passos a frente:

Execução Local

Para executar o projeto localmente, siga os passos abaixo:

Inicie a Azure Function localmente:

 func start
Teste a função a cessando o endpoint local gerado.
Publicação no Azure

Crie um recurso de Function App no Azure:
Essa prublicacao so se faz necessaria se tudo funcionar corretamente localmente. se sim, execute um comando parecido com esse :

 az functionapp create --resource-group $RESOURCE_GROUP --consumption-plan-location $REGION --runtime python --functions-version 4 --name $FUNCTION_APP_NAME --storage-account $STORAGE_ACCOUNT_NAME --os-type Linux
Configure as variáveis de ambiente na Function App:
As configuracaoes de variavel de ambiente ja estao no setup-functions.sh porem se algo mudar execute um comando baseado em :

      az functionapp config appsettings set --name <Nome-da-Sua-Function-App> --resource-group <Seu-Resource-Group> --settings AZURE_COSMOS_CONNECTION_STRING=$AZURE_COSMOS_CONNECTION_STRING AZURE_STORAGE_CONNECTION_STRING=$AZURE_STORAGE_CONNECTION_STRING
Publique a Azure Function: Se precisar mudar o codigo e republicar

 func azure functionapp publish <Nome-da-Sua-Function-App>
Gerenciamento de Variáveis de Ambiente

Este projeto utiliza variáveis de ambiente para configurar as conexões com o Cosmos DB e o Storage Account. Essas variáveis podem ser configuradas tanto localmente quanto no ambiente do Azure.

Recursos Adicionais

• Documentação do Azure Cosmos DB • Documentação do Azure Functions • Exemplo de API MongoDB no Cosmos DB

Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.