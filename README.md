# devspoon-startup-cloud-tizen

**[English](README.md)** · [한국어](README-kr.md)

Docker-based templates for a web stack (nginx + Django / PHP) and project-management solutions — Plane, Jenkins, Gitea and Harbor. SmartThings / Bixby-integrated application servers are not provided.

## Discontinuation of support for open source development

This project no longer offers open source development support, for startup commercial development and for security reasons.

The configuration shipped in this repository is still complete and verified end to end — only new open source development support has stopped.

## Repository family — which one to pick

This repository is one of four that share the same foundation. Pick by what you need to run, not by name.

| Repository | What it adds | Pick it when |
|---|---|---|
| [devspoon-web] | The web stack only — 6 stacks (gunicorn · uvicorn · uwsgi · daphne · php-7.3 · php-8.4) | You only need to serve a web app or API |
| [devspoon-startup-web] | + Plane · Jenkins · Gitea · Harbor | You want the project-management solutions too |
| devspoon-startup-tizen | + a Tizen development environment (`dev_env_service/tizen-env`, `tizenenv`) | You develop for Samsung Tizen IoT devices |
| **devspoon-startup-cloud-tizen** (this one) | The same set as devspoon-startup-web, positioned for cloud operation | You run on a cloud VM and do not need the Tizen toolchain |

**What this repository actually contains**: the web/app-server layer here is the same as [devspoon-startup-web] — the same five stacks, the same app-server configs, the same nginx configs. The compose files for the Python stacks are byte-identical to [devspoon-web]'s. There is no Tizen toolchain and no SmartThings / Bixby application server.

So the practical difference is positioning, not structure: this repository is the one to clone when the target is a cloud VM and you want the whole project-management set without the Tizen tooling.

## Project management solutions

These are the four solutions this repository can install. Follow the links for the full description, architecture and installation steps of each.

| Solution | What it does | Containers | Install method | Details (upstream repository) |
|---|---|---|---|---|
| **[Plane](#plane)** | Project management — issues · cycles · modules | 13 | compose (standalone / all-in-one) | [makeplane/plane](https://github.com/makeplane/plane) |
| **[Jenkins](#jenkins)** | CI — automated build · test · deploy | 2 | compose (standalone / all-in-one) | [jenkinsci/jenkins](https://github.com/jenkinsci/jenkins) |
| **[Gitea](#gitea)** | Self-hosted git service | 1 | compose (standalone / all-in-one) | [go-gitea/gitea](https://github.com/go-gitea/gitea) |
| **[Harbor](#harbor)** | Private Docker Registry | created by installer | **its own installer** (separate host recommended) | [goharbor/harbor](https://github.com/goharbor/harbor) |

Plane, Jenkins and Gitea can run **together** behind a single nginx (→ [all-in-one startup](#all-in-one-startup--master_service-one-compose-file-for-everything)), or you can run just **one** of them at a time (→ [standalone](#project_mng_service--standalone-installation)).

## Features

- **Web stacks ported from devspoon-web** — `compose/web_service/` has five stacks: `nginx_gunicorn`, `nginx_uvicorn`, `nginx_uwsgi`, `nginx_daphne` (Python / Django 6, uv) and `nginx_php` (PHP 8.4 only). See [Web stack & CI](#web-stack--ci).

- **Install only what you need** — pick a single solution under `compose/project_mng_service/<solution>` instead of installing all of them. Run only one standalone service at a time (see [Standalone concurrency rules](#standalone-concurrency-rules)).

- **All-in-one combinations** — to run a web stack together with Plane, Jenkins and Gitea, use one of the five files in `compose/master_service/` (see [all-in-one startup](#all-in-one-startup--master_service-one-compose-file-for-everything)).

- **One nginx reverse-proxies everything** — in master_service a single nginx serves the web app and reverse-proxies Plane, Jenkins and Gitea by domain.

  ```
  Example

  test.com        -> company website
  plane.test.com  -> Plane
  jen.test.com    -> Jenkins
  git.test.com    -> Gitea
  ```

- **Secrets kept out of git (`.env-example`)** — every compose folder ships a tracked `.env-example` while the real `.env` is gitignored. Copy it to `.env`, generate the empty secrets with `script/lib/django_secrets.sh` (`ensure_env_secrets`), and never commit the live file. The `${VAR:?}` checks in the compose files fail fast when a required secret is missing.

- **Other**

  - Gitea serves git over SSH on port 2222.
  - Harbor is installed with its own installer scripts (see [Harbor](#harbor)).

## Considerations

- **Development-oriented docker service** — a good fit for startups and new-service teams that change and test things often.

- **Built for cloud VMs as much as for bare servers** — it runs on a server you operate yourself, and it is also used in production on OCI (Oracle Cloud Infrastructure); AWS and GCP work the same way. Nothing here depends on a managed service, so the same compose files move between them.

- **On a cloud VM, remember the security group** — ports Docker publishes bypass the host's iptables INPUT chain. Opening a port with `ufw` alone is not enough: you must also allow it in the cloud security group (OCI VCN security list, AWS security group and so on). The symptom when you forget is distinctive — the private IP works while the public domain times out. This bites hardest on Gitea's git-over-SSH port **2222**, which the container publishes directly (80 and 443 are usually already open).

- **Cloud storage and backups are yours to arrange** — Plane and Gitea keep their data in named volumes on the instance's disk. Snapshot the volume (or run the documented `pg_dump` / `gitea dump`) as part of your instance backup policy; nothing here replicates to object storage on its own.

- **Requirements** — Docker Engine with the Compose plugin. **≥ 2.17** is required for the Python app image builds, and **≥ 2.20** for `include:`, which master_service and the standalone Plane / Gitea stacks rely on. The legacy `docker-compose` (v1) command is only used by the bundled Harbor installer.

## Web stack & CI

The web stack description matches the canonical [devspoon-web] README, adapted to this repository's layout. Every command starts from the repository root.

### The five stacks

| Stack | compose folder | app service | nginx config folder | Profile | Host ports |
|---|---|---|---|---|---|
| gunicorn | `compose/web_service/nginx_gunicorn` | `gunicorn-app` | `config/web-server/nginx/gunicorn` | `celery` | 80, 443, `127.0.0.1:5555` (flower) |
| uvicorn | `compose/web_service/nginx_uvicorn` | `uvicorn-app` | `config/web-server/nginx/uvicorn` | `celery` | 80, 443, `127.0.0.1:5555` |
| uwsgi | `compose/web_service/nginx_uwsgi` | `uwsgi-app` | `config/web-server/nginx/uwsgi` | `celery` | 80, 443, `127.0.0.1:5555` |
| daphne | `compose/web_service/nginx_daphne` | `daphne-app` | `config/web-server/nginx/gunicorn` (shared) | `celery` | 80, 443, `127.0.0.1:5555` |
| php 8.4 | `compose/web_service/nginx_php` | `php-app` | `config/web-server/nginx/php` | `redis` | 80, 443 |

- Python stacks always start `webserver`, the app and `redis`; `--profile celery` adds `celery`, `celery-beat` and `flower`. The php stack starts `webserver` and `php-app`, and `--profile redis` adds `redis`.
- Every stack uses ports 80/443, so run only one stack per host.
- Sample apps: `www/django_sample` for Python stacks, `www/php_sample` for the php stack.

### 1. Generating `.env` secrets (first setup · upgrade)

The secrets in `.env-example` are **empty** (`DJANGO_SECRET_KEY`, `REDIS_PASSWORD`, `FLOWER_PWD` for Python stacks; `REDIS_PASSWORD` for php). Compose requires them with `${VAR:?}`, so startup is refused while they are blank. Run this once per stack, from the repository root:

```bash
D=compose/web_service/nginx_gunicorn
cp "$D/.env-example" "$D/.env"
bash -c ". script/lib/django_secrets.sh && ensure_env_secrets $D/.env"
```

- Only secret keys that are empty or still hold the old `CHANGE_ME_*` placeholder are filled with `openssl rand -hex` values (`DJANGO_SECRET_KEY` 100 hex, `*_KEY_BASE` 128 hex, everything else 64 hex). Keys that already have a value are left alone.
- The helper writes to a temporary file in the same folder and swaps it in; if it generated anything, it tightens the permissions to 600 (stricter permissions are kept). If openssl is missing or fails it ends with `FAIL` and `.env` is untouched.
- **The helper does not fill non-secret placeholders — enter them yourself before going live.**

  | Key | Where | Value |
  |---|---|---|
  | `FLOWER_ID` | web stacks · master | flower login ID (default `CHANGE_ME_FLOWER_USER`) |
  | `DJANGO_ALLOWED_HOSTS` | web stacks · master | add the domain you serve |
  | `PLANE_DOMAIN` · `PLANE_WEB_URL` · `PLANE_CORS_ALLOWED_ORIGINS` | master · standalone plane | all three the same domain, matching `server_name` in the proxy conf |
  | `GITEA_DOMAIN` · `GITEA_ROOT_URL` | master · standalone gitea | the domain and the full URL |

- `www/django_sample/secrets.json` is only needed when you run `manage.py` directly on the host: `bash -c '. script/lib/django_secrets.sh && ensure_django_secrets'` (created only when missing, mode 600). Containers use the `DJANGO_SECRET_KEY` environment variable.

> **Upgrade note — keeping an `.env` from an older version**
>
> An old `.env` may have no `DJANGO_SECRET_KEY` line at all, or may still hold `CHANGE_ME_*` values. Running the helper once on that same `.env` fixes it.
>
> What the helper does:
>
> - **Where it looks**: `docker-compose*.yml` in the same folder, plus any fragment those files pull in with `include:` (`compose/common/*.yml`).
> - **What it looks for**: keys those files require with `:?` whose name contains SECRET, PASSWORD or PWD, or ends with `_KEY_BASE`.
> - **What it does**: appends missing keys at the end of the file and replaces `CHANGE_ME_*` with new values. Keys that already have a value are untouched, and the file mode is set to 600.
>
> A quoted empty value such as `KEY=""` is not filled. Change it to `KEY=` first.
>
> Older versions tracked the `.env` files under `compose/web_service/*`, `compose/master_service` and `compose/project_mng_service/*` in git. They are untracked now, so `git pull` may remove your local `.env` — **copy it somewhere safe before pulling.** If you are running with keys from a `secrets.json` or `.env` that was once public in the repository, replace them (this invalidates sessions).

### 2. Starting a stack

After the `.env` commands in §1 (run from the repository root), move into the stack folder and start it. Add `--build` to rebuild images after an upgrade or a change to a Dockerfile / `uv.lock`. Run only one stack per host.

```bash
# gunicorn (from the repository root)
cd compose/web_service/nginx_gunicorn
docker compose up -d --build             # webserver + gunicorn-app + redis
docker compose --profile celery up -d    # + celery · celery-beat · flower
```

uvicorn, uwsgi and daphne use the same commands — only the folder name changes to `compose/web_service/nginx_uvicorn`, `nginx_uwsgi` or `nginx_daphne`.

```bash
# php (from the repository root)
cd compose/web_service/nginx_php
docker compose up -d --build             # webserver + php-app
docker compose --profile redis up -d     # + redis
```

> ⚠️ **`docker compose down -v` deletes named volumes**, including the web stack's app data, master_service's Plane data (`plane-pgdata` and friends) and Gitea's repositories (`gitea-data`). Use `stop` when you only want to bring the containers down.

- **Startup order — the app initialises the DB, then celery and beat start.**
  Only the app service initialises the database: `python manage.py migrate --noinput` if `manage.py` exists, otherwise the project's `prestart.sh`. `celery` and `celery-beat` are bound with `depends_on: <app>: condition: service_healthy`, so they start after the app is healthy. No two containers race to migrate.
- **Flower binds to `127.0.0.1:5555` only.** Reach it over an SSH tunnel: `ssh -L 5555:127.0.0.1:5555 <host>`, then open `http://127.0.0.1:5555` locally.
- `DJANGO_DEBUG` (default `0`) and `DJANGO_ALLOWED_HOSTS` are controlled through `.env` and passed to the app, celery and beat. Use `DJANGO_DEBUG=1` only for local development.
- Operate containers with `docker compose stop` / `start` / `restart`. Include the same profile you started with when profile services are involved (`docker compose --profile celery stop`, or `--profile redis` for php) — without it, `stop` leaves celery, celery-beat and flower (or redis) running.

### 3. Image names · build · uv

- **Image names** follow `${IMAGE_NAMESPACE:-devspoon}-nginx:latest` (`-py-app:latest`, `-uwsgi-app:latest`, `-php-app:8.4`). With the default value you get `devspoon-*` tags.

  Tests use a different namespace so they never overwrite your production tags — the verifiers and `verify-ngxblocker.sh` use `IMAGE_NAMESPACE=devspoon-it`, and run-ci's build step (`s2_build.sh`) uses `devspoon-test/*`.
- The pre-installed packages in the app images (`py-app`, `uwsgi-app`) are derived from `www/django_sample/uv.lock`. Compose passes it automatically via `build.additional_contexts: lock: ../../../www/django_sample`, which needs **Docker Compose ≥ 2.17**  (`docker compose version`).
- If your Compose is older than 2.17, or you call `docker build` directly, pass the extra build context explicitly (from the repository root, with BuildKit):

  ```bash
  docker build --build-context lock=www/django_sample -t devspoon-py-app:latest docker/gunicorn/
  docker build --build-context lock=www/django_sample -t devspoon-uwsgi-app:latest docker/uwsgi/
  ```

  Leaving it out makes the build fail with `"/pyproject.toml": not found`.
- **uv** — dependencies for `www/django_sample` are managed with `pyproject.toml` and `uv.lock`. Containers install into the system Python without a virtualenv (`UV_PROJECT_ENVIRONMENT=/usr/local`), and the startup command runs `uv sync --inexact --extra <stack> --extra celery`. The app, celery and celery-beat of one stack sync with the same extras.

  Adding a dependency has an order to it:

  ```bash
  cd www/django_sample && uv add <pkg>        # 1. add on the host → commit uv.lock
  cd compose/web_service/nginx_gunicorn        # 2. into the stack folder
  docker compose --profile celery stop
  docker compose up -d --build                 # 3. rebuild the app image
  docker compose --profile celery up -d        # 4. bring celery · celery-beat back too
  ```

  Skip step 4 and celery keeps running with the old dependencies. The celery services have no `build:` of their own — they only reference the app's image — so `up --build` without the profile does not replace them.

### 4. nginx · php configuration

- **nginx conf generators** — `nginx_http_conf.sh` and `nginx_https_conf.sh` under `config/web-server/nginx/<gunicorn|uvicorn|uwsgi|php>/` turn `sample_nginx_http(s).conf` into per-domain configs in `conf.d/`. Run with `-h` for the options. The daphne stack reuses the gunicorn folder.
- **nginx startup hook** — the image's `/docker-entrypoint.d/30-wait-upstreams.sh` waits until the upstream names (app containers) in the configs resolve before starting nginx. The wait is `NGINX_UPSTREAM_WAIT` seconds (default 30, `0` disables it), adjustable through the webserver's `environment`.

  This prevents nginx from dying with `[emerg] host not found in upstream` when it comes up before the app, such as after a reboot or a `start`. It cannot fully cover a whole-project `docker compose restart`, where everything restarts at once — **apply config changes with `nginx -s reload`, and restart everything with `stop` → `start`.**
- **Edit the php-fpm pool at `config/app-server/php/pool.d/www.conf`.** Compose mounts exactly two files read-only: that `www.conf` and `config/app-server/php/php_ini/php.ini`. Any `<DOMAIN>_php.conf` that `php_conf.sh` writes into `pool.d/` is therefore never loaded.

### 5. CI — `script/ci/run-ci.sh`

#### What it is for

A regression suite that answers one question after you change the repository: **do all the stacks in it still actually come up?** It does not stop at syntax checks — it starts the containers and waits for real responses.

GitHub Actions (`.github/workflows/test.yml`) calls the same script on every push, and you can run `bash script/ci/run-ci.sh` locally for the same result.

#### How it works

It runs 12 steps **in order** and **stops immediately** on the first failure. Each step writes a log under `log/ci/`, and on failure it reports which step failed and why, with the tail of that log.

| # | Step | What it does |
|---|---|---|
| 1 | preflight | Checks the required tools and files exist and the design invariants hold (read-only) |
| 2 | dependency audit | `uv audit` over every `www/*/uv.lock` — fails if a lock carries a known vulnerability that is not in `script/test/audit-allow.txt` (read-only, a few seconds) |
| 3 | prereq · log dirs | Creates the log folders the tests write to |
| 4 | nginx conf generators | Verifies the configs produced by `nginx_http_conf.sh` / `nginx_https_conf.sh` match the inputs |
| 5 | compose validation | Compose syntax and mount paths for every stack |
| 6 | repository-specific checks | `script/ci/repo-steps.sh` — rules unique to this repository (static assertions for Plane, Gitea, Jenkins, Harbor) |
| 7 | image builds | Builds every Dockerfile under `devspoon-test/*` tags (never overwriting production tags) |
| 8 | static regression | `s6_regression.sh` — invariants that catch previously fixed defects coming back |
| 9 | healthcheck | Validates the healthcheck and `depends_on` declarations of the five stacks |
| 10 | stack matrix | **Actually starts** gunicorn · uvicorn · uwsgi · daphne · php in turn — 200 responses, bot blocking, healthy, zero restarts, DEBUG off, 403 on upload paths |
| 11 | sample projects | Checks the django and php samples work |
| 12 | script logs | Checks the scripts write their logs properly |

#### Requirements

- It starts real containers, so **host ports 80, 443 and 5555 must be free.**
- Tools needed: docker (Compose ≥ 2.17), uv, jq, curl, openssl, php-cli.
- Notifications are optional. If the repository secrets `SLACK_WEBHOOK_URL`, `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are absent, only those notifications are skipped — the tests still run.
- Uploaded logs (`log/ci`, `log/test_run`) are masked with `script/lib/mask_secrets.sh` before upload.

#### If you do not want it

CI only serves repository maintenance; it has nothing to do with running the services. Delete `.github/workflows/test.yml` and Actions stops running. You can delete `script/ci/` and `script/test_run/` entirely without affecting anything under `compose/`.

## Choosing an install method — all-in-one vs standalone

Plane, Jenkins and Gitea can be installed **two ways**. Either way the service definitions come from the same files under `compose/common/`, so behaviour is identical — the only difference is whether they share one front nginx.

| | All-in-one (`compose/master_service`) | Standalone (`compose/project_mng_service`) |
|---|---|---|
| What comes up | web stack + Plane + Jenkins + Gitea, **all at once** | the **one** service you picked |
| nginx | **one nginx** proxies the web app and all three by domain | one nginx dedicated to that service |
| Running together | everything runs together | **one at a time** (they all take 80/443) |
| TLS | can be configured ([HTTPS section](#setting-up-https-on-a-web-server)) | **HTTP only** |
| When to use | production, running several solutions together | evaluating or testing a single service |

Harbor installs through its own installer and belongs to neither — see [Harbor](#harbor).

```
All-in-one example — one nginx splits traffic by domain

  test.com        ->  web app (django / php)
  plane.test.com  ->  Plane
  jen.test.com    ->  Jenkins
  git.test.com    ->  Gitea   (+ git clone over ssh://…:2222)
```

## All-in-one startup — master_service (one compose file for everything)

Running **one** compose file from `compose/master_service/` brings up the web stack, Plane, Jenkins and Gitea together, with a single nginx splitting traffic by domain. There is no need to start each service separately.

### Choosing a file

Only the web stack differs; **Plane, Jenkins and Gitea are in all five files.** Pick one.

| File | Web stack | Profile to add |
|---|---|---|
| `docker-compose-gunicorn.yml` | gunicorn | `--profile celery` |
| `docker-compose-uvicorn.yml` | uvicorn | `--profile celery` |
| `docker-compose-uwsgi.yml` | uwsgi | `--profile celery` |
| `docker-compose-daphne.yml` | daphne | `--profile celery` |
| `docker-compose-php.yml` | php 8.4 | `--profile redis` (no celery) |

What one file brings up — **17 containers** for the php combination:

| Group | Containers |
|---|---|
| Web | `nginx-webserver` · `php-app` (or `<stack>-app`) · `redis_db` |
| Plane | `plane-db` · `plane-redis` · `plane-mq` · `plane-minio` · `plane-migrator` (one-shot) · `plane-api` · `plane-worker` · `plane-beat-worker` · `plane-web` · `plane-space` · `plane-admin` · `plane-live` · `plane-proxy` |
| Jenkins | `jenkins` ( + one-shot `jenkins-init`) |
| Gitea | `gitea` |

The Plane and Gitea definitions are pulled in with `include:` from the **same files** the standalone stacks use (`compose/common/{plane-services,gitea-service}.yml`) — this needs **Docker Compose ≥ 2.20**.

### Startup steps

All commands below start from the **repository root**. There is nothing to prepare in advance — the Plane and Gitea admin accounts are created after startup.

**1. Create `.env` and fill in the secrets**

```bash
D=compose/master_service
cp "$D/.env-example" "$D/.env"
bash -c ". script/lib/django_secrets.sh && ensure_env_secrets $D/.env"
```

The helper walks the `include:`d definitions too, so it fills the five Plane secrets along with `REDIS_PASSWORD`, `DJANGO_SECRET_KEY` and the rest.

**2. Fill in the placeholders yourself** — the helper does not touch these. Open `compose/master_service/.env` and put in your real domains.

| Key | Value | Notes |
|---|---|---|
| `DJANGO_ALLOWED_HOSTS` | add the web app domain | e.g. `localhost,127.0.0.1,web.example.com` |
| `PLANE_DOMAIN` · `PLANE_WEB_URL` · `PLANE_CORS_ALLOWED_ORIGINS` | the Plane domain (all three identical) | `WEB_URL` and `CORS` include the `http://` prefix |
| `GITEA_DOMAIN` · `GITEA_ROOT_URL` | the Gitea domain | `ROOT_URL` is the full URL with a trailing `/` |
| `FLOWER_ID` | flower login ID | Python stacks only |

**3. Generate the web app's domain config** — web stacks get their per-domain config from a generator. Skip this and only the bundled `localhost` config exists, so requests for your web domain hit the catch-all and are cut off with **444**.

```bash
# php example — webroot php_sample, backend php-app:9000
bash config/web-server/nginx/php/nginx_http_conf.sh -w php_sample -p 80 -d web.example.com -a php-app -s 9000
```

Python combinations use a different folder and arguments (gunicorn, for example: `config/web-server/nginx/gunicorn/nginx_http_conf.sh -w django_sample -p 80 -d <domain> -a gunicorn-app -s 8000`). Run with `-h` for the options.

**4. Copy the three proxy configs** — for Plane, Jenkins and Gitea. Skip one and only that service is inactive; the rest start normally.

```bash
P=config/web-server/nginx/php/proxy
cp "$P/plane/plane_proxy.conf.example"     "$P/plane/plane_proxy.conf"       # server_name -> Plane domain
cp "$P/jenkins/jenkins_proxy.conf.example" "$P/jenkins/jenkins_proxy.conf"   # server_name -> Jenkins domain
cp "$P/gitea/gitea_proxy.conf.example"     "$P/gitea/gitea_proxy.conf"       # server_name -> Gitea domain
```

The webserver mounts that folder read-only at `/etc/nginx/proxy.d/<svc>/`, and `nginx.conf` reads it with `include /etc/nginx/proxy.d/*/*.conf;`. **Do not copy into `conf.d`.** The samples contain only an HTTP (80) server block — add the 443 block through the [HTTPS section](#setting-up-https-on-a-web-server).

**5. Start** — one compose file brings everything up.

```bash
cd compose/master_service
docker compose -f docker-compose-php.yml --profile redis up -d --build          # php combination
# or
docker compose -f docker-compose-gunicorn.yml --profile celery up -d --build    # gunicorn combination
```

`--build` rebuilds the web stack images (nginx and app). Add it after an upgrade or a change to a Dockerfile / `uv.lock`. Plane, Jenkins and Gitea pull public images and are never built.

> ⚠️ **The first startup takes several minutes.** `plane-migrator` must finish the DB migration before `plane-api` starts, and `plane-proxy` becomes ready after that. Add `--wait` to block until everything is ready (`--wait --wait-timeout 900`).

**6. Verify**

```bash
docker compose -f docker-compose-php.yml --profile redis ps          # container status
docker compose -f docker-compose-php.yml exec webserver nginx -t     # config check including proxy.d
```

**7. First-time setup per service** — done after startup.

| Service | What to do |
|---|---|
| Plane | Open the domain in a browser and sign up — you become the first user. Instance settings live at `/god-mode/` (see [Plane](#plane)) |
| Jenkins | `docker compose -f docker-compose-php.yml exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword` for the initial password |
| Gitea | `docker compose -f docker-compose-php.yml exec -u git gitea gitea admin user create --username <id> --password '<pw>' --email <mail> --admin` |

### Operating commands

Always pass `-f docker-compose-<stack>.yml` together with the profile you started with.

| Goal | Command |
|---|---|
| Apply a config change only | `docker compose -f … exec webserver nginx -t && … exec webserver nginx -s reload` |
| Restart nginx only | `docker compose -f … restart webserver` |
| Restart everything | `docker compose -f … --profile redis stop` → `… start` |
| Stop everything | `docker compose -f … --profile redis stop` |

> ⚠️ Avoid a whole-project `docker compose restart`. Everything restarts at once, and nginx can come up while the app is down and die once with `[emerg] host not found in upstream`.
> ⚠️ `docker compose down -v` **deletes** the Plane data and the Gitea repositories.

## project_mng_service — standalone installation

### Standalone concurrency rules

- **Run only one standalone service at a time.** `nginx_plane`, `nginx_jenkins` and `gitea` all take host 80/443 (or 2222), and the `plane-*`, `jenkins` and `gitea` container names are the same ones master_service uses. They also cannot run alongside a web stack (`compose/web_service`) or master_service.
- **To run several services at once, use master_service.**
- **Standalone stacks are HTTP only (port 80, no TLS).**
  Port 443 is mapped, but there is no TLS server block for the service — the catch-all `default.conf` merely rejects the handshake (`ssl_reject_handshake on`). In other words **login credentials travel in clear text.**
  For public networks put a TLS terminator (a separate reverse proxy or LB) in front, or use master_service, where TLS can be configured.

**How the standalone nginx is wired**

- The per-service folder `config/web-server/nginx/php/proxy/<svc>/` is mounted read-only at `/etc/nginx/conf.d/`.
- The catch-all `config/web-server/nginx/php/conf.d/default.conf` is mounted over the placeholder `default.conf` inside that folder.
- Without a `<svc>_proxy.conf` copy, nginx answers 444 to every Host and **still starts normally**.

> The placeholder `default.conf` is a read-only mount point. Do not edit or delete it.

---

### Plane

#### What it is

Official site: [Plane]

**In one line**: an open source project management tool that splits work into issues and groups them into cycles. Same family as Jira and Linear, installed and run on your own server.

**Concepts** — nested from the top down.

| Concept | Description |
|---|---|
| Instance | The whole Plane installation. Sign-up policy, authentication and mail are configured in **God Mode** (`/god-mode/`) |
| Workspace | A company or team space. Members and permissions attach here |
| Project | A unit of work inside a workspace, with its own identifier (e.g. `LIVE`) |
| Issue | The actual task, with state, assignee, priority, labels and due date |
| Cycle | Issues grouped by a time box — the equivalent of a sprint |
| Module | Issues grouped by feature or goal, independent of time |

**Main features**

| Feature | Description |
|---|---|
| Multiple views | Switch the same issue list between board (kanban), list, calendar, gantt and spreadsheet |
| Cycles · modules | Run sprints and feature groupings separately, with burndown charts for progress |
| Pages | Documents attached to a project, **edited by several people at once** (handled by `plane-live`) |
| Public sharing | Publish an issue list or page read-only to the outside (handled by `plane-space`) |
| Attachments · images | Stored in the S3-compatible store (`plane-minio`) |
| API | Create and query workspaces, projects and issues over a REST API |
| God Mode | Instance admin screen — sign-up policy, authentication (password, magic link, OAuth), SMTP, file size limits |

**Use it when**

- You want issue and sprint management **on your own server** rather than on a SaaS.
- You want it under the same domain family as Jenkins and Gitea, operated in one place.

**Worth knowing**

- 13 containers in one bundle make it the heaviest service in this repository. The first startup takes several minutes.
- Mail (invitations, notifications) is off by default. Configure SMTP in God Mode to use it.

#### Architecture

13 containers work as one bundle. The definition lives in **one place**, `compose/common/plane-services.yml`, shared by the standalone stack and all five master_service combinations through `include:` (**Docker Compose ≥ 2.20** required).

| Role | Container | Image |
|---|---|---|
| Web UI | `plane-web` | `makeplane/plane-frontend` |
| Public pages | `plane-space` | `makeplane/plane-space` |
| Admin screen (God Mode) | `plane-admin` | `makeplane/plane-admin` |
| API server | `plane-api` | `makeplane/plane-backend` |
| Live collaboration (WebSocket) | `plane-live` | `makeplane/plane-live` |
| Background jobs | `plane-worker` · `plane-beat-worker` | `makeplane/plane-backend` |
| DB migration (one-shot) | `plane-migrator` | `makeplane/plane-backend` |
| Database | `plane-db` | `postgres:15.7-alpine` |
| Cache | `plane-redis` | `valkey/valkey:7.2.11-alpine` |
| Message queue | `plane-mq` | `rabbitmq:3.13.6-management-alpine` |
| Attachment storage | `plane-minio` | `quay.io/minio/minio` (S3 compatible) |
| In-stack proxy | `plane-proxy` | `makeplane/plane-proxy` (Caddy) |

- **No host ports are published.** The front nginx proxies to `plane-proxy`.
- **All data lives in named volumes**: `plane-pgdata` (DB), `plane-uploads` (attachments), `plane-rabbitmq`, `plane-redisdata`, `plane-proxy-*`, `plane-logs-*`. No host folders to create up front.
- Based on the upstream `deployments/cli/community/docker-compose.yml`, adjusted to close the host ports and sit behind the front nginx.

#### Standalone installation and use

1. **Create `.env`** — compose refuses to start while the five secrets (`PLANE_SECRET_KEY`, `PLANE_LIVE_SERVER_SECRET_KEY`, `PLANE_DB_PASSWORD`, `PLANE_MQ_PASSWORD`, `PLANE_MINIO_PASSWORD`) are empty. The helper walks the `include:`d definition and fills them.

   ```bash
   D=compose/project_mng_service/nginx_plane
   cp "$D/.env-example" "$D/.env"
   bash -c ". script/lib/django_secrets.sh && ensure_env_secrets $D/.env"
   ```

2. **Enter the domain** — set `PLANE_DOMAIN`, `PLANE_WEB_URL` and `PLANE_CORS_ALLOWED_ORIGINS` to the **same domain** yourself (the helper does not fill these). They must also match `server_name` in the proxy conf for login, the API and live collaboration to work. When serving over HTTPS, write the two URLs with `https://`.

3. **Prepare the proxy conf** (from the repository root)

   ```bash
   P=config/web-server/nginx/php/proxy/plane
   cp "$P/plane_proxy.conf.example" "$P/plane_proxy.conf"   # set server_name to your domain
   ```

4. **Start**

   ```bash
   cd compose/project_mng_service/nginx_plane
   docker compose up -d --build
   ```

   The first startup takes **several minutes**. `plane-migrator` must finish the DB migration before `plane-api` starts; the rest follow.

5. **First account** — open the domain in a browser and sign up; that account becomes the first user of the instance. Instance administration is at `/god-mode/` on the same domain. To block outside sign-ups, turn sign-up off in God Mode's Authentication settings.

6. **Backup**

   ```bash
   D=compose/project_mng_service/nginx_plane   # master: D=compose/master_service + -f docker-compose-<stack>.yml
   (cd "$D" && docker compose exec -T plane-db pg_dump -U plane -d plane) | gzip > ~/plane-db-$(date +%F).sql.gz
   chmod 600 ~/plane-db-*.sql.gz               # it contains user and workspace data
   ```

   Attachments live in the `plane-uploads` volume: `docker run --rm -v plane-uploads:/d -v "$HOME":/b alpine tar czf /b/plane-uploads.tgz -C /d .`

> ⚠️ **Changing a secret breaks the existing database.** `PLANE_DB_PASSWORD` is frozen as the PostgreSQL password at the moment the `plane-pgdata` volume is created. Recreate `.env` with a different value and `plane-migrator` fails with `FATAL: password authentication failed for user "plane"`, and none of the containers behind it start.
> To change it, change the database too (`docker compose exec plane-db psql -U plane -c "ALTER USER plane PASSWORD '<new value>';"`), or discard the data and recreate the volume (`docker compose down -v`).

See the [Plane documentation][Plane docs] for more.

---

### Jenkins

#### What it is

Official site: [Jenkins]

**In one line**: a CI/CD server that runs the jobs you define automatically. It repeats "build, test and deploy when code lands" without anyone doing it by hand.

**Concepts**

| Concept | Description |
|---|---|
| Job / Pipeline | The definition of the work to run. The modern style writes the pipeline into a `Jenkinsfile` in the repository |
| Build | One execution of a job, with a number, logs and artifacts |
| Trigger | What starts it — a git push webhook, a schedule (cron), a manual run, or another job succeeding |
| Agent / Node | The executor that actually runs the work. By default that is Jenkins itself (the built-in node) |
| Credentials | Repository keys, registry passwords and the like, stored encrypted and injected into jobs |
| Plugin | Extensions. Git, Docker and Slack integration — most features are plugins |

**Main features**

| Feature | Description |
|---|---|
| Automatic build · test | Runs on every push so broken commits surface immediately |
| Pipelines | Splits build → test → image → deploy into stages and shows each stage's result |
| Parallel · distributed runs | Spreads work across several agents |
| Artifact storage | Keeps build outputs and test reports per build number |
| Notifications | Reports failures to mail, Slack and so on (via plugins) |

**How it fits with the rest of this repository**

```
push to Gitea  ->  webhook  ->  Jenkins builds and tests  ->  push image to Harbor
```

**Worth knowing**

- A fresh install has almost no plugins. Install the recommended set in the wizard after the first login.
- Everything lives in the single `jenkins_home` folder (configuration, jobs, build history, plugins). That folder is what you back up.

#### Architecture

| Role | Container | Image |
|---|---|---|
| Jenkins itself | `jenkins` | `jenkins/jenkins:lts-jdk21` |
| Ownership fix (one-shot) | `jenkins-init` | the same image, run as root |

- Data accumulates in the **host directory `jenkins_home`** under the compose folder (unlike Plane and Gitea, this is not a named volume).
- The jenkins image runs as **uid 1000** inside the container. So on every startup `jenkins-init` first sets `jenkins_home` to be owned by 1000. That avoids the `missing rw permissions on JENKINS_HOME` restart loop even when the host account that cloned the repository is not uid 1000. This is why `jenkins_home` appears owned by uid 1000 on the host (master_service behaves the same).
- No host port is published; the front nginx proxies container port 8080.

#### Standalone installation and use

1. **Prepare the proxy conf** (from the repository root)

   ```bash
   P=config/web-server/nginx/php/proxy/jenkins
   cp "$P/jenkins_proxy.conf.example" "$P/jenkins_proxy.conf"   # set server_name
   ```

2. **Create `.env`** — logging settings only, no secrets.

   ```bash
   D=compose/project_mng_service/nginx_jenkins
   cp "$D/.env-example" "$D/.env"
   ```

3. **Start** — add `--build` to rebuild the nginx image after an upgrade or a Dockerfile change.

   ```bash
   cd compose/project_mng_service/nginx_jenkins
   docker compose up -d --build
   ```

4. **First login** — read the initial admin password and enter it in the web UI.

   ```bash
   docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```

See the [Jenkins documentation](https://www.jenkins.io/doc/) for more.

---

### Gitea

#### What it is

Official site: [Gitea]

**In one line**: GitHub for your own server. Repository hosting with a web UI, issues, pull requests and permissions, running in a single container.

**Concepts**

| Concept | Description |
|---|---|
| User · organisation | The repository owner. Create teams under an organisation and grant permissions per team |
| Repository | A git repository plus issues, PRs, wiki and releases |
| Pull request | A merge request for a branch, with review, approval and a merge strategy (merge, squash, rebase) |
| Webhook | Announces events (push, PR, …) to the outside — **this is what triggers Jenkins builds** |
| Access | Both **SSH** (register a public key, then `ssh://git@<domain>:2222/…`) and **HTTP** (password or token) |

**Main features**

| Feature | Description |
|---|---|
| Repository hosting | Private and public, organisation/team permissions, branch protection rules |
| Issues · PRs | Labels, milestones, reviews, inline code comments |
| Webhooks · API | Trigger CI on push; manage repositories, users and issues over a REST API |
| Mirroring | Pull from or push to an external repository on a schedule |
| Releases | Attach binaries to a tag for distribution |
| Actions | GitHub Actions-compatible CI (needs a separate runner — not part of this repository's setup) |

**Compared with GitHub and GitLab**

| | Gitea |
|---|---|
| Weight | One container, a few hundred MB of memory — far lighter than GitLab |
| Database | Embedded SQLite by default; move to PostgreSQL or another external DB as you grow |
| Scope | Centred on repositories, issues and PRs. In this repository CI is a separate tool (Jenkins) |

**Worth knowing**

- Sign-up is **disabled by default** (`GITEA_DISABLE_REGISTRATION=true`). An administrator creates the accounts.
- git over SSH uses host port `2222`. On a cloud host you must open it in the security group too.

#### Architecture

| Role | Container | Image |
|---|---|---|
| Gitea itself | `gitea` | `gitea/gitea` |

- **One container** is all it takes. It uses an embedded SQLite database; to switch to an external DB (PostgreSQL and so on), add `GITEA__database__*` entries to `.env`.
- All data collects in a single named volume, **`gitea-data`** (repositories, database, SSH host keys).
- **HTTP** publishes no host port; the front nginx proxies container port 3000.
- **git over SSH** publishes host port `2222` (`GITEA_SSH_PORT`) directly from the container. Inside the container the image's own OpenSSH serves port 22.
- The install wizard is skipped through `INSTALL_LOCK` — the `.env` values settle the configuration.

#### Standalone installation and use

1. **Create `.env` and enter the domain** — no secrets involved.

   ```bash
   D=compose/project_mng_service/gitea
   cp "$D/.env-example" "$D/.env"      # edit GITEA_DOMAIN · GITEA_ROOT_URL
   ```

   `GITEA_ROOT_URL` is the full URL including the trailing `/` (for example `http://git.example.com/`). Webhooks, clone URLs and OAuth redirects use this value verbatim. Write `https://` when serving over HTTPS.

2. **Prepare the proxy conf** (from the repository root)

   ```bash
   P=config/web-server/nginx/php/proxy/gitea
   cp "$P/gitea_proxy.conf.example" "$P/gitea_proxy.conf"   # set server_name
   ```

3. **Start**

   ```bash
   cd compose/project_mng_service/gitea
   docker compose up -d --build
   ```

4. **Create the administrator** (once)

   ```bash
   docker compose exec -u git gitea gitea admin user create \
     --username <id> --password '<pw>' --email <mail> --admin
   ```

   Under `master_service`, move to `cd compose/master_service` and add `-f docker-compose-<stack>.yml` to the command above.

   The default `GITEA_DISABLE_REGISTRATION=true` means only an administrator can create accounts. Set it to `false` in `.env` to allow self sign-up.

5. **Use it** — create a repository in the web UI, register your SSH public key, then

   ```bash
   git clone ssh://git@<domain>:2222/<account>/<repo>.git    # SSH
   git clone http://<domain>/<account>/<repo>.git             # HTTP (token or password for private repos)
   ```

6. **Backup**

   ```bash
   docker compose exec -u git gitea gitea dump -c /data/gitea/conf/app.ini -f /tmp/gitea-dump.zip
   docker compose cp gitea:/tmp/gitea-dump.zip ~/
   ```

> ⚠️ **Opening SSH 2222 to the outside takes more than a host firewall rule.** Ports published by Docker bypass the host's iptables INPUT chain. On a cloud host you must also add inbound 2222 to the security group (OCI VCN security list, AWS security group and so on). Miss that and the private IP works while the public domain times out.

See the [Gitea documentation][Gitea docs] for more.

---

### Harbor

#### What it is

Official site: [Harbor]

**In one line**: Docker Hub for your own site. Store and distribute container images yourself instead of pushing them outside, with enterprise features such as permissions, scanning and signing.

**Concepts**

| Concept | Description |
|---|---|
| Project | The unit that holds images. Set it public or private and give members roles (developer, master, guest) |
| Repository · tag | Push and pull as `<harbor domain>/<project>/<image>:<tag>` |
| Robot account | A dedicated credential for CI, separate from human accounts and scoped narrowly |
| Replication | Synchronises images with another registry (Docker Hub, another Harbor) on a schedule |
| Retention · GC | Deletes old tags by rule and reclaims disk by collecting unreferenced layers |

**Main features**

| Feature | Description |
|---|---|
| Access control | Per-project permissions, LDAP and OIDC integration |
| Vulnerability scanning | Scans pushed images for CVEs and can block pulls above a severity threshold |
| Image signing | Enforces that only signed images are deployed |
| Audit log | Records who pushed, pulled or deleted what |
| Charts · artifacts | Stores OCI artifacts such as Helm charts besides container images |

**How it fits with the rest of this repository**

```
Jenkins build  ->  docker push <harbor domain>/<project>/<app>:<tag>  ->  pull on the production host
```

**Worth knowing**

- Its installation is **completely different** from the other three services — it uses Harbor's official installer rather than a compose definition (see [Architecture](#architecture-3) below).
- It takes port 80 with its own nginx, so **it is better not to put it on the same host as the other services.**
- The `hostname` in `harbor.yml` **cannot be a loopback IP (`127.0.0.1`).** Harbor's own validation refuses the install with `127.0.0.1 can not be the hostname` — use a domain or a real IP.

#### Architecture

**This differs from the other services in this repository.** No compose definition is provided.

Instead, Harbor's official installer is bundled (`compose/project_mng_service/harbor-v2.0.0/`). The installer generates its own compose file and starts several containers (portal, core, registry, database, job service and so on).

- The installer does not use the `docker compose` plugin — it calls a command literally named **`docker-compose`** (a Compose v1-era script).
- Harbor takes an http port (80 by default) with its own nginx.

#### Installation and use

1. **Provide a legacy `docker-compose` command**

   If `check_dockercompose` in `common.sh` cannot parse `docker-compose --version` as **1.18.0 or newer**, it stops at `[Step 1]`:

   ```
   Need to install docker-compose(1.18.0+) by yourself first and run this script again.
   ```

   Put a Compose v1 binary on the PATH, or create a wrapper that calls the `docker compose` plugin. The version gate only looks at the output of **a command named `docker-compose`**, so a wrapper passes it.

   ```bash
   printf '#!/bin/sh\ncase "$1" in --version|version) exec docker compose version ;; esac\nexec docker compose "$@"\n' \
     | sudo tee /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

   The wrapper rewrites `--version` to `version` because recent Compose plugins print usage instead of a version for `docker compose --version`. This wrapper is what we used to verify http and https installation and startup (portal, API, registry token).

2. **Install** — **run as root** (the same as Harbor's official guidance).

   ```bash
   cd compose/project_mng_service/harbor-v2.0.0
   sudo bash autoinstall.sh        # generate the config and install in one go
   ```

   To split it, run `bash update_harbor_config.sh` to produce `harbor.yml`, then `sudo bash install.sh`. As a normal user it stops at `[Step 4]` with `permission denied`, because `prepare` creates root-owned 0600 files. After installation run `docker-compose down`, `ps` and similar with `sudo` from the same folder.

3. **Inputs** — it asks for the domain, the http port and whether to use https. Paths (ssl, data volume, log) are entered as **plain paths** such as `/data` (no escaping needed).

4. **For https**, place the certificate in this layout before installing.

   ```
   compose/project_mng_service/harbor-v2.0.0/ssl/letsencrypt/live/<domain>/{fullchain,privkey}.pem
   ```

   `autoinstall.sh` copies the contents of `ssl/` under the ssl path you entered (`<ssl path>/letsencrypt/live/<domain>/…`) and writes that domain into the certificate paths in `harbor.yml`. The default path `/etc` needs root.

5. **Execute bits** — only `prepare` is tracked with the execute bit (`100755`). The rest (`install.sh`, `autoinstall.sh`, `update_harbor_config.sh`, `common.sh`) are `100644`, so run them as `bash <script>` as shown above. To use `./install.sh` instead, `chmod +x` that one file.

> ⚠️ **Do not put Harbor on the same host as the other services.** Harbor takes port 80 with its own nginx and collides with this repository's web stack, master_service and standalone proxies. If you must share a host, choose a different http port in `update_harbor_config.sh` and proxy to it from the front nginx (for example a master_service proxy conf).

See the [Harbor 2.0 documentation](https://goharbor.io/docs/2.0.0/) for more.

## Setting up HTTPS on a web server

Bring the site up over HTTP first, obtain a certificate, then switch to the HTTPS config.

> The master_service folder has no `docker-compose.yml`. Add `-f docker-compose-<stack>.yml` to every `docker compose` command below.
> Example: `docker compose -f docker-compose-gunicorn.yml exec webserver bash /script/letsencrypt.sh`

1. **Generate the HTTP config** — run `config/web-server/nginx/<service>/nginx_http_conf.sh`. It writes one config per domain under `conf.d/`, always ending in `_http`.

2. **Start over HTTP** — `docker compose up -d --build` in the compose folder. (`--build` is only needed after an upgrade or a Dockerfile / `uv.lock` change.)

3. **Obtain the certificate** — run `docker compose exec webserver bash /script/letsencrypt.sh` and enter the domain(s) and e-mail address. The ACME webroot is fixed at `/www/certbot` (every generated config and proxy sample serves `/.well-known/acme-challenge/` from there), so it is not asked for.

4. **Switch to the HTTPS config** — run `nginx_https_conf.sh` in the same folder, then delete the `_http` config you used through step 3 from `conf.d/`.

5. **Proxy configs are manual** — there is no generator for the Plane, Jenkins and Gitea proxy configs. After obtaining the certificate, add a `listen 443 ssl` server block to `config/web-server/nginx/php/proxy/<svc>/<svc>_proxy.conf` yourself (see `config/web-server/nginx/php/sample_nginx_https.conf` for the ssl directives).

   Switch the `.env` values that carry URLs to `https://` as well — `PLANE_WEB_URL` and `PLANE_CORS_ALLOWED_ORIGINS` for Plane, `GITEA_ROOT_URL` for Gitea.

6. **Apply** — if you only changed configs, nginx just needs to re-read them.

   ```bash
   docker compose exec webserver nginx -t && docker compose exec webserver nginx -s reload
   ```

   If you changed `.env` values in step 5, recreate only those containers.

   ```bash
   docker compose up -d plane-api plane-web plane-live
   docker compose up -d gitea
   ```

   > ⚠️ Do not use a whole-project `docker compose restart`. Everything restarts at once, and nginx can come up while the app is down and die once with `[emerg] host not found in upstream` (it does restart automatically). Restart everything with `stop` → `start` instead.
   >
   > ⚠️ Do not use `docker compose down -v` either — it deletes the named volumes (Plane data, Gitea repositories and so on).

7. **Renewal cron** — certbot renewal is built into the nginx image (`docker/nginx/Dockerfile` registers it in crontab at build time). You do **not** need a cron job on the host. Check with `docker compose exec webserver crontab -l`.

## Verification status

Last verified 2026-09-30 on an Oracle Cloud aarch64 instance (4 vCPU / 23 GiB, Ubuntu 24.04, Docker 29.7.2, Compose v5.4.0). Every check below used internal paths only — `127.0.0.1` with a Host header, and container-to-container calls.

| Area | Result |
|---|---|
| Web stacks (5) | Each started, HTTP 200, all containers running with zero restarts, celery connected to the authenticated broker and published a task |
| Plane standalone | 13 / 13 — migration finished, 12 containers healthy, `/god-mode/` and `/spaces/` reachable, instance API responding |
| Jenkins standalone | 10 / 10 — reachable through nginx, initial admin password retrievable, `jenkins_home` persisted |
| Gitea standalone | 14 / 14 — admin created, repository created, HTTP clone and push, commits visible on the server |
| Harbor standalone | 11 / 11 — installed, portal and API up, project created, registry token issued |
| All-in-one (master_service, php) | 23 / 23 — **17 containers at once** behind one nginx, split across four domains; `restart webserver` and `stop` → `start` both clean |
| Static checks | `s6_regression`, `repo-steps`, `preflight` all pass |

**Not verified**: reaching **TCP 2222 over the public domain**. The OCI security list has no inbound rule for it, so it is an infrastructure limitation rather than a defect — git over SSH passes over the private IP. Add the inbound rule and re-run `PARTS="php standalone" bash docs/livetest/master-live.sh` to close it.

## Additional development item

- System integration between Jenkins, Gitea and Plane.
- Support docker-swarm, kubernetes
- docker and orchestration monitoring system
- backup and security system
- Support cloud such as AWS, GCM etc

## Community

- **Personal Website** : Owner's personal website is devspoon.com

## Demos

- **youtube** - Preparing

## Partners and Users

- Lim Do-Hyun Owner Developer/project Manager, bluebamus@gmail.com  
  Personal github.io : [bluebamus.github.io]

<!-- Markdown link & img dfn's -->

[devspoon-web]: https://github.com/devspoons/devspoon-web
[devspoon-startup-web]: https://github.com/devspoons/devspoon-startup-web
[Plane]: https://plane.so/
[Plane docs]: https://developers.plane.so/self-hosting/overview
[Jenkins]: https://en.wikipedia.org/wiki/Jenkins_(software)
[Gitea]: https://about.gitea.com/
[Gitea docs]: https://docs.gitea.com/installation/install-with-docker
[Harbor]: https://en.wikipedia.org/wiki/Harbor
[bluebamus.github.io]: https://bluebamus.github.io
