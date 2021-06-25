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

![Elasticsearch%20Kibana%20%E1%84%89%E1%85%A5%E1%86%AF%E1%84%8E%E1%85%B5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%89%E1%85%B5%E1%86%AF%E1%84%92%E1%85%A2%E1%86%BC%20823015e51fa24586ba49605fa987f604/Untitled.png](Elasticsearch%20Kibana%20%E1%84%89%E1%85%A5%E1%86%AF%E1%84%8E%E1%85%B5%20%E1%84%86%E1%85%B5%E1%86%BE%20%E1%84%89%E1%85%B5%E1%86%AF%E1%84%92%E1%85%A2%E1%86%BC%20823015e51fa24586ba49605fa987f604/Untitled.png)