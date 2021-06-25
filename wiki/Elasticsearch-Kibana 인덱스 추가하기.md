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

    ![1](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/95f08d9c-a2cf-4e8f-9a5b-053e8a3975d5/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210625%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210625T134403Z&X-Amz-Expires=86400&X-Amz-Signature=db97be6c86d50bcea0b14dd5ba3671a9cb56eec36ceb6b1001e05266a7c534ba&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22)

3. 현재 매핑 확인

    ```bash
    GET {index name}/_mapping
    ```