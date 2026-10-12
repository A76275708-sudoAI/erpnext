# ERP v1 — Bench / Docker install

## D7 runtime on agent box (2026-10-12 Asia/Shanghai)

Runnable path: **frappe_docker disposable stack** pinned to `frappe/erpnext:v15.122.0` + bind-mounted `erp_fulfillment`.

| Item | Value |
|------|-------|
| URL | http://127.0.0.1:8080 |
| Site name | `frontend` |
| Admin | `Administrator` / `admin` (local-only weak password) |
| Compose | `docker-compose.frappe-pwd-v15.yml` (also `/workspace/frappe_docker/pwd-v15.yml`) |
| Start helper | `./scripts/d7-start-frappe-docker.sh` |

Apps on site: `frappe`, `erpnext`, `erp_fulfillment`. Fixtures imported (7 roles, 9 custom fields). Seven smoke users created (see `d7-status.md`).

### Box quirks fixed in D7

1. **8G `/swapfile`** — created + fstab entry (was 0 swap).
2. **Docker without systemd** — `containerd` + `dockerd` started manually; `policy-rc.d` blocks service start.
3. **iptables-legacy FORWARD DROP** — container→container TCP timed out until `iptables-legacy -P FORWARD ACCEPT`.
4. **YAML flow-list commas** — `command: [bench, worker, --queue, short,default,long]` splits queue names; use block list.

### One-command restart (after reboot / dockerd death)

```bash
./scripts/d7-start-frappe-docker.sh
# first boot / empty volumes: create-site takes ~2–5 min
```

### Re-install erp_fulfillment after fresh create-site

```bash
docker exec -u frappe frappe_docker-backend-1 bash -lc '
  cd /home/frappe/frappe-bench
  grep -qx erp_fulfillment sites/apps.txt || echo erp_fulfillment >> sites/apps.txt
  ./env/bin/pip install -e apps/erp_fulfillment -q
  bench --site frontend install-app erp_fulfillment
  ERP_V1_FIXTURES_DIR=/home/frappe/frappe-bench/fixtures-erp-v1/erp_v1 \
    bench --site frontend execute erp_fulfillment.scripts.import_fixtures.run
  bench --site frontend execute erp_fulfillment.scripts.create_smoke_users.run
'
docker restart frappe_docker-backend-1
```

## Legacy D6 notes (native bench)

Full native bench still needs Python 3.10/3.11, Node 18+, yarn. Prefer Docker path above on this box.

```bash
docker compose -f docker-compose.erp-v1.yml up -d   # MariaDB+Redis only
export MYSQL_ROOT_PASSWORD=erp_v1_root
./scripts/install-bench-erp-v1.sh
```
