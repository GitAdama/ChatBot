# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.choices import Choice
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import (
    MessageFactory,
    TurnContext,
    BotTelemetryClient,
    NullTelemetryClient,
)
from botbuilder.dialogs.prompts.choice_prompt import ChoicePrompt
from botbuilder.schema import InputHints

from booking_details import BookingDetails
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from .booking_dialog import BookingDialog
from botbuilder.azure import CosmosDbConfig,CosmosDbStorage
import pymongo

# COSDB = None
class MainDialog(ComponentDialog):
    def __init__(
        self,
        luis_recognizer: FlightBookingRecognizer,
        booking_dialog: BookingDialog,
        cosmodb: CosmosDbStorage, 
        telemetry_client: BotTelemetryClient = None,
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)
        self.telemetry_client = telemetry_client or NullTelemetryClient()
        self.booking_details_ = None
        self.cosmodb = cosmodb
        choice_prompt = ChoicePrompt(ChoicePrompt.__name__)
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = self.telemetry_client
        choice_prompt.telemetry_client = self.telemetry_client

        booking_dialog.telemetry_client = self.telemetry_client
        cosmodb.telemetry_client = self.telemetry_client
        wf_dialog = WaterfallDialog(
            "WFDialog", [self.intro_step, self.act_step, self.confirm_step, self.final_step]
        )
        wf_dialog.telemetry_client = self.telemetry_client

        self._luis_recognizer = luis_recognizer
        self._booking_dialog_id = booking_dialog.id

        self.add_dialog(choice_prompt)
        self.add_dialog(text_prompt)
        self.add_dialog(booking_dialog)
        self.add_dialog(wf_dialog)

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)
    
        
        message_text = (
            str(step_context.options)
            if step_context.options
            else "What can we help you with today?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text(f"Luis ON?{step_context.options}")
        #         ))
        self.booking_details_ = None

        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the BookingDialog path with an empty BookingDetailsInstance.
            # await step_context.prompt(
            #     TextPrompt.__name__,
            #     PromptOptions(
            #         prompt=MessageFactory.text(f"Luis ON?{step_context.options}")
            #     ))
            self.booking_details_ = None

            return await step_context.begin_dialog(
                self._booking_dialog_id, BookingDetails()
            )
            

        # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
        intent, luis_result, recognizer_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )
        # first_conv = step_context.result
        # step_context.values["first_conv"] = f"User_start_conv : {first_conv}"
        
        # await step_context.context.send_activity(f"TEST_var{first_conv}")
        TEST_LUIS_intent = recognizer_result.entities.get("or_city", [{"$instance": {}}])[0]
                        
                    
        # await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text(f"Luis ON?{intent} and {luis_result}, {recognizer_result}/n {TEST_LUIS_intent}")
        #         ))
        if intent == Intent.BOOK_FLIGHT.value and luis_result:
            # Show a warning for Origin and Destination if we can't resolve them.
            await MainDialog._show_warning_for_unsupported_cities(
                step_context.context, luis_result
            )
            self.booking_details_ = None

            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._booking_dialog_id, luis_result)

        # if intent == Intent.GET_WEATHER.value:
        #     get_weather_text = "TODO: get weather flow here"
        #     get_weather_message = MessageFactory.text(
        #         get_weather_text, get_weather_text, InputHints.ignoring_input
        #     )
        #     await step_context.context.send_activity(get_weather_message)

        else:
            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)
    
    async def confirm_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        # await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text(f"user_validation {step_context.values.items()} and details {step_context.result.user_validation}")
        #         ),
        #     )
        self.booking_details_ = None

        if step_context.result is not None:
            self.booking_details_ = result  = step_context.result
            

        #     # Now we have all the booking details call the booking service.

        #     # If the call to the booking service was successful tell the user.
        #     # time_property = Timex(result.travel_date)
        #     # travel_date_msg = time_property.to_natural_language(datetime.now())
        #     MY_TEST = (result.user_validation.lower() == "unsatisfy")
            
            msg_txt = f"I have you booked to {result.destination} from {result.origin} on {result.go} until {result.back} for {result.budget}"
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)
        #     # return 
            return await step_context.prompt(
                ChoicePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(f"Please give a review for improvement prurpose"),
                    choices=[Choice("Unsatisfy"), Choice("Good"), Choice("Perfect")],
                ),)
           


    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
      
        self.booking_details_.user_validation = step_context.result.value
         
        if self.booking_details_ is not None:
            result = self.booking_details_

            
          
            if result.user_validation.lower() == "unsatisfy":
                # log_id = step_context._turn_context.activity.conversation.as_dict()["id"] 
                # collectionStore = {f"{log_id}" : None}
                self.booking_details_.user = step_context._turn_context.activity.conversation.as_dict()['id']
                self.cosmodb.insert_one(self.booking_details_.__dict__) 
                # self.cosmodb.write({f"booking{step_context._turn_context.activity.conversation.as_dict()['id'] }" : self.booking_details_})
                # result.conv_log.append(step_context.values["first_conv"])
                
                await step_context.context.send_activity(f"Thanks for you review we keep anonymous track of this conversation for improvement purpose")#, {result.conv_log}") # AND {self.booking_details_.conv_log}")
                self.booking_details_ = None
        prompt_message = "Thank for using our bot service! What else can we do for you?"
        return await step_context.replace_dialog(self.id, prompt_message)

    @staticmethod
    async def _show_warning_for_unsupported_cities(
        context: TurnContext, luis_result: BookingDetails
    ) -> None:
        """
        Shows a warning if the requested From or To cities are recognized as entities but they are not in the Airport entity list.
        In some cases LUIS will recognize the From and To composite entities as a valid cities but the From and To Airport values
        will be empty if those entity values can't be mapped to a canonical item in the Airport.
        """
        if luis_result.unsupported_airports:
            message_text = (
                f"Sorry but the following airports are not supported:"
                f" {', '.join(luis_result.unsupported_airports)}"
            )
            message = MessageFactory.text(
                message_text, message_text, InputHints.ignoring_input
            )
            await context.send_activity(message)
