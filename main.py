import os
import requests
from dotenv import load_dotenv
from typing import Any, Dict
from utils import beautify_resopnse

load_dotenv()

api_key = os.getenv('COOLIFY_API_KEY')
base_url = os.getenv('BASE_URL')

headers = {
    'Authorization': f'Bearer {api_key}'
}

# name of the db under configuration, general
cool_db_name = "postgresql-database-ys0k4sokowssos80004c08g8"
uuid = "ys0k4sokowssos80004c08g8"


# GET /databases
def get_datbases_with_backups(db_name: str = "", config: bool = False) -> Dict[str, Any]:
    r = requests.get(f"{base_url}/databases", headers=headers)
    if db_name:
        for item in r.json():
            if item.get("name") == db_name:
                return beautify_resopnse(item)

    return r.json()[0]["backup_configs"] if config else r.json()[0]


# GET /databases/:uuid/backups
def get_database_backup_details_by_uuid(uuid: str) -> Dict[str, Any]:
    r = requests.get(f"{base_url}/databases/{uuid}/backups", headers=headers)
    return r.json()


example_patch_body = {
    "save_s3": True,
    "enabled": True,
    "dump_all": True,
    "frequency": "daily",
    "database_backup_retention_amount_locally": 30,
    "database_backup_retention_days_locally": 1337,
    "database_backup_retention_max_storage_locally": 30,
    "database_backup_retention_amount_s3": 90,
    "database_backup_retention_days_s3": 2000,
    "database_backup_retention_max_storage_s3": 90,
}


# PATCH /datbases/:uuid
def update_database_backup(uuid: str) -> Dict[str, Any]:
    r = requests.patch(f"{base_url}/databases/{uuid}",
                       headers=headers, json=example_patch_body)
    if r.status_code != 200:
        print(f"Error: received status code {r.status_code}")
        print(f"Response content: {r.text}")
        return {}

    try:
        return r.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: resopnse is not valid json")
        print(f"Response content: {r.text}")
        return {}


# DELETE /databases/{uuid}/backups/{backup_id}
# 0 will be the latest backup and `len(get_database_backup_details_by_uuid(uuid)) - 1` will be the first backup
def delete_specific_backup_by_uuid_and_backupID(uuid: str, backup_id: int) -> Dict[str, Any]:
    bid = get_database_backup_details_by_uuid(
        uuid)["executions"][backup_id]['id']

    r = requests.delete(
        f"{base_url}/databases/{uuid}/backups/{bid}", headers=headers)

    if r.status_code != 200:
        print(f"Error: received status code {r.status_code}")
        print(f"Response content: {r.text}")
        return {}

    return r.json()


def main():
    a = get_datbases_with_backups(cool_db_name)
    # b = get_database_backup_details_by_uuid(uuid)["executions"][0]['id']
    # c = update_database_backup(uuid)
    # d = delete_specific_backup_by_uuid_and_backupID(uuid, 0)
    print(beautify_resopnse(a))


if __name__ == "__main__":
    main()
