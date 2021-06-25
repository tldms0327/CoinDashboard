# Elasticsearch/Kibana 설치 및 실행

# ✅ Elasticsearch

### Java 설치

```bash
$ sudo apt-get update
$ sudo apt-get install default-jre
$ java -version # java version 8 이상이어야 함
```

### Elasticsearch 설치

[Install Elasticsearch with Debian Package | Elasticsearch Guide [7.13] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html)

```bash
$ wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.13.2-amd64.deb
$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.13.2-amd64.deb.sha512
$ shasum -a 512 -c elasticsearch-7.13.2-amd64.deb.sha512
$ sudo dpkg -i elasticsearch-7.13.2-amd64.deb
```

### 환경 설정

```bash
$ sudo vim /etc/elasticsearch/elasticsearch.yml
# 원격 접속을 위해 아래 설정 추가
network.host: 0.0.0.0
```

### 실행

```bash
# 시작
$ sudo systemctl start elasticsearch.service

# 실행 상태 확인
$ sudo systemctl status elasticsearch.service

# 종료
$ sudo systemctl stop elasticsearch.service
```

# ✅ Kibana

### Kibana 설치

[Install Kibana with Debian package | Kibana Guide [7.13] | Elastic](https://www.elastic.co/guide/en/kibana/current/deb.html)

```bash
$ wget https://artifacts.elastic.co/downloads/kibana/kibana-7.13.2-amd64.deb
$ shasum -a 512 kibana-7.13.2-amd64.deb
$ sudo dpkg -i kibana-7.13.2-amd64.deb
```

### 환경 설정

```bash
$ sudo vim /etc/kibana/kibana.yml
# 아래 설정 추가
server.port: 5601
server.host: "0.0.0.0"
elasticsearch.host: ["http://localhost:9200"]
```

### 실행

```bash
# 시작
$ sudo systemctl start kibana.service

# 실행 상태 확인
$ sudo systemctl status kibana.service

# 종료
$ sudo systemctl stop kibana.service
```

주소창에 `http://{ec2IP_address}:5601`을 입력하여 Kibana에 접속한다.

![1](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/28c15cb8-50e4-4c38-b9e3-374a70f1e586/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210625%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210625T134326Z&X-Amz-Expires=86400&X-Amz-Signature=3285456b270c2e354da856efad0ca15437cb8fbdb40f54b1544e0b38f57b3035&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22)