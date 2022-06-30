# DukeDataDeliveryPipeline
Services that deliver data stored in Azure between users.

```mermaid
sequenceDiagram
    participant DDD
    participant LogicApp
    participant DataFactory
    participant FunctionApp    
    participant AzureBlobStorage   
    
    DDD->>LogicApp: POST source and destinations to API
    LogicApp->>DataFactory: Run DataDelivery pipeline
    DataFactory->>FunctionApp: Fetch list of files being delivered
    DataFactory->>AzureBlobStorage: Copy files to destination container
    DataFactory->>DDD: POST manifest of files delivered to DDD
```
## Detailed Flow

- [DDD - Duke Data Delivery Website](https://github.com/Duke-GCB/D4S2)
  - Sends POST request containing
    - Azure Blob Storage source and destination container paths
    - Delivery UUID - unique identifier for each delivery request
    - Delivery ID - id of the delivery being performed
  - Receives a POST at the end of the process 
    - on success the POST contains a manifest of the files delivered
    - on failure the POST contains an error message
- [Logic App](logic-app.json)
  - Receives a POST request
  - Reads key vault for URL and authentication for webhook
  - Runs DataFactory passing request body and webhook config
- [Data Factory](data-factory.json)
  - Calls FunctionApp to create a manifest of files being delivered
  - Uses `Copy data` Activity to copy data to the destination
  - Notifies the external webhook on failure or success of the pipeline
- [Function App](function-app)
  - Reads source files returning a manifest including file paths and their checksums

## Azure Blob Storage Permissions
The following storage permissions are required:
- Data Factory
  - Write Permissions on the sink container
  - Read Permissions on the source container  
- Function App
  - Read Permissions on the source container
