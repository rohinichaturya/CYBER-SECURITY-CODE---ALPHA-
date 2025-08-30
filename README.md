# Task 4 — Network Intrusion Detection System (NIDS)

This bundle includes a minimal working setup for Suricata + visualization and an optional
auto-response script that blocks offending IPs based on alerts.

## Contents
- `nids_autoblock.py` — reads Suricata `eve.json` from stdin and blocks `src_ip` via UFW
- `suricata_local.rules` — sample local rule (ICMP ping)
- `docker-compose.yml`, `pipelines.yml`, `pipeline/suricata.conf` — Elastic + Kibana + Logstash stack for dashboards

## Quick Start (Ubuntu/Debian)
```bash
sudo apt update && sudo apt -y install suricata suricata-update jq ufw docker.io docker-compose-plugin
ip a   # note your monitoring interface, e.g., eth0
sudo nano /etc/suricata/suricata.yaml   # set af-packet -> interface: eth0 and ensure eve-log enabled
echo '# include local rules' | sudo tee -a /etc/suricata/suricata.yaml >/dev/null
# place suricata_local.rules into /etc/suricata/rules/local.rules
sudo cp suricata_local.rules /etc/suricata/rules/local.rules
sudo suricata-update && sudo systemctl restart suricata
```

## Test Alerts
```bash
ping -c 1 1.1.1.1
tail -n 20 /var/log/suricata/eve.json | jq
```

## Auto-Block (optional, requires sudo)
```bash
sudo cp nids_autoblock.py /usr/local/bin/nids_autoblock.py
sudo chmod +x /usr/local/bin/nids_autoblock.py
tail -F /var/log/suricata/eve.json | sudo /usr/local/bin/nids_autoblock.py
```

## Visualization — EveBox (quickest)
```bash
docker run -d --name evebox -p 5636:5636 -v /var/log/suricata:/var/log/suricata:ro jasonish/evebox
# Visit http://localhost:5636
```

## Visualization — Elastic/Kibana via Docker Compose
```bash
cd Task4_NIDS_Code
docker compose up -d
# Visit http://localhost:5601 and create index pattern: suricata-*
```

## Troubleshooting
- `sudo journalctl -u suricata -e`
- `sudo ethtool -K eth0 gro off lro off`
- `sudo tcpdump -i eth0 -nn` (verify traffic visible)
- `sudo suricata -T -c /etc/suricata/suricata.yaml` (config test)
