
# Cloudflare DNS Manager

A Dockerized Python script to manage Cloudflare DNS records, supporting **CNAME**, **A**, **AAAA**, **TXT**, and other record types. It uses **Supercronic** for scheduled execution (cron jobs) to ensure DNS records are always in sync.

## Features

- ✅ Manage Cloudflare DNS records through **Cloudflare API**
- ✅ Supports **CNAME**, **A**, **AAAA**, **TXT**, and other DNS record types
- ✅ **Supercronic** integration for scheduling DNS updates
- ✅ Dockerized for easy deployment and management
- ✅ Logging of DNS sync operations
- ✅ Customizable cron schedule for syncing DNS records

## Prerequisites

- **Docker** and **Docker Compose** installed
- **Cloudflare API Token** with `DNS:Edit` permissions for the domain you wish to manage

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cloudflare-dns-manager.git
cd cloudflare-dns-manager
```

### 2. Configure Cloudflare API Token

Create a `.env` file in the root directory and add your Cloudflare API token:

```bash
echo "CF_API_TOKEN=your-cloudflare-api-token" > .env
```

The API token must have `DNS:Edit` permissions for the domain you want to manage.

### 3. Configure DNS Records

Edit the `config.json` file to define the DNS records you want to manage. Here’s an example:

```json
[
  {
    "type": "CNAME",
    "name": "plex",
    "content": "home.example.com",
    "proxied": true
  },
  {
    "type": "TXT",
    "name": "acme-challenge",
    "content": "validation-token",
    "ttl": 120
  },
  {
    "type": "A",
    "name": "vpn",
    "content": "203.0.113.25",
    "proxied": false
  }
]
```

You can define any combination of DNS records (CNAME, TXT, A, etc.) that you want to manage.

### 4. Build and Run the Container

Once you've configured the necessary files, build and run the Docker container using Docker Compose:

```bash
docker compose up --build -d
```

This will build the container, start the service, and schedule the DNS sync based on the cron job defined in `schedule.cron`.

### 5. Check Logs

The logs for the DNS synchronization will be available in the `logs/` directory:

- **DNS Sync Log**: `logs/dns_manager.log`
- **Cron Job Log**: `logs/cron.log`

### 6. Customize the Cron Schedule

The sync is scheduled to run daily at 3:45 AM by default in the `schedule.cron` file:

```cron
45 3 * * * python3 /app/cloudflare_dns.py >> /app/logs/cron.log 2>&1
```

Feel free to modify the cron schedule to your needs. For example:

- `*/15 * * * *` → runs every 15 minutes
- `0 * * * *` → runs every hour

You can use [crontab.guru](https://crontab.guru) to easily generate cron expressions.

## Docker Compose Configuration

The project uses **Docker Compose** to manage the service. Below is the configuration:

```yaml
services:
  cloudflare-dns-manager:
    build: .
    container_name: cloudflare-dns-manager
    environment:
      - CF_API_TOKEN=${CF_API_TOKEN}
      - CF_ZONE_NAME=example.com
      - CONFIG_PATH=/app/config.json
      - LOG_PATH=/app/logs/dns_manager.log
    volumes:
      - ./config.json:/app/config.json:ro
      - ./logs:/app/logs
    restart: unless-stopped
```

## Troubleshooting

- **Cloudflare API Token**: Make sure your API token has the correct permissions (`DNS:Edit`) for the specified domain.
- **Cron Jobs**: Ensure that the cron schedule is correct in `schedule.cron` for the desired execution frequency.
- **Logs**: Check the logs located in the `logs/` directory for detailed information about the DNS record synchronization process.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
