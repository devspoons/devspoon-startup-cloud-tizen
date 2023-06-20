# devspoon-startup-cloud-tizen

devspoon-startup-cloud-tizen creates third-party application servers that automatically interact with SmartThings, Bixby, and other systems through Docker.
This provides a server infrastructure of back-end services for Tizen-based IoT devices.

devspoon-startup-cloud-tizen는 docker를 통해 SmartThings, Bixby 그리고 다른 시스템들과 자동으로 상호 연동되는 서드파티 어플리케이션 서버를 만들어 줍니다.  
본 기술은 Tizen-based IoT 장치들을 위한 back-end 인프라를 구축는 방법을 제공해 줍니다.

- You can get more informations at [devspoons.github.io]

## Project management solutions

- **[OpenProject] :** Open source project management software to help you work on your project efficiently

- **[Jenkins] :** As one of the CI tools, CI (Continuous Integration) refers to continuous integration, which is an automated process for developers, and new code changes are automatically built and tested regularly to notify developers to solve problems that can occur when multiple developers develop simultaneously. Software that helps secure development stability and reliability

- **[Gitolite] :** Configuration Management Tool. user can install git server software at own server

- **[Harbor] :** The Private Docker Registry Server for businesses that store and distribute Docker Images

- **[OpenProject(KR)] :** 프로젝트를 효율적으로 진행할 수 있도록 지원하는 오픈 소스 프로젝트 관리 소프트웨어

- **[Jenkins(KR)] :** CI 툴 중 하나로 CI (Continuous Integration)는 개발자를 위한 자동화 프로세스인 지속적인 통합을 말하며 새로운 코드 변경 사항들이 정기적으로 자동 빌드 및 테스트되어 개발자에게 알려줌으로 여러명의 개발자가 동시에 개발하며 발생할 수 있는 문제들을 해결하여 개발의 안정성 및 신뢰성을 확보할 수 있도록 지원하는 소프트웨어

- **[Gitolite] :** 형상 관리 도구 혹은 버전관리 시스템으로 자체적으로 설치하고 운영할 수 있는 git 소프트웨어

- **[Harbor(KR)] :** Docker Image를 저장하고 분배하는 기업용 Private Docker Registry Server

## Features

- **Supports creation of configuration files required for each service:** Environment files and security keys used for each service are created according to the user's keyboard input using a shell script or automatically generated.

- **User custom installation support :** You can selectively install only the desired solution at compose/project_mng_service/(solution) without having to install all the solutions.

  - If you want to install more than one solution at the same time, just uncomment what you want at compose/master_service/docker-compose.yml.

- **Access web server and project management solutions with one nginx through nginx proxy :** All solutions are available on one nginx server.

  - You can use ssh for direct access to gitolite.
  - The harbor will be supported in a future version due to security issues, and you can connect to your own server through harbor.yml.

    ```
    Example

    test.com -> company website
    blog.test.com -> blog website
    shop.test/com -> shopping mall website
    open.test.com -> openproject solution
    jen.test.com -> jenkins solution
    ```

- **각 서비스들에 필요한 환경설정 파일 생성 지원 :** 각 서비스들에 사용되는 환경파일 및 보안키 등을 쉘 스크립트를 이용해 사용자의 키보드 입력에 맞춰 생성하거나 자동으로 생성합니다.

- **사용자 맞춤식 설치 지원 :** 모든 솔루션을 설치할 필요 없이 compose/project_mng_service/(solution)에서 원하는 솔루션만 선택적으로 설치할 수 있습니다.

  - 두개 이상의 솔루션을 동시에 설치하고 싶다면 compose/master_service/docker-compose.yml에서 원하는 항목만 주석 제거하면 됩니다.

- **nginx의 proxy를 통해 하나의 nginx로 웹서버 및 프로젝트 관리 솔루션들에 접근 가능 :** 하나의 nginx 서버에서 모든 솔루션을 이용할 수 있습니다.

  - gitolite는 ssh로 직접 접근하여 사용하면 됩니다.
  - harbor는 보안문제로 차후 버전에서 지원할 예정이며 harbor.yml을 통해 자체 서버로 연결 가능합니다.

    ```
    Example

    test.com -> company website
    blog.test.com -> blog website
    shop.test/com -> shopping mall website
    open.test.com -> openproject solution
    jen.test.com -> jenkins solution
    ```

## considerations

- **Development-oriented docker service** : This open source is designed for focused on development-oriented rather than perfect docker container distribution and is suitable for startups or new service development teams with frequent initial modifications and tests.

- **Orchestration not supported** : In the future, we plan to interoperate with cloud services such as AWS and GCM

- **this open-source considers generic servers that are not support AWS, GCM** : This open source is intended to be installed and operated on a server that is directly operated, and on general server hosting, and plans to integrate with cloud services such as AWS and GCM in the future
- **개발 중심적 docker 서비스** : 이 오픈소스는 완전한 docker container의 배포가 아닌 개발 중심적으로 설계되었으며 초기 수정과 테스트가 빈번한 스타트업 혹은 신규 서비스 개발팀에게 적합합니다.
- **오케스트레이션 미지원** : 앞으로 AWS, GCM 등의 Cloud 서비스와 연동할 계획이며 이후 오캐스트레이션이 지원될 예정입니다.
- **AWS, GCM 기반이 아닌 일반 서버 고려** : 이 오픈소스는 직접 운용하고있는 서버, 일반적인 서버 호스팅에서 설치하여 운영하는 것을 목적으로 하고 있으며 앞으로 단계적으로 AWS, GCM 등의 Cloud 서비스와 연동할 계획입니다.

## Install & Run

### OpenProject

1. When using OpenProject, e-mail account information is required to send events by e-mail

- [mailgun] service setting

  - It is recommended to use [sendgrid] as the rate policy change

  ```
  Information on the following items should be updated by referring to the comments in the docker-compose.yml file in the compose/project_mng_service/nginx_openproject folder

  environment:
        EMAIL_DELIVERY_METHOD: smtp
        SMTP_ADDRESS: smtp.mailgun.org #Need to change when using other services than mailgun
        SMTP_PORT: 587 #Need to change when using other services than mailgun
        SMTP_DOMAIN: "test.com" #user's SMTP domain information
        SMTP_AUTHENTICATION: login
        SMTP_ENABLE_STARTTLS_AUTO: "true"
        SMTP_USER_NAME: "test@test.com" #Service account information
        SMTP_PASSWORD: "1234567890067655abcdefgh" #Service authentication key information
  ```

2. Run nginx_proxy_conf.sh file in config/web-server/(web server type) and enter service port number, domain, proxy url(Openproject's application name in docker-compose.yml), proxy port number, filename, and than, it make a nginx conf file in conf.d folder

3. Run docker-compose.yml (single mode)

   ```
   get move to compose/project_mng_service/nginx_openproject
   Execute docker-compose.yml using "docker-compose up -d" command
   ```

4. There are advanced information in [OpenProject Official User Documentation](https://docs.openproject.org/installation-and-operations/operation/backing-up/)

---

### Jenkins

1. Run nginx_proxy_conf.sh file in config/web-server/(web server type) and enter service port number, domain, proxy url(Openproject's application name in docker-compose.yml), proxy port number, filename, and than, it make a nginx conf file in conf.d folder

2. Run docker-compose.yml (single mode)

   ```
   get move to compose/project_mng_service/nginx_jenkins
   Execute docker-compose.yml using "docker-compose up -d" command
   ```

3. There are advanced information in [Jenkins Official User Documentation](https://www.jenkins.io/doc/)

---

### Gitolite

1. This docker make 2 account as gitolite-creator and git-manager. gitolite install at gitolite-creator and git-manager will manage gitolite system such as add new user or make new repogitory etc

2. For management add new user account or make new repository, administrator must be accessed gitolite server by git-manager account. So, User must make client_user.pub key in docker/gitolite/system folder. Dockerfile will add this key at authorized_keys in git-manager account

3. Run docker-compose.yml (single mode)

   ```
   get move to compose/project_mng_service/gitolite
   current ssh port number is 2222. if user want to change the ssh port number, modify in docker-compose.yml
   Execute docker-compose.yml using "docker-compose up -d" command
   ```

4. There are sample code

   - /home/git-manager/sample-script in the container

   ```
   clone_admin.sh -> clone admin repository to manage gitolite system. administrator must manage gitolite system though only git-manager account
   add_user.sh -> it show how to add new user in gitolite
   ```

5. There are advanced information in [Gitolite Cookbook](https://gitolite.com/gitolite/cookbook)

---

### Harbor

1. To use harbor, it require latest docker-compose package. run /compose/project_mng_service/harbor-v.2.0.0/update_docker-compose.sh. if user already have latest version than 1.26.0, don't need this step

2. harbor require a configuration file such as harbor.yml. update_harbor_config.sh file make harbor.yml. and then run install.sh, harbor will install successfully

3. If user want to install harbor by one step, user can use autoinstall.sh file. it is process to make harbor.yml and run install.sh.

4. If user want to use https, have to make ssl key in /compose/project_mng_service/harbor-v.2.0.0/ssl/ before runing install.sh or autoinstall.sh.

5. If user want to make ssl key, refer "Setting up HTTPS on a web server" section. there are at bottom in this page

6. There are advanced information in [Harbor 2.0 Documentation](https://goharbor.io/docs/2.0.0/)

## Setting up HTTPS on a web server

- This step requires running http nginx server. it recommend php nginx server for this step. if user need to informations for this, refer to [devspoon-web]

  ```
  1. There are letsencrypt.sh shell script file in script folder and it interlocked by volumes.
  so user can access script file in a nginx container.

  2. use "docker exec -it <nginx container name> bash" command, user can get docker inside.

  3. run letsencrypt.sh and insert informations such as webroot, domain, e-mail etc.
      this script make ssl-key and make crontab schedule automatically

  4. using "exit" command user can get off from container

  5. Run nginx_proxy_https_conf.sh file in config/web-server/(web server type) and enter service port number, domain, proxy url(Openproject's application name in docker-compose.yml), proxy port number, filename, and than, it make a nginx conf file in conf.d folder

  6. user have to remove http conf file in config/web-server/<service>/conf.d/

  7. run "docker-compose up" command in the compose folder
  ```

## Community

- **Personal Website :** Owner's personam website is [devspoon.com]
- **Github.io :** Ther are more detail guide [devspoon.github.io]

## Demos

- **[youtube]** - Preparing

## Partners and Users

- Lim Do-Hyun Owner Developer/project Manager, bluebamus@gmail.com  
  Personal github.io : [bluebamus.github.io]

- 임도현 Owner 개발자/기획자, bluebamus@gmail.com  
  개인 github.io 사이트 : [bluebamus.github.io]

<!-- Markdown link & img dfn's -->

[devspoon-web]: https://github.com/devspoons/devspoon-web
[OpenProject(KR)]: http://wiki.webnori.com/display/pms/Open+Project+7
[Jenkins(KR)]: https://jjeongil.tistory.com/810
[Harbor(KR)]: https://engineering.linecorp.com/ko/blog/harbor-for-private-docker-registry/
[mailgun]: https://www.mailgun.com/
[sendgrid]: https://sendgrid.com/
[OpenProject]: https://docs.openproject.org/user-guide/wiki/
[Jenkins]: https://en.wikipedia.org/wiki/Jenkins_(software)
[Gitolite]: https://wiki.archlinux.org/index.php/Gitolite
[Harbor]: https://en.wikipedia.org/wiki/Harbor
[bluebamus.github.io]: bluebamus.github.io
[devspoons.github.io]: devspoons.github.io
