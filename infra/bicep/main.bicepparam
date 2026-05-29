using './main.bicep'

param prefix = 'tripwire'
// Provide via CLI: -p pgAdminPassword=$(openssl rand -base64 24)
// Never commit a real password.
param pgAdminPassword = readEnvironmentVariable('PG_ADMIN_PASSWORD', '')
