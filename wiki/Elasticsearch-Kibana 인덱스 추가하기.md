# Elasticsearch - Kibana 인덱스 추가하기

1. **AWS Elasticsearch Service**에서 **Kibana** 접속
2. `Stack Management` - `Dev Tools` - `console`에서 아래 명령 실행

    ```bash
    PUT coinboard4
    {
      "mappings": {
        "properties": {
          "close_price" : {
            "type": "double",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "high_price" : {
            "type" : "double",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "low_price" : {
            "type" : "double",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "num_trades" : {
            "type" : "long"
          },
          "open_price" : {
            "type" : "double",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "opentime" : {
            "type" : "date"
          },
          "quote_asset_volume" : {
            "type" : "double",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          },
          "symbol" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          }
        }
      }
    }
    ```

    ![Elasticsearch%20-%20Kibana%20%E1%84%8B%E1%85%B5%E1%86%AB%E1%84%83%E1%85%A6%E1%86%A8%E1%84%89%E1%85%B3%20%E1%84%8E%E1%85%AE%E1%84%80%E1%85%A1%E1%84%92%E1%85%A1%E1%84%80%E1%85%B5%20fd8cae0a4b364247b8cc92dc6d1b0aaf/Untitled.png](Elasticsearch%20-%20Kibana%20%E1%84%8B%E1%85%B5%E1%86%AB%E1%84%83%E1%85%A6%E1%86%A8%E1%84%89%E1%85%B3%20%E1%84%8E%E1%85%AE%E1%84%80%E1%85%A1%E1%84%92%E1%85%A1%E1%84%80%E1%85%B5%20fd8cae0a4b364247b8cc92dc6d1b0aaf/Untitled.png)

3. 현재 매핑 확인

    ```bash
    GET {index name}/_mapping
    ```