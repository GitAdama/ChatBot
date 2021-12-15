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
    LUIS_APP_ID = os.environ.get("LuisAppId", "ca94a985-2be7-4c01-9639-b1eabf364d0a")
#   03786a1b-fd5d-47b5-8162-77087f15d0cf    
    # LUIS_API_KEY = os.environ.get("LuisAPIKey", "d64005b2c6784af9896afb766f71e14e")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "a087c67998a749968f5b196587c2308e")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "myluisadama.cognitiveservices.azure.com/") #("LuisAPIHostName", "luisadama.cognitiveservices.azure.com/")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "myluisadama-authoring.cognitiveservices.azure.com/") #("LuisAPIHostName", "luisadama-authoring.cognitiveservices.azure.com/")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "c53d8bdd-108c-4b97-8f31-b26870f6f661"
    )
    
    
    # Cosmos database credentials
    DB_URI = "mongodb://p10db:82MFBcUdxpkcVuzfuauwuuIvQ6C4HG5CAIM5XasAd6P0wRobTkv0vsIJ5ZCB464rXC3Ar6OLfCaW65JGsHVCRQ==@p10db.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@p10db@"


    DB = "Conversations"
    DB_COLLECTION = "ConvCollection"

    COSDB_URL = "p10db.mongo.cosmos.azure.com" #"dbp10adama.mongo.cosmos.azure.com"#"https://localhost:8081"
    COSDB_COLLECTION = "Conversations"
    COSDB_DB = "ConvCollection"
    COSDB_KEY = "82MFBcUdxpkcVuzfuauwuuIvQ6C4HG5CAIM5XasAd6P0wRobTkv0vsIJ5ZCB464rXC3Ar6OLfCaW65JGsHVCRQ==" #"Y2bnS1kx9XpImZ5fxV0msuRqnECigdIhNuWQKuqHjnBOtU9ikcOBZQjD2EmyswKBFPNv1FkZctSYJNOn7JKuag==" #"C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
