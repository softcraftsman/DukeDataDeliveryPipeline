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
    
    User->>LogicApp: POST source and destinations to API
    LogicApp->>DataFactory: Run DataDelivery pipeline
    DataFactory->>FunctionApp: Fetch list of files being delivered
    DataFactory->>AzureBlobStorage: Copy files to destination container
    DataFactory->>DeliveryWebsite: POST manifest of files delivered Delivery Website
```

## Azure Blob Storage Permissions
The following storage permissions are required:
- Data Factory
  - Write Permissions on the sink container
  - Read Permissions on the source container  
- Logic App
  - Read Permissions on the source container
  
  
 
