import os
import logging
import sys
import traceback
from aiounittest import AsyncTestCase
from botbuilder import testing
from botbuilder.applicationinsights.application_insights_telemetry_client import ApplicationInsightsTelemetryClient
from botbuilder.core import MessageFactory, middleware_set
from botbuilder.core.conversation_state import ConversationState
from botbuilder.core.memory_storage import MemoryStorage
from botbuilder.core.user_state import UserState
from botbuilder.dialogs import (
    ComponentDialog,
    DialogContext,
    DialogTurnResult,
    DialogTurnStatus,
    PromptOptions,
    TextPrompt,
    WaterfallDialog,
    WaterfallStepContext,
    dialog,
    waterfall_step_context,
)
from botbuilder.integration.applicationinsights.aiohttp.aiohttp_telemetry_processor import AiohttpTelemetryProcessor
from botbuilder.schema import Activity
from botbuilder.testing import DialogTestClient, DialogTestLogger
from pymongo import collection
from bots.dialog_and_welcome_bot import DialogAndWelcomeBot
from dialogs import BookingDialog
from config import DefaultConfig
from booking_details import BookingDetails
from dialogs.main_dialog import MainDialog
from flight_booking_recognizer import FlightBookingRecognizer
from botbuilder.azure import CosmosDbConfig,CosmosDbStorage
import  pymongo




MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)

CONFIG = DefaultConfig()

INSTRUMENTATION_KEY = CONFIG.APPINSIGHTS_INSTRUMENTATION_KEY
TELEMETRY_CLIENT = ApplicationInsightsTelemetryClient(
    INSTRUMENTATION_KEY, telemetry_processor=AiohttpTelemetryProcessor(), client_queue_size=10
)



# ComosDB config
# COSDB_URL = CONFIG.COSDB_URL
# COSDB_KEY = CONFIG.COSDB_KEY
# COSDB_COLLECTION = CONFIG.COSDB_COLLECTION
# COSDB_DB = CONFIG.COSDB_DB 

# cosconfig = CosmosDbConfig(COSDB_URL, COSDB_KEY, COSDB_COLLECTION, COSDB_DB)
# cosdbStore = CosmosDbStorage(cosconfig)

URI = CONFIG.DB_URI
DATA_BASE = CONFIG.DB 
DB_COLLECTION = CONFIG.DB_COLLECTION 
client = pymongo.MongoClient(URI)

myDB = client[DATA_BASE]
cosdbStore = myDB[DB_COLLECTION]

# cosdbStore.insert_one({"user": "test"})


# Create dialogs and Bot
RECOGNIZER = FlightBookingRecognizer(CONFIG)
BOOKING_DIALOG = BookingDialog()
DIALOG = MainDialog(RECOGNIZER, BOOKING_DIALOG, cosdbStore, telemetry_client=TELEMETRY_CLIENT)
BOT = DialogAndWelcomeBot(CONVERSATION_STATE, USER_STATE, DIALOG, TELEMETRY_CLIENT)


class DialogTestClientTest(AsyncTestCase):
    """Tests for dialog test client."""

    def __init__(self, *args, **kwargs):
        super(DialogTestClientTest, self).__init__(*args, **kwargs)
        logging.basicConfig(format="", level=logging.INFO)
    
    async def test_new_unitest_bot_full_wfd_and_waiting_status(self):
                
        compnt = DIALOG
        client = DialogTestClient(
            "test", 
            compnt,
            middlewares=[DialogTestLogger()]
        )
        compnt

        reply = await client.send_activity("hello")
        self.assertEqual("What can we help you with today?", reply.text)
        reply = await client.send_activity("I want to go to Paris from London ")
        self.assertEqual("When will you go?", reply.text)
        reply = await client.send_activity("september 30th")
        self.assertEqual("Wich date you come back?", reply.text)
        reply = await client.send_activity("december 31")
        self.assertEqual("What is your budget?", reply.text)
        reply = await client.send_activity("2000€")
        self.assertEqual("I have you booked to Paris from London on september 30th until december 31 for 2000€", reply.text)
        next_reply = client.get_next_reply()
        self.assertEqual("Please give a review for improvement prurpose (1) Unsatisfy, (2) Good, or (3) Perfect", next_reply.text)
        reply = await client.send_activity("Good")
        self.assertEqual("Thank for using our bot service! What else can we do for you?", reply.text)
        self.assertEqual(DialogTurnStatus.Waiting, client.dialog_turn_result.status)        
        

    async def test_new_unitest_bot_ask_budget_resume_and_review(self):
                

        compnt = DIALOG
        client = DialogTestClient(
            "test", 
            compnt,
            middlewares=[DialogTestLogger()]
        )
        compnt

        reply = await client.send_activity("hello")
        self.assertEqual("What can we help you with today?", reply.text)
        reply = await client.send_activity("I want to go to Paris from London on september 30th to december 31")
        self.assertEqual("What is your budget?", reply.text)

        reply = await client.send_activity("2000€")
        self.assertEqual("I have you booked to Paris from London on september 30th until december 31 for 2000€".lower(), reply.text.lower())
        next_reply = client.get_next_reply()
        self.assertEqual("Please give a review for improvement prurpose (1) Unsatisfy, (2) Good, or (3) Perfect", next_reply.text)
        reply = await client.send_activity("Good")
        self.assertEqual("Thank for using our bot service! What else can we do for you?", reply.text)



    async def test_new_unitest_bot_continue_dialog_and_saved_conv(self):
        # testing = cosdbStore
        # print("TEST", cosdbStore.)
        compnt = DIALOG
        client = DialogTestClient(
            "test", 
            compnt,
            middlewares=[DialogTestLogger()]
        )
        compnt

        reply = await client.send_activity("hello")
        self.assertEqual("What can we help you with today?", reply.text)
        reply = await client.send_activity("I want to go to Paris from London on september 30th to december 31")
        self.assertEqual("What is your budget?", reply.text)

        reply = await client.send_activity("2000€")
        self.assertEqual("I have you booked to Paris from London on september 30th until december 31 for 2000€".lower(), reply.text.lower())
        next_reply = client.get_next_reply()
        self.assertEqual("Please give a review for improvement prurpose (1) Unsatisfy, (2) Good, or (3) Perfect", next_reply.text)
        reply = await client.send_activity("Good")
        self.assertEqual("Thank for using our bot service! What else can we do for you?", reply.text)
        #End last dialogue and begin new dialogue
        
        reply = await client.send_activity("I want to go to Paris from London on september 30th to december 31 with 2000€")
        self.assertEqual("I have you booked to Paris from London on september 30th until december 31 for 2000".lower(), reply.text.lower())
        next_reply = client.get_next_reply()
        self.assertEqual("Please give a review for improvement prurpose (1) Unsatisfy, (2) Good, or (3) Perfect", next_reply.text)
        reply = await client.send_activity("Unsatisfy")
        self.assertEqual("Thanks for you review we keep anonymous track of this conversation for improvement purpose", reply.text)
        next_reply = client.get_next_reply()
        self.assertEqual("Thank for using our bot service! What else can we do for you?", next_reply.text)
        
        # # Look in database to see saved dialogue.
        item = cosdbStore.find_one({"user": "Convo1"})
        
        dialog_saved = item["conv_log"]
        self.assertIn('I want to go to Paris from London on september 30th to december 31 with 2000€', dialog_saved)
