import os
import json
import logging
import requests

ZONE_NAME = os.getenv("CF_ZONE_NAME")
CF_API_TOKEN = os.getenv("CF_API_TOKEN")
CONFIG_PATH = os.getenv("CONFIG_PATH", "config.json")
LOG_PATH = os.getenv("LOG_PATH", "logs/dns_manager.log")

HEADERS = {
    "Authorization": f"Bearer {CF_API_TOKEN}",
    "Content-Type": "application/json"
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)

def get_zone_id():
    url = f"https://api.cloudflare.com/client/v4/zones?name={ZONE_NAME}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    result = resp.json()["result"]
    return result[0]["id"] if result else None

def get_dns_record(zone_id, name):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?name={name}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    records = resp.json()["result"]
    return records[0] if records else None

def delete_record(zone_id, record_id):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    resp = requests.delete(url, headers=HEADERS)
    resp.raise_for_status()
    logging.info(f"Deleted record ID: {record_id}")

def create_record(zone_id, record):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    resp = requests.post(url, headers=HEADERS, json=record)
    resp.raise_for_status()
    logging.info(f"Created {record['type']} record for {record['name']} -> {record['content']}")

def sync_record(zone_id, record_cfg):
    name = record_cfg["name"]
    record_type = record_cfg["type"]
    content = record_cfg["content"]
    proxied = record_cfg.get("proxied", False)
    ttl = record_cfg.get("ttl", 300)

    fqdn = f"{name}.{ZONE_NAME}" if not name.endswith(ZONE_NAME) else name
    existing = get_dns_record(zone_id, fqdn)

    if existing:
        if existing["type"] == record_type and existing["content"] == content:
            logging.info(f"{record_type} record for {fqdn} already exists and is correct.")
            return
        else:
            logging.warning(f"Conflicting record found for {fqdn}. Deleting.")
            delete_record(zone_id, existing["id"])

    new_record = {
        "type": record_type,
        "name": fqdn,
        "content": content,
        "ttl": ttl
    }

    if record_type in ("CNAME", "A", "AAAA"):
        new_record["proxied"] = proxied

    create_record(zone_id, new_record)

def main():
    zone_id = get_zone_id()
    if not zone_id:
        logging.error("Zone ID not found.")
        return

    with open(CONFIG_PATH, "r") as f:
        records = json.load(f)

    for record in records:
        try:
            sync_record(zone_id, record)
        except Exception as e:
            logging.error(f"Error syncing {record['name']}: {e}")

if __name__ == "__main__":
    main()
