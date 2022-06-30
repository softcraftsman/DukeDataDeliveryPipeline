# Azure Function to create a manifest for a storage account/filesystem/path.
# Reads all files based on the storage account, file system, and path.
# Returns a manifest of these files in the form of a JSON array.
# Each entry in the array contains a name, content_md5, and size for
# a file. Note that while Azure Blob Storage doesn't require content_md5
# this function does.
import logging
import json
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    body = json.loads(req.get_body())
    storage_account = body.get('storage_account')
    file_system_name = body.get('file_system')
    file_path = body.get('path')

    logging.info(
        f"ReadManifest called with {storage_account}, {file_system_name}, {file_path}")
    client = DataLakeServiceClient(
        f"https://{storage_account}.dfs.core.windows.net",
        credential=DefaultAzureCredential())
    file_system_client = client.get_file_system_client(file_system_name)

    result = []
    for path in file_system_client.get_paths(file_path):
        if not path.is_directory:
            file_client = file_system_client.get_file_client(path.name)
            file_properties = dict(file_client.get_file_properties())
            content_settings = file_properties.get("content_settings")
            content_md5 = content_settings["content_md5"].hex()
            result.append({
                "name": path.name,
                "content_md5": content_md5,
                "size": file_properties.get("size")
            })

    return func.HttpResponse(json.dumps(result), mimetype="application/json")

