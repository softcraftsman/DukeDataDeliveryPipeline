# DukeDataDeliveryPipeline
Services that deliver data stored in Azure between users.

```mermaid
sequenceDiagram
    participant User
    participant LogicApp
    participant DataFactory
    participant FunctionApp    
    participant AzureBlobStorage   
    participant DeliveryWebsite
    
    User->>LogicApp: POST delivery request to API
    LogicApp->>DataFactory: Runs DataDelivery pipeline
    DataFactory->>FunctionApp: Fetch list of files being delivered
    DataFactory->>AzureBlobStorage: Copy files to customer's bucket 
    DataFactory->>DeliveryWebsite: POST manifest of files delivered Delivery Website
```

## Azure Blob Storage Permissions
The following storage permissions are required:
- Data Factory
  - Write Permissions on the sink Container
  - Read Permissions on the source Container  
- Logic App
  - Read Permissions on the source Container
  
  
 
