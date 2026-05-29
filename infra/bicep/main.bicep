// TripWire — Azure-native infrastructure as code.
// One command provisions the full stack:
//   az deployment group create -g rg-tripwire -f main.bicep -p main.bicepparam
//
// Designed for the Azure for Students subscription: all SKUs chosen to fit the
// $100 credit ceiling. See AZURE_SETUP.md for the cost model.

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Short name prefix for all resources.')
param prefix string = 'tripwire'

@description('Azure OpenAI model deployments to create.')
param openAiDeployments array = [
  { name: 'gpt-4o', model: 'gpt-4o', version: '2024-08-06', capacity: 10 }
  { name: 'gpt-4o-mini', model: 'gpt-4o-mini', version: '2024-07-18', capacity: 30 }
  { name: 'text-embedding-3-large', model: 'text-embedding-3-large', version: '1', capacity: 30 }
]

@description('PostgreSQL admin login.')
param pgAdminUser string = 'tripwire_admin'

@secure()
@description('PostgreSQL admin password.')
param pgAdminPassword string

var uniqueSuffix = uniqueString(resourceGroup().id)

// ---------- Azure OpenAI ----------
resource openai 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: '${prefix}-aoai-${uniqueSuffix}'
  location: location
  kind: 'OpenAI'
  sku: { name: 'S0' }
  properties: {
    customSubDomainName: '${prefix}-aoai-${uniqueSuffix}'
    publicNetworkAccess: 'Enabled'
  }
}

@batchSize(1)
resource deployments 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = [
  for d in openAiDeployments: {
    parent: openai
    name: d.name
    sku: { name: 'Standard', capacity: d.capacity }
    properties: {
      model: { format: 'OpenAI', name: d.model, version: d.version }
    }
  }
]

// ---------- Azure AI Content Safety (Prompt Shields) ----------
resource contentSafety 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: '${prefix}-cs-${uniqueSuffix}'
  location: location
  kind: 'ContentSafety'
  sku: { name: 'S0' }
  properties: {
    customSubDomainName: '${prefix}-cs-${uniqueSuffix}'
    publicNetworkAccess: 'Enabled'
  }
}

// ---------- Cosmos DB for PostgreSQL (pgvector) ----------
resource pg 'Microsoft.DBforPostgreSQL/flexibleServers@2024-08-01' = {
  name: '${prefix}-pg-${uniqueSuffix}'
  location: location
  sku: { name: 'Standard_B1ms', tier: 'Burstable' }
  properties: {
    version: '16'
    administratorLogin: pgAdminUser
    administratorLoginPassword: pgAdminPassword
    storage: { storageSizeGB: 32 }
    backup: { backupRetentionDays: 7, geoRedundantBackup: 'Disabled' }
    highAvailability: { mode: 'Disabled' }
  }
}

resource pgFirewallAzure 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2024-08-01' = {
  parent: pg
  name: 'AllowAllAzureServices'
  properties: { startIpAddress: '0.0.0.0', endIpAddress: '0.0.0.0' }
}

// Enable pgvector at server level (allowlist the extension).
resource pgVectorConfig 'Microsoft.DBforPostgreSQL/flexibleServers/configurations@2024-08-01' = {
  parent: pg
  name: 'azure.extensions'
  properties: { value: 'VECTOR,PGCRYPTO', source: 'user-override' }
}

// ---------- Log Analytics + App Insights ----------
resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${prefix}-logs-${uniqueSuffix}'
  location: location
  properties: { sku: { name: 'PerGB2018' }, retentionInDays: 30 }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${prefix}-ai-${uniqueSuffix}'
  location: location
  kind: 'web'
  properties: { Application_Type: 'web', WorkspaceResourceId: logs.id }
}

// ---------- Container Apps environment ----------
resource acaEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: '${prefix}-env'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logs.properties.customerId
        sharedKey: logs.listKeys().primarySharedKey
      }
    }
  }
}

// ---------- SignalR (Free tier) ----------
resource signalr 'Microsoft.SignalRService/signalR@2024-03-01' = {
  name: '${prefix}-sr-${uniqueSuffix}'
  location: location
  sku: { name: 'Free_F1', tier: 'Free', capacity: 1 }
  kind: 'SignalR'
  properties: { features: [ { flag: 'ServiceMode', value: 'Default' } ] }
}

// ---------- Outputs (wire into apps/api/.env) ----------
output openAiEndpoint string = openai.properties.endpoint
output contentSafetyEndpoint string = contentSafety.properties.endpoint
output postgresHost string = pg.properties.fullyQualifiedDomainName
output appInsightsConnectionString string = appInsights.properties.ConnectionString
output containerAppsEnvId string = acaEnv.id
