FROM python:3.11-slim

# Install Supercronic
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.29/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic

RUN apt-get update && apt-get install -y curl \
  && curl -fsSLo /usr/local/bin/${SUPERCRONIC} ${SUPERCRONIC_URL} \
  && chmod +x /usr/local/bin/${SUPERCRONIC} \
  && mkdir -p /app/logs \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cloudflare_dns.py config.json entrypoint.sh schedule.cron ./
RUN chmod +x entrypoint.sh

VOLUME /app/logs

ENTRYPOINT ["./entrypoint.sh"]
