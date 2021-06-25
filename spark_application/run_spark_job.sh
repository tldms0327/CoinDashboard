#/bin/bash

zip py-files.zip IndicatorCalculator.py DataLoader.py
spark-submit --master yarn --deploy-mode cluster --py-files py-files.zip main.py
