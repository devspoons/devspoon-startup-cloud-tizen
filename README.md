# devspoon-startup-cloud-tizen

Docker-based templates for a web stack (nginx + Django/PHP) and project-management solutions (Plane, Jenkins, Gitea, Harbor). SmartThings/Bixby-integrated application servers are not provided (open-source development support discontinued).

# Discontinuation of support for open source development

This project no longer offers open source development support for startup commercial development and for security reasons.

## Project management solutions

- **[Plane]** : Open source project management software (issues · cycles · modules) to help you work on your project efficiently

- **[Jenkins]** : As one of the CI tools, CI (Continuous Integration) refers to continuous integration, which is an automated process for developers, and new code changes are automatically built and tested regularly to notify developers to solve problems that can occur when multiple developers develop simultaneously. Software that helps secure development stability and reliability

- **[Gitea]** : Lightweight self-hosted git service — web UI, issues, pull requests, and git over SSH/HTTP

- **[Harbor]** : The Private Docker Registry Server for businesses that store and distribute Docker Images

- **[Plane]** : 이슈 · 사이클 · 모듈로 프로젝트를 효율적으로 진행할 수 있도록 지원하는 오픈 소스 프로젝트 관리 소프트웨어

- **[Jenkins(KR)]** : CI 툴 중 하나로 CI (Continuous Integration)는 개발자를 위한 자동화 프로세스인 지속적인 통합을 말하며 새로운 코드 변경 사항들이 정기적으로 자동 빌드 및 테스트되어 개발자에게 알려줌으로 여러명의 개발자가 동시에 개발하며 발생할 수 있는 문제들을 해결하여 개발의 안정성 및 신뢰성을 확보할 수 있도록 지원하는 소프트웨어

- **[Gitea]** : 자체 설치형 경량 git 서비스 — 웹 UI, 이슈, pull request, SSH/HTTP git 접근을 제공하는 git 소프트웨어

- **[Harbor(KR)]** : Docker Image를 저장하고 분배하는 기업용 Private Docker Registry Server

## Features

- **Web stacks ported from devspoon-web** : `compose/web_service/` has five stacks — `nginx_gunicorn`, `nginx_uvicorn`, `nginx_uwsgi`, `nginx_daphne` (Python / Django 6, uv) and `nginx_php` (PHP 8.4 only). See [Web stack & CI](#web-stack--ci).

- **User custom installation support** : You can selectively install only the desired solution at `compose/project_mng_service/<solution>` without having to install all the solutions. Run only one standalone service at a time (see [단독 서비스 동시 기동 규칙](#단독-서비스-동시-기동-규칙)).

- **All-in-one combinations** : To run a web stack together with Plane, Jenkins and Gitea, use one of the five files in `compose/master_service/` (see [master_service](#master_service--웹-스택--plane--jenkins--gitea)).

- **Access web server and project management solutions with one nginx through nginx proxy** : In master_service, one nginx serves the web app and reverse-proxies Plane, Jenkins and Gitea by domain.

  ```
  Example

  test.com -> company website
  plane.test.com -> Plane solution
  jen.test.com -> jenkins solution
  ```

- **Secret separation (`.env-example`)** : Every compose folder ships a tracked `.env-example`, while the actual `.env` is gitignored. Copy it to `.env`, then generate the empty secrets with `script/lib/django_secrets.sh` (`ensure_env_secrets`); never commit the live file. `${VAR:?}` checks in the compose files fail-fast if a required secret is missing.

- **etc** :

  - You can use ssh (port 2222) for git over SSH on Gitea.
  - Harbor is installed with its own installer scripts (see [Harbor](#harbor)).

- **devspoon-web 에서 이식한 웹 스택** : `compose/web_service/` 에 5개 스택이 있습니다 — `nginx_gunicorn`, `nginx_uvicorn`, `nginx_uwsgi`, `nginx_daphne`(Python / Django 6, uv), `nginx_php`(PHP 8.4 전용). [Web stack & CI](#web-stack--ci) 참고.

- **사용자 맞춤식 설치 지원** : 모든 솔루션을 설치할 필요 없이 `compose/project_mng_service/<solution>` 에서 원하는 솔루션만 선택적으로 설치할 수 있습니다. 단독 서비스는 한 번에 하나만 기동합니다([단독 서비스 동시 기동 규칙](#단독-서비스-동시-기동-규칙) 참고).

- **올인원 조합** : 웹 스택과 Plane · Jenkins · Gitea 를 함께 띄우려면 `compose/master_service/` 의 5개 파일 중 하나를 사용하세요([master_service](#master_service--웹-스택--plane--jenkins--gitea) 참고).

- **nginx의 proxy를 통해 하나의 nginx로 웹서버 및 프로젝트 관리 솔루션들에 접근 가능** : master_service 에서 nginx 하나가 웹 앱을 서비스하고 Plane · Jenkins · Gitea 를 도메인별로 리버스 프록시합니다.

  ```
  Example

  test.com -> company website
  plane.test.com -> Plane solution
  jen.test.com -> jenkins solution
  ```

- **비밀값 분리(`.env-example`)** : 모든 compose 폴더에 추적되는 `.env-example` 이 있고 실제 `.env` 는 gitignore 됩니다. `.env` 로 복사한 뒤 `script/lib/django_secrets.sh`(`ensure_env_secrets`)로 빈 비밀값을 생성하고, 실제 파일은 커밋하지 마세요. 필수 비밀값이 없으면 compose 의 `${VAR:?}` 검사가 기동을 거부합니다.

- **기타** :

  - Gitea 의 git over SSH 는 ssh(포트 2222)로 접근합니다.
  - Harbor 는 자체 설치 스크립트로 설치합니다([Harbor](#harbor) 참고).

## considerations

- **Development-oriented docker service** : This open source is designed for focused on development-oriented rather than perfect docker container distribution and is suitable for startups or new service development teams with frequent initial modifications and tests.

- **Orchestration not supported** : In the future, we plan to interoperate with cloud services such as AWS and GCM

- **this open-source considers generic servers that are not support AWS, GCM** : This open source is intended to be installed and operated on a server that is directly operated, and on general server hosting, and plans to integrate with cloud services such as AWS and GCM in the future

- **Requirements** : Docker Engine with the Compose plugin (`docker compose`, **≥ 2.17** for the Python app image builds). Legacy `docker-compose` (v1) commands are not used except by the bundled Harbor installer.

- **개발 중심적 docker 서비스** : 이 오픈소스는 완전한 docker container의 배포가 아닌 개발 중심적으로 설계되었으며 초기 수정과 테스트가 빈번한 스타트업 혹은 신규 서비스 개발팀에게 적합합니다.
- **오케스트레이션 미지원** : 앞으로 AWS, GCM 등의 Cloud 서비스와 연동할 계획이며 이후 오캐스트레이션이 지원될 예정입니다.
- **AWS, GCM 기반이 아닌 일반 서버 고려** : 이 오픈소스는 직접 운용하고있는 서버, 일반적인 서버 호스팅에서 설치하여 운영하는 것을 목적으로 하고 있으며 앞으로 단계적으로 AWS, GCM 등의 Cloud 서비스와 연동할 계획입니다.
- **요구 사항** : Compose 플러그인이 있는 Docker Engine(`docker compose`, Python 앱 이미지 빌드는 **≥ 2.17**). 레거시 `docker-compose`(v1) 명령은 번들된 Harbor 설치 스크립트 외에는 쓰지 않습니다.

## Web stack & CI

웹 스택 서술은 정본 [devspoon-web] README 와 같습니다(검수 완료본을 이 저장소 구조에 맞춤). 모든 명령은 저장소 루트 기준입니다.

### 스택 5종

| 스택 | compose 폴더 | app 서비스 | nginx 설정 폴더 | 프로파일 | 호스트 포트 |
|---|---|---|---|---|---|
| gunicorn | `compose/web_service/nginx_gunicorn` | `gunicorn-app` | `config/web-server/nginx/gunicorn` | `celery` | 80, 443, `127.0.0.1:5555`(flower) |
| uvicorn | `compose/web_service/nginx_uvicorn` | `uvicorn-app` | `config/web-server/nginx/uvicorn` | `celery` | 80, 443, `127.0.0.1:5555` |
| uwsgi | `compose/web_service/nginx_uwsgi` | `uwsgi-app` | `config/web-server/nginx/uwsgi` | `celery` | 80, 443, `127.0.0.1:5555` |
| daphne | `compose/web_service/nginx_daphne` | `daphne-app` | `config/web-server/nginx/gunicorn` (공유) | `celery` | 80, 443, `127.0.0.1:5555` |
| php 8.4 | `compose/web_service/nginx_php` | `php-app` | `config/web-server/nginx/php` | `redis` | 80, 443 |

- Python 스택은 `webserver`·app·`redis` 가 항상 뜨고, `--profile celery` 가 `celery`·`celery-beat`·`flower` 를 더합니다. php 스택은 `webserver`·`php-app` 이 뜨고 `--profile redis` 가 `redis` 를 더합니다.
- 모든 스택이 80/443 을 쓰므로 한 호스트에서 한 스택만 기동합니다.
- 샘플 앱: Python 스택은 `www/django_sample`, php 스택은 `www/php_sample`.

### 1. `.env` 비밀값 생성 (최초 설정 · 업그레이드)

`.env-example` 의 비밀값(Python 스택 `DJANGO_SECRET_KEY` · `REDIS_PASSWORD` · `FLOWER_PWD`, php 스택 `REDIS_PASSWORD`)은 **빈 값**입니다. compose 가 `${VAR:?}` 로 요구하므로 비워 둔 채로는 기동이 거부됩니다. 저장소 루트에서 스택마다 한 번:

```bash
D=compose/web_service/nginx_gunicorn
cp "$D/.env-example" "$D/.env"
bash -c ". script/lib/django_secrets.sh && ensure_env_secrets $D/.env"
```

- 값이 비었거나 옛 `CHANGE_ME_*` 인 비밀 키만 `openssl rand -hex` 무작위 값으로 채웁니다(`DJANGO_SECRET_KEY` 100 hex, `*_KEY_BASE` 128 hex, 그 외 64 hex). 이미 값이 있는 키는 바꾸지 않습니다.
- 같은 폴더의 임시 파일에 쓴 뒤 교체하며, 값을 생성했으면 권한을 600 으로 좁힙니다(더 엄격하면 유지). openssl 이 없거나 실패하면 `FAIL` 로 끝나고 `.env` 내용은 바뀌지 않습니다.
- **비밀이 아닌 자리표시자는 헬퍼가 채우지 않습니다 — 운영 전에 직접 입력하세요**: `FLOWER_ID`(`CHANGE_ME_FLOWER_USER`), master·단독 plane 의 `PLANE_DOMAIN`·`PLANE_WEB_URL`·`PLANE_CORS_ALLOWED_ORIGINS`(proxy conf 의 `server_name` 과 동일), gitea 의 `GITEA_DOMAIN`·`GITEA_ROOT_URL`, `DJANGO_ALLOWED_HOSTS`(도메인 추가).
- 호스트에서 `manage.py` 를 직접 실행할 때만 `www/django_sample` 의 `secrets.json` 이 필요합니다: `bash -c '. script/lib/django_secrets.sh && ensure_django_secrets'` (없을 때만 생성, 600). 컨테이너는 `DJANGO_SECRET_KEY` 환경변수를 씁니다.

> **업그레이드 노트 — 이전 버전에서 쓰던 `.env` 를 유지하는 경우**: 옛 `.env` 에는 `DJANGO_SECRET_KEY` 줄이 없거나 `CHANGE_ME_*` 값이 남아 있을 수 있습니다. 위 헬퍼를 같은 `.env` 에 한 번 실행하면 같은 폴더 `docker-compose*.yml` 이 `:?` 로 요구하는 비밀 키(이름에 SECRET·PASSWORD·PWD 포함 또는 `_KEY_BASE` 로 끝남) 중 없는 키를 끝에 추가하고 `CHANGE_ME_*` 를 교체하며, 기존 값은 보존하고 권한을 600 으로 맞춥니다. `KEY=""` 처럼 따옴표로 둘러싼 빈 값은 채우지 않으니 먼저 `KEY=` 로 고치세요.
>
> 이전 버전은 `compose/web_service/*`·`compose/master_service`·`compose/project_mng_service/*` 의 `.env` 를 git 으로 추적했습니다. 이 버전에서 추적이 해제되어 `git pull` 이 로컬 `.env` 를 지울 수 있으니 **pull 전에 `.env` 를 다른 곳에 복사**해 두세요. 이전에 저장소에 공개됐던 `secrets.json`·`.env` 의 키로 운영 중이라면 새 값으로 교체하세요(세션 무효화).

### 2. 기동

§1 의 `.env` 명령(저장소 루트) 뒤, 저장소 루트에서 스택 폴더로 이동해 기동합니다(`--build` 는 업그레이드나 Dockerfile / `uv.lock` 변경 뒤 이미지를 다시 빌드합니다). 한 호스트에 한 스택만 띄웁니다.

```bash
# gunicorn (저장소 루트에서)
cd compose/web_service/nginx_gunicorn
docker compose up -d --build             # webserver + gunicorn-app + redis
docker compose --profile celery up -d    # + celery · celery-beat · flower
```

uvicorn · uwsgi · daphne 는 gunicorn 과 같은 명령이며 폴더 이름만 `compose/web_service/nginx_uvicorn` · `nginx_uwsgi` · `nginx_daphne` 로 바꿉니다.

```bash
# php (저장소 루트에서)
cd compose/web_service/nginx_php
docker compose up -d --build             # webserver + php-app
docker compose --profile redis up -d     # + redis
```

- **기동 순서 — app 이 DB 를 초기화한 뒤 celery · beat**: 각 스택의 app 서비스만 서버 기동 전에 `uv sync` 후 DB 를 1회 초기화합니다(`manage.py` 가 있으면 `python manage.py migrate --noinput`, 없으면 프로젝트의 `prestart.sh`). `celery` · `celery-beat` 는 `depends_on: <app>: condition: service_healthy` 라 app 이 healthy 가 된 뒤 기동합니다 — 동시 migrate 경쟁이 없습니다.
- **Flower** 는 **`127.0.0.1:5555` 에만 바인드**됩니다. 원격 접근은 SSH 터널: `ssh -L 5555:127.0.0.1:5555 <host>` 후 로컬 브라우저에서 `http://127.0.0.1:5555`.
- `DJANGO_DEBUG`(기본 `0`) · `DJANGO_ALLOWED_HOSTS` 를 `.env` 로 제어하며 app · celery · beat 에 전달됩니다. `DJANGO_DEBUG=1` 은 로컬 개발에서만 쓰세요.
- 컨테이너는 `docker compose stop` / `start` / `restart` 로 운영합니다. 프로필 서비스까지 대상이면 기동과 같은 프로필을 붙입니다(`docker compose --profile celery stop`, php 는 `--profile redis stop`) — 프로필 없는 `stop` 은 celery · celery-beat · flower(php 는 redis) 컨테이너를 남깁니다.

### 3. SQLite 데이터 위치 — named volume `/data`

Python 스택(gunicorn · uvicorn · uwsgi · daphne)의 SQLite 는 호스트 `www/<PROJECT_DIR>/db.sqlite3` 가 아니라 compose named volume `app-data` 의 **`/data/<PROJECT_DIR>.sqlite3`** (`SQLITE_PATH` 환경변수)에 저장됩니다. 컨테이너는 이 볼륨과 로그 디렉터리만 www-data 소유로 맞추고, 호스트 소스 트리(`/www`)의 소유권은 바꾸지 않습니다. `SQLITE_PATH` 가 없는 호스트 `manage.py` 실행은 여전히 `www/<PROJECT_DIR>/db.sqlite3` 를 씁니다.

**기존 DB 이관** (호스트 `db.sqlite3` 를 계속 쓰려면 — gunicorn 스택 예, celery 프로파일은 이관 후 기동):

```bash
cd compose/web_service/nginx_gunicorn
docker compose up -d --build  # app-data 볼륨 생성 (빈 DB 로 migrate 됨)
docker compose cp ../../../www/django_sample/db.sqlite3 gunicorn-app:/data/django_sample.sqlite3
docker compose exec gunicorn-app chown www-data:www-data /data/django_sample.sqlite3
docker compose restart gunicorn-app   # 기동 명령이 다시 돌며 이관한 DB 에 미적용 migrate 반영 (app 만 — 전체 restart 는 nginx 기동 경합)
```

> ⚠️ **`docker compose down -v` 는 `app-data` 볼륨, 즉 SQLite DB 를 삭제합니다.** 컨테이너만 내리려면 `docker compose stop` 을 쓰세요 (`down` 은 비권장, 특히 `-v`; 프로필 서비스는 §2 처럼 `--profile` 을 붙임). 백업: `docker compose cp gunicorn-app:/data/django_sample.sqlite3 ./backup.sqlite3`. master_service 의 Plane 데이터 볼륨(`plane-pgdata`·`plane-uploads` 등)과 Gitea 저장소 볼륨(`gitea-data`)도 `-v` 로 삭제됩니다.

### 4. 이미지 이름 · 빌드 · uv

- 이미지 이름은 `${IMAGE_NAMESPACE:-devspoon}-nginx:latest` 형식입니다(`-py-app:latest`, `-uwsgi-app:latest`, `-php-app:8.4`). 기본값이면 `devspoon-*` 태그이고, 검증기·`verify-ngxblocker.sh` 는 `IMAGE_NAMESPACE=devspoon-it`, run-ci 빌드 단계(`s2_build.sh`)는 `devspoon-test/*` 태그로 빌드해 운영 태그를 덮어쓰지 않습니다.
- 앱 이미지(`py-app` · `uwsgi-app`)의 사전 설치 패키지는 `www/django_sample/uv.lock` 에서 도출됩니다. compose 는 `build.additional_contexts: lock: ../../../www/django_sample` 로 이를 자동 전달하므로 **Docker Compose ≥ 2.17** 이 필요합니다 (`docker compose version`).
- Compose 가 2.17 미만이거나 `docker build` 를 직접 쓸 때는 추가 빌드 컨텍스트를 명시합니다(저장소 루트, BuildKit):

  ```bash
  docker build --build-context lock=www/django_sample -t devspoon-py-app:latest docker/gunicorn/
  docker build --build-context lock=www/django_sample -t devspoon-uwsgi-app:latest docker/uwsgi/
  ```

  빠뜨리면 빌드가 `"/pyproject.toml": not found` 로 실패합니다.
- **uv**: `www/django_sample` 의 의존성은 `pyproject.toml` · `uv.lock` 으로 관리합니다. 컨테이너는 가상환경 없이 시스템 Python 에 설치하며(`UV_PROJECT_ENVIRONMENT=/usr/local`), 기동 명령이 `uv sync --inexact --extra <stack> --extra celery` 를 실행합니다. 같은 스택의 app · celery · celery-beat 는 같은 extras 로 sync 합니다. 의존성 추가는 호스트에서 `cd www/django_sample && uv add <pkg>` 후 `uv.lock` 을 커밋하고 스택 폴더에서 `docker compose --profile celery stop && docker compose up -d --build` 로 재기동하고, celery 사용 시 `docker compose --profile celery up -d` 로 celery · celery-beat 도 다시 올립니다(앱 이미지 사전 설치도 `uv.lock` 에서 도출; celery 는 `build:` 없이 같은 이미지를 참조하므로 프로필 없는 `up --build` 만으로는 옛 이미지·옛 의존성으로 계속 동작).

### 5. nginx · php 설정

- nginx conf 생성기: `config/web-server/nginx/<gunicorn|uvicorn|uwsgi|php>/` 의 `nginx_http_conf.sh` · `nginx_https_conf.sh` 가 `sample_nginx_http(s).conf` 로 `conf.d/` 에 도메인별 conf 를 만듭니다(`-h` 로 옵션 확인). daphne 는 gunicorn 폴더를 씁니다.
- nginx 기동 훅: 이미지의 `/docker-entrypoint.d/30-wait-upstreams.sh` 가 conf 의 upstream(앱 컨테이너) 이름이 해석될 때까지 최대 `NGINX_UPSTREAM_WAIT` 초(기본 30, `0` 이면 비활성, webserver `environment` 로 조정) 기다린 뒤 nginx 를 띄웁니다 — 재부팅·`start` 처럼 app 보다 webserver 가 먼저 뜰 때 `[emerg] host not found in upstream` 으로 죽는 것을 막습니다. 전체 `docker compose restart` 는 동시 재시작이라 훅으로도 완전히 막히지 않으니 conf 반영은 `nginx -s reload`, 전체 재기동은 `stop` → `start` 를 쓰세요.
- php-fpm pool 은 **`config/app-server/php/pool.d/www.conf` 를 편집**합니다. compose 는 `www.conf`(`/usr/local/etc/php-fpm.d/www.conf`)와 `config/app-server/php/php_ini/php.ini` 만 단일 파일로 읽기 전용 마운트하므로, `php_conf.sh` 가 `pool.d/` 에 만드는 `<DOMAIN>_php.conf` 는 로드되지 않습니다.

### 6. CI — `script/ci/run-ci.sh`

`bash script/ci/run-ci.sh` 가 11단계를 순서대로 실행합니다: preflight → prereq·로그 디렉터리 → nginx conf 생성기 → compose 검증 → 저장소 고유 검사(`script/ci/repo-steps.sh`) → 이미지 빌드 → 정적 회귀(s6) → healthcheck → 스택 매트릭스(gunicorn · uvicorn · uwsgi · daphne · php 실기동) → 샘플 프로젝트 → 스크립트 로그.

- 실제 컨테이너를 띄우므로 호스트 80/443/5555 가 비어 있어야 합니다. 필요 도구: docker(Compose ≥ 2.17), uv, jq, curl, openssl, php-cli.
- GitHub Actions(`.github/workflows/test.yml`)는 같은 스크립트를 실행합니다. 알림은 선택 — 저장소 secrets `SLACK_WEBHOOK_URL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` 가 없으면 해당 알림을 건너뜁니다. 업로드 로그(`log/ci`, `log/test_run`)는 `script/lib/mask_secrets.sh` 로 비밀값을 마스킹한 뒤 올립니다.

## master_service — 웹 스택 + Plane · Jenkins · Gitea

`compose/master_service/` 의 5조합은 한 nginx(`webserver`) 뒤에 웹 스택과 Plane · Jenkins · Gitea 를 함께 띄웁니다. `.env` 하나(`compose/master_service/.env-example`)를 공유하고, Plane · Gitea 서비스 정의는 단독 스택과 같은 `compose/common/{plane-services,gitea-service}.yml` 을 `include:` 합니다(**Docker Compose ≥ 2.20**).

| 파일 | 웹 스택 | 프로파일 |
|---|---|---|
| `docker-compose-gunicorn.yml` | gunicorn | `celery` |
| `docker-compose-uvicorn.yml` | uvicorn | `celery` |
| `docker-compose-uwsgi.yml` | uwsgi | `celery` |
| `docker-compose-daphne.yml` | daphne | `celery` |
| `docker-compose-php.yml` | php 8.4 | `redis` (celery 없음) |

모든 조합에 **Plane**(`makeplane/plane-*`, 앱·DB·큐·오브젝트 저장소·내부 프록시 13 서비스) · `jenkins`(`jenkins/jenkins:lts-jdk21`) · **Gitea**(`gitea/gitea`, 호스트 2222 = git over SSH) 가 포함됩니다.

1. **Plane · Gitea 는 사전 준비가 없습니다** — 관리자 계정은 기동 뒤에 만듭니다([Plane](#plane) 6 · [Gitea](#gitea) 4단계).
2. **`.env` 생성** — Plane 비밀 키 5종도 헬퍼가 생성합니다(`include:` 한 `compose/common/plane-services.yml` 의 `${KEY:?}` 까지 훑습니다).

   ```bash
   D=compose/master_service
   cp "$D/.env-example" "$D/.env"
   bash -c ". script/lib/django_secrets.sh && ensure_env_secrets $D/.env"
   ```

   이어서 `PLANE_DOMAIN` · `PLANE_WEB_URL` · `PLANE_CORS_ALLOWED_ORIGINS` · `GITEA_DOMAIN` · `GITEA_ROOT_URL` · `FLOWER_ID` 자리표시자를 직접 입력합니다.
3. **proxy 샘플 복사** — webserver 가 `config/web-server/nginx/php/proxy/<svc>/` 를 `/etc/nginx/proxy.d/<svc>/` 로 읽기 전용 마운트하고, `nginx.conf` 가 `include /etc/nginx/proxy.d/*/*.conf;` 로 읽습니다. `conf.d` 로 복사하지 않습니다.

   ```bash
   P=config/web-server/nginx/php/proxy
   cp "$P/plane/plane_proxy.conf.example" "$P/plane/plane_proxy.conf"                           # server_name 수정
   cp "$P/gitea/gitea_proxy.conf.example" "$P/gitea/gitea_proxy.conf"                           # server_name 수정
   cp "$P/jenkins/jenkins_proxy.conf.example" "$P/jenkins/jenkins_proxy.conf"                   # server_name 수정
   ```

   복사본(`*_proxy.conf`, gitignore)이 없으면 주석뿐인 `default.conf` 만 읽혀 해당 proxy 가 비활성입니다. 샘플은 HTTP(80) 서버 블록만 있으므로 TLS 는 [HTTPS 절](#setting-up-https-on-a-web-server)로 443 블록을 추가합니다.
4. **기동** — 저장소 루트에서 스택 폴더로 이동합니다(`--build` 는 업그레이드나 Dockerfile / `uv.lock` 변경 뒤 이미지를 다시 빌드합니다).

   ```bash
   cd compose/master_service
   docker compose -f docker-compose-gunicorn.yml --profile celery up -d --build
   docker compose -f docker-compose-php.yml --profile redis up -d --build      # php 조합
   ```

   > ⚠️ **첫 기동은 Plane 마이그레이션 때문에 수 분 걸립니다**: `plane-migrator` 가 성공으로 끝난 뒤 `plane-api` 가 뜨고, 그 뒤에 `plane-proxy` 가 준비됩니다. Plane · Gitea 데이터는 named volume 이므로 호스트 폴더를 만들 필요가 없습니다(`docker compose down -v` 는 그 볼륨을 지웁니다).

## project_mng_service — 단독 서비스

### 단독 서비스 동시 기동 규칙

- **단독 서비스는 한 번에 하나만 기동합니다.** `nginx_plane` · `nginx_jenkins` · `gitea` 가 모두 호스트 80/443(또는 2222)을 쓰고, `plane-*` · `jenkins` · `gitea` 컨테이너 이름이 master_service 와 같습니다. 웹 스택(`compose/web_service`)·master_service 와도 동시에 띄울 수 없습니다.
- **여러 서비스를 동시에 운영하려면 master_service 를 쓰세요.**
- **단독 proxy 스택(`nginx_plane` · `nginx_jenkins` · `gitea`)은 HTTP 전용입니다(80, TLS 없음).** 443 은 매핑돼 있지만 catch-all `default.conf` 가 TLS 핸드셰이크를 거부(`ssl_reject_handshake on`)할 뿐 서비스용 TLS 서버 블록이 없어, 로그인 자격증명이 80 으로 평문 전송됩니다. 공개망 운영은 앞단 TLS 종단(별도 리버스 프록시·LB) 뒤에 두거나, TLS 를 구성할 수 있는 master_service 를 쓰세요.

단독 proxy 스택 구조: nginx 가 `config/web-server/nginx/php/proxy/<svc>/` 서비스별 폴더를 `/etc/nginx/conf.d/` 로 읽기 전용 마운트하고, 그 폴더의 자리표시자 `default.conf` 자리에 catch-all `config/web-server/nginx/php/conf.d/default.conf` 를 덮어 마운트합니다. 복사본 `<svc>_proxy.conf` 가 없으면 모든 Host 에 444 로 응답하며 정상 기동합니다. 자리표시자 `default.conf` 는 편집·삭제하지 마세요(읽기 전용 마운트 지점).

### Plane

1. `.env` 생성 — Plane 비밀 키 5종(`PLANE_SECRET_KEY` · `PLANE_LIVE_SERVER_SECRET_KEY` · `PLANE_DB_PASSWORD` · `PLANE_MQ_PASSWORD` · `PLANE_MINIO_PASSWORD`)이 비어 있으면 compose 가 기동을 거부합니다. 헬퍼가 `include:` 한 `compose/common/plane-services.yml` 의 키까지 찾아 채웁니다.

   ```bash
   D=compose/project_mng_service/nginx_plane
   cp "$D/.env-example" "$D/.env"
   bash -c ". script/lib/django_secrets.sh && ensure_env_secrets $D/.env"
   ```

2. 도메인 3개를 **같은 값**으로 직접 입력합니다(헬퍼가 채우지 않는 자리표시자): `PLANE_DOMAIN` · `PLANE_WEB_URL` · `PLANE_CORS_ALLOWED_ORIGINS`. proxy conf 의 `server_name` 과도 같아야 로그인·API·실시간 협업(WebSocket)이 모두 동작합니다. HTTPS 로 서비스하면 `PLANE_WEB_URL` · `PLANE_CORS_ALLOWED_ORIGINS` 를 `https://` 로 적습니다.

3. proxy 샘플 복사(저장소 루트): `P=config/web-server/nginx/php/proxy/plane; cp "$P/plane_proxy.conf.example" "$P/plane_proxy.conf"` 후 `server_name` 수정.

4. 기동(저장소 루트에서): `cd compose/project_mng_service/nginx_plane && docker compose up -d` (HTTP 전용 — 위 단독 서비스 규칙 참조). 첫 기동은 `plane-migrator` 가 DB 마이그레이션을 마친 뒤 `plane-api` 가 뜨므로 수 분 걸립니다.

5. 구성: 앱(`plane-web` · `plane-space` · `plane-admin` · `plane-api` · `plane-live` · `plane-worker` · `plane-beat-worker` · 1회성 `plane-migrator`) + 데이터(`plane-db` PostgreSQL 15 · `plane-redis` Valkey · `plane-mq` RabbitMQ · `plane-minio` S3 호환 저장소) + 스택 내부 프록시(`plane-proxy`, Caddy). 정의는 `compose/common/plane-services.yml` 한 곳에 있고 master_service 5조합이 같은 파일을 `include:` 합니다 — **Docker Compose ≥ 2.20** 이 필요합니다.

6. 첫 계정: 브라우저로 도메인에 접속해 가입하면 그 계정이 인스턴스 첫 사용자가 됩니다. 인스턴스 관리(`/god-mode`)는 `plane-admin` 이 담당하며 같은 도메인의 `/god-mode/` 경로로 열립니다. 외부 가입을 막으려면 God Mode 의 Authentication 설정에서 sign-up 을 끕니다.

7. > ⚠️ **비밀값을 바꾸면 기존 DB 볼륨과 어긋납니다**: `PLANE_DB_PASSWORD` 는 `plane-pgdata` 볼륨이 처음 만들어질 때의 PostgreSQL 사용자 비밀번호로 굳습니다. `.env` 만 새로 만들어(또는 `ensure_env_secrets` 를 빈 `.env` 에 다시 돌려) 값이 바뀌면 `plane-migrator` 가
   > `FATAL: password authentication failed for user "plane"` 으로 실패하고 뒤따르는 앱 컨테이너가 전부 기동하지 못합니다. 값을 바꿀 때는 DB 안의 비밀번호도 함께 바꾸거나(`docker compose exec plane-db psql -U plane -c "ALTER USER plane PASSWORD '<새 값>';"`), 데이터를 버려도 되면 볼륨을 새로 만드세요(`docker compose down -v`).

8. 데이터는 전부 named volume 입니다(`plane-pgdata` · `plane-uploads` · `plane-rabbitmq` · `plane-redisdata` · `plane-proxy-*` · `plane-logs-*`). 호스트 폴더 소유권 문제가 없는 대신 **`docker compose down -v` 를 쓰면 전부 삭제**됩니다 — 컨테이너만 내릴 때는 `stop` 을 쓰세요. 논리 백업 예:

   ```bash
   D=compose/project_mng_service/nginx_plane   # master: D=compose/master_service, 아래 명령에 -f docker-compose-<stack>.yml 추가
   (cd "$D" && docker compose exec -T plane-db pg_dump -U plane -d plane) | gzip > ~/plane-db-$(date +%F).sql.gz
   chmod 600 ~/plane-db-*.sql.gz   # 사용자·워크스페이스 데이터가 들어 있다
   ```

   첨부 파일은 `plane-minio` 볼륨(`plane-uploads`)에 있습니다: `docker run --rm -v plane-uploads:/d -v "$HOME":/b alpine tar czf /b/plane-uploads.tgz -C /d .`

9. 더 자세한 내용은 [Plane 공식 문서][Plane docs] 참고. 이 저장소의 정의는 업스트림 `deployments/cli/community/docker-compose.yml` 을 기준으로, 호스트 포트를 열지 않고 앞단 nginx 뒤에 두도록 조정한 것입니다.

---

### Jenkins

1. proxy 샘플 복사(저장소 루트): `P=config/web-server/nginx/php/proxy/jenkins; cp "$P/jenkins_proxy.conf.example" "$P/jenkins_proxy.conf"` 후 `server_name` 수정.
2. `.env` 생성(저장소 루트): `D=compose/project_mng_service/nginx_jenkins; cp "$D/.env-example" "$D/.env"` (로그 설정만, 비밀값 없음).
3. 기동(저장소 루트에서, `--build` 는 업그레이드나 Dockerfile 변경 뒤 nginx 이미지 재빌드): `cd compose/project_mng_service/nginx_jenkins && docker compose up -d --build` — 이미지 `jenkins/jenkins:lts-jdk21`, 데이터는 같은 폴더 `jenkins_home`(HTTP 전용 — 위 규칙 참조). jenkins 이미지는 uid 1000 으로 동작하므로, 기동 때마다 1회성 `jenkins-init` 서비스가 같은 이미지를 root 로 실행해 `jenkins_home` 폴더 소유자를 1000 으로 맞춘 뒤 jenkins 가 뜹니다(클론한 호스트 사용자 uid 가 1000 이 아니어도 `missing rw permissions on JENKINS_HOME` 재시작 루프가 생기지 않음 — master_service 도 동일). 그래서 이 폴더는 호스트에서 uid 1000 소유로 보입니다.
4. There are advanced information in [Jenkins Official User Documentation](https://www.jenkins.io/doc/)

---

### Gitea

1. `.env` 생성 후 도메인 입력(비밀값 없음):

   ```bash
   D=compose/project_mng_service/gitea
   cp "$D/.env-example" "$D/.env"      # GITEA_DOMAIN · GITEA_ROOT_URL 을 실제 도메인으로 수정
   ```

   `GITEA_ROOT_URL` 은 끝에 `/` 를 포함한 전체 URL 입니다(예: `http://git.example.com/`). HTTPS 로 서비스하면 `https://` 로 적습니다 — 웹훅·클론 URL·OAuth 리다이렉트가 이 값을 씁니다.

2. proxy 샘플 복사(저장소 루트): `P=config/web-server/nginx/php/proxy/gitea; cp "$P/gitea_proxy.conf.example" "$P/gitea_proxy.conf"` 후 `server_name` 수정.

3. 기동(저장소 루트에서): `cd compose/project_mng_service/gitea && docker compose up -d` — HTTP 는 앞단 nginx 가 프록시하고, git over SSH 는 컨테이너가 호스트 `2222`(`GITEA_SSH_PORT`)를 직접 게시합니다. 방화벽·보안 그룹에서 2222 를 열어야 외부에서 SSH 클론이 됩니다 — Docker 가 게시한 포트는 호스트 iptables 의 INPUT 체인을 거치지 않으므로, 호스트 방화벽만 열고 **클라우드 보안 그룹**(예: OCI VCN 보안 목록 · AWS 보안 그룹)을 빠뜨리면 `10.x` 사설 IP 로는 되는데 공인 도메인으로는 timeout 이 납니다.

4. 관리자 계정 생성(최초 1회, 설치 화면은 `INSTALL_LOCK` 으로 건너뜁니다):

   ```bash
   cd compose/project_mng_service/gitea      # master: cd compose/master_service, 아래 명령에 -f docker-compose-<stack>.yml 추가
   docker compose exec -u git gitea gitea admin user create \
     --username <id> --password '<pw>' --email <mail> --admin
   ```

   기본값은 `GITEA_DISABLE_REGISTRATION=true`(관리자만 계정 생성)입니다. 자체 가입을 허용하려면 `.env` 에서 `false` 로 바꾸세요.

5. 사용: 웹 UI 에서 저장소를 만들고 SSH 공개키를 등록한 뒤

   ```bash
   git clone ssh://git@<도메인>:2222/<계정>/<저장소>.git      # SSH
   git clone http://<도메인>/<계정>/<저장소>.git               # HTTP(개인 저장소는 토큰·비밀번호 인증)
   ```

6. 데이터는 named volume `gitea-data`(저장소·SQLite DB·SSH 호스트키) 하나에 모입니다. `docker compose down -v` 는 이 볼륨을 지웁니다. 백업: `docker compose exec -u git gitea gitea dump -c /data/gitea/conf/app.ini -f /tmp/gitea-dump.zip && docker compose cp gitea:/tmp/gitea-dump.zip ~/`. 외부 DB(PostgreSQL 등)를 쓰려면 `.env` 에 `GITEA__database__*` 를 추가합니다.

7. 더 자세한 내용은 [Gitea 공식 문서][Gitea docs] 참고.

---

### Harbor

1. 저장소에 있던 Compose v1 설치 스크립트는 삭제됐습니다. 번들된 Harbor v2.0.0 installer(`install.sh` · `common.sh`)는 `docker compose` 플러그인을 쓰지 않고 **`docker-compose` 라는 이름의 명령**을 직접 호출합니다. `common.sh` 의 `check_dockercompose` 가 `docker-compose --version` 을 실행해 **1.18.0 이상**으로 파싱하지 못하면 `[Step 1]` 에서 `Need to install docker-compose(1.18.0+) by yourself first and run this script again.` 를 출력하고 **exit 1** 로 중단하므로, 레거시 Compose v1(1.18.0+) 바이너리를 운영자가 직접 PATH 에 준비합니다. (버전 판정은 이름이 `docker-compose` 인 명령의 출력만 봅니다 — v2 형식 문자열을 내는 같은 이름의 실행 파일도 이 관문을 통과합니다. `docker compose` 플러그인을 부르는 래퍼 `printf '#!/bin/sh\ncase "$1" in --version|version) exec docker compose version ;; esac\nexec docker compose "$@"\n' | sudo tee /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose` 로 http·https 설치와 기동(포털·API·레지스트리 토큰)을 검증했습니다 — 최근 Compose 플러그인은 `docker compose --version` 에 버전이 아니라 사용법을 출력하므로 래퍼가 `version` 으로 바꿔 전달해야 합니다.)
2. `install.sh` 는 내부에서 `./prepare` 를 **직접 실행**하므로, `prepare` 한 파일만 저장소에 **실행 권한(`100755`)으로 추적**됩니다 — 별도 `chmod` 없이 `[Step 3]` 을 통과합니다. 나머지 스크립트(`install.sh` · `autoinstall.sh` · `update_harbor_config.sh` · `common.sh`)는 `100644` 이며 실행 비트가 필요 없습니다: `common.sh` 는 `install.sh` 가 `source` 하고, 나머지는 아래 3항처럼 **`bash <스크립트>` 형태로 실행**합니다(`autoinstall.sh` 도 내부에서 `bash install.sh` 로 호출합니다). `./install.sh` 처럼 직접 실행하고 싶다면 그 파일에만 `chmod +x` 하세요.
3. `bash update_harbor_config.sh` 가 도메인·http 포트·https 여부를 입력받아 `harbor.yml` 을 만들고, `bash install.sh` 로 설치합니다. `bash autoinstall.sh` 는 두 단계를 한 번에 실행합니다. 입력하는 경로(ssl·data volume·log)는 `/data` 처럼 일반 경로 그대로 입력합니다(이스케이프 불필요, 예전 `\/data` 입력도 허용). https 를 쓰려면 설치 전에 `compose/project_mng_service/harbor-v2.0.0/ssl/letsencrypt/live/<도메인>/{fullchain,privkey}.pem` 구조로 인증서를 둡니다 — `autoinstall.sh` 가 `ssl/` 의 내용을 입력한 ssl path 아래로 복사하고(`<ssl path>/letsencrypt/live/<도메인>/…`, 기본 `/etc` 는 root 권한 필요), `harbor.yml` 인증서 경로에 입력 도메인을 넣습니다. `install.sh` 재실행 시 기존 harbor 컨테이너를 `down -v` 로 내린 뒤 다시 올립니다. **설치는 root 로 실행합니다**(`sudo bash autoinstall.sh` / `sudo bash install.sh`, Harbor 공식 안내와 동일): `prepare` 가 `common/config/*/env` 를 root 소유 600 으로 만들기 때문에 일반 사용자로 실행하면 `[Step 4]` 에서 `open …/common/config/jobservice/env: permission denied` 로 멈춥니다. 이후 `docker-compose` 명령(`down`·`ps` 등)도 같은 폴더에서 `sudo` 로 실행합니다.
4. **공존**: Harbor 는 자체 nginx 로 http 포트(기본 80)를 씁니다. 이 저장소의 웹 스택·master_service·단독 proxy 와 같은 호스트라면 **별도 호스트를 권장**하고, 같은 호스트라면 `update_harbor_config.sh` 에서 다른 http 포트를 지정한 뒤 앞단 nginx(예: master_service proxy conf)에서 그 포트로 프록시하세요.
5. There are advanced information in [Harbor 2.0 Documentation](https://goharbor.io/docs/2.0.0/)

## Setting up HTTPS on a web server

- This step requires running http nginx server
- master_service 는 compose 폴더에 `docker-compose.yml` 이 없으므로 아래 모든 `docker compose` 명령에 `-f docker-compose-<stack>.yml` 을 붙입니다(예: `docker compose -f docker-compose-gunicorn.yml exec webserver bash /script/letsencrypt.sh`).

  1. 웹 스택: Run nginx_http_conf.sh located in config/web-server/nginx/<service>. Create a conf file for each domain under config/web-server/nginx/<service>/conf.d/. Generated filenames always end with "_http".

  2. Start the stack with `docker compose up -d --build` in its compose folder (--build rebuilds the images after an upgrade or a Dockerfile / uv.lock change). This will run the default nginx using http.

  3. The script/letsencrypt.sh shell script file is linked per volume (`/script`). Run `docker compose exec webserver bash /script/letsencrypt.sh` and enter the domain(s) and email. The ACME webroot is fixed to /www/certbot (every generated conf and proxy sample serves /.well-known/acme-challenge/ from it), so there is no webroot input.

  4. Now create a conf file for https: run nginx_https_conf.sh located in config/web-server/nginx/<service>, then remove the http conf file from config/web-server/nginx/<service>/conf.d/.

  5. master_service 의 plane · jenkins · gitea proxy 는 생성기가 없습니다 — 인증서 발급 후 `config/web-server/nginx/php/proxy/<svc>/<svc>_proxy.conf` 에 `listen 443 ssl` 서버 블록을 직접 추가합니다(`config/web-server/nginx/php/sample_nginx_https.conf` 의 ssl 지시어 참고). Plane 은 `.env` 의 `PLANE_WEB_URL`·`PLANE_CORS_ALLOWED_ORIGINS` 를, Gitea 는 `GITEA_ROOT_URL` 을 `https://` 로 바꿉니다.

  6. Apply the new conf in the compose folder: `docker compose exec webserver nginx -t && docker compose exec webserver nginx -s reload` (or restart only nginx: `docker compose restart webserver`). Plane 의 `PLANE_WEB_URL` 등이나 Gitea 의 `GITEA_ROOT_URL` 을 바꿨다면 `docker compose up -d plane-api plane-web plane-live` · `docker compose up -d gitea` 로 해당 컨테이너만 다시 만듭니다. 전체 `docker compose restart` 는 모든 서비스를 동시에 재시작하므로 app 이 내려가는 순간 nginx 가 떠 `[emerg] host not found in upstream` 으로 한 번 종료될 수 있습니다(자동 재기동) — 전체 재기동은 `docker compose stop` → `docker compose start` 를 쓰세요. Do not use `docker compose down -v` — named volumes (SQLite `/data`, Plane 데이터, Gitea 저장소) are deleted.

  7. Certbot 갱신 cron 은 nginx 이미지 안에 내장되어 있습니다 (`docker/nginx/Dockerfile` 이 빌드 시 crontab 에 등록). 호스트에서 별도 `crontab` 설정은 **불필요** 합니다. 확인: `docker compose exec webserver crontab -l`.

## Community

- **Personal Website** : Owner's personal website is devspoon.com

## Demos

- **youtube** - Preparing

## Partners and Users

- Lim Do-Hyun Owner Developer/project Manager, bluebamus@gmail.com
  Personal github.io : [bluebamus.github.io]

- 임도현 Owner 개발자/기획자, bluebamus@gmail.com
  개인 github.io 사이트 : [bluebamus.github.io]

<!-- Markdown link & img dfn's -->

[devspoon-web]: https://github.com/devspoons/devspoon-web
[Jenkins(KR)]: https://jjeongil.tistory.com/810
[Harbor(KR)]: https://engineering.linecorp.com/ko/blog/harbor-for-private-docker-registry/
[Plane]: https://plane.so/
[Plane docs]: https://developers.plane.so/self-hosting/overview
[Jenkins]: https://en.wikipedia.org/wiki/Jenkins_(software)
[Gitea]: https://about.gitea.com/
[Gitea docs]: https://docs.gitea.com/installation/install-with-docker
[Harbor]: https://en.wikipedia.org/wiki/Harbor
[bluebamus.github.io]: https://bluebamus.github.io
