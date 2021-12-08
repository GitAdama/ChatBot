#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Configuration for the bot."""

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LuisAppId", "8a5d989d-fb81-4078-9f42-f4ca77d8356f")
#   03786a1b-fd5d-47b5-8162-77087f15d0cf    
    # LUIS_API_KEY = os.environ.get("LuisAPIKey", "d64005b2c6784af9896afb766f71e14e")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "5b83e952f7b848caa14a00b503e6d582")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "luisadama.cognitiveservices.azure.com/")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "luisadama-authoring.cognitiveservices.azure.com/")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "178ef8e8-27bf-4e38-86a7-27b750e91b45"
    )
    
    # Cosmos database credentials


    DB_URI = "mongodb://dbp10adama:Y2bnS1kx9XpImZ5fxV0msuRqnECigdIhNuWQKuqHjnBOtU9ikcOBZQjD2EmyswKBFPNv1FkZctSYJNOn7JKuag==@dbp10adama.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@dbp10adama@"


    DB = "Conversations"
    DB_COLLECTION = "ConvCollection"

    COSDB_URL = "dbp10adama.mongo.cosmos.azure.com"#"https://localhost:8081"
    COSDB_COLLECTION = "Conversations"
    COSDB_DB = "ConvCollection"
    COSDB_KEY = "Y2bnS1kx9XpImZ5fxV0msuRqnECigdIhNuWQKuqHjnBOtU9ikcOBZQjD2EmyswKBFPNv1FkZctSYJNOn7JKuag==" #"C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
