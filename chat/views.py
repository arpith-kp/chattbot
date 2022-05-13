# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

import requests
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import dialogflow
import os
import json
from django.views.decorators.csrf import csrf_exempt
#from dialogflow_v2 import dialogflow_v2 as Dialogflow
# Create your views here.
from requests.auth import HTTPBasicAuth

from bridge.models import BridgeResponse, BridgeResponsePayload
from bridge.serializer import BridgeRequestSerializer
from bridge.serializer import BridgeResponseSerializer

POST_URL = 'https://subdomain0.ezegnyte.com/rest/public/chatbot/1.0/send'

@require_http_methods(['GET'])
def index_view(request):
    return render(request, 'home.html')

def convert(data):
    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)

    return data


def send_request_to_egnyte(response):
    if response.query_result.intent.display_name == "user":
        parameters = response.query_result.parameters
        foldername = parameters.fields.get('foldername')
        username = parameters.fields.get('username')
        data = {
            "requestId": uuid.uuid4(),
            'requestedAction': "SET_PERMISSION",
            'requestedPayload': {
                "folderName": foldername.string_value,
                "userName": username.string_value,
                "priv": "RWD"

            }
        }

        # bridgeSerializer = BridgeRequestSerializer(data)
        # bridgeRequest = JsonResponse(bridgeSerializer)
        r = requests.post(POST_URL, data=json.dumps(data),auth = HTTPBasicAuth('user1', 'puser1'))
        # bridgeResponse = BridgeResponsePayload.objects.all().first()
        data = r.json()
        # serializer = BridgeResponseSerializer(r.json())
        # finalR = model_to_dict(data)
        return json.dumps(data, cls=DjangoJSONEncoder)
        # try:
        #     bridgeResponse = BridgeResponseSerializer(finalR)
        #     bridgeResponseObj = bridgeResponse.data
        #     return bridgeResponseObj
        # except Exception as e:
        #     bridgeResponse = BridgeResponse.objects.none()
        #     bridgeResponseObj = bridgeResponse.data
        #     return bridgeResponseObj

        # if r.status_code == 200:
        #     try:
        #         bridgeResponse = BridgeResponseSerializer(r.json())
        #         bridgeResponseObj = bridgeResponse.data
        #         return bridgeResponseObj
        #     except Exception as e:
        #         bridgeResponse = BridgeResponse.objects.none()
        #         bridgeResponseObj = bridgeResponse.data
        #         return bridgeResponseObj


@csrf_exempt
@require_http_methods(['POST'])
def chat_view(request):
    print('Body', request.body)
    input_dict = convert(request.body)
    input_text = json.loads(input_dict)['text']

    GOOGLE_AUTHENTICATION_FILE_NAME = "AppointmentScheduler.json"
    current_directory = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_directory, GOOGLE_AUTHENTICATION_FILE_NAME)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

    GOOGLE_PROJECT_ID = "academic-ratio-125719"
    session_id = "1234567891"
    context_short_name = "does_not_matter"

    context_name = "projects/" + GOOGLE_PROJECT_ID + "/agent/sessions/" + session_id + "/contexts/" + \
               context_short_name.lower()

    parameters = dialogflow.types.struct_pb2.Struct()
    #parameters["foo"] = "bar"

    context_1 = dialogflow.types.context_pb2.Context(
        name=context_name,
        lifespan_count=2,
        parameters=parameters
    )
    query_params_1 = {"contexts": [context_1]}

    language_code = 'en'
    
    response = detect_intent_with_parameters(
        project_id=GOOGLE_PROJECT_ID,
        session_id=session_id,
        query_params=query_params_1,
        language_code=language_code,
        user_input=input_text
    )

    egnyteResponse = None
    try:
        egnyteResponse = send_request_to_egnyte(response)
    except Exception as e:
        print(e)
        pass

    if egnyteResponse is None:
        response = response.query_result.fulfillment_text
    else:
        response = egnyteResponse

    return HttpResponse(response, status=200)
    # return HttpResponse(JsonResponse(egnyteResponse), status=200)


def detect_intent_with_parameters(project_id, session_id, query_params, language_code, user_input):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    #text = "this is as test"
    text = user_input

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input,
        query_params=query_params
    )

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    print('Parameters: {} ', response.query_result.parameters)

    return response
    

def about(request):
    return render(request, 'chat/about.html')
