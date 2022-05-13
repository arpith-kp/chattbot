import json

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from bridge.models import BridgeResponsePayload
from bridge.serializer import BridgeRequestSerializer, BridgeResponseSerializer
from django.forms.models import model_to_dict


@csrf_exempt
def egnyte_post(request:HttpRequest):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        serializer = BridgeRequestSerializer(data=data)
        try:
            if serializer.is_valid():
                bridgeResponse = BridgeResponsePayload.objects.all().first()
        except Exception as e:
            print(e)
            bridgeResponse = BridgeResponsePayload.objects.none()

        bridgeResponse = BridgeResponsePayload.objects.all().first()
        serializer = BridgeResponseSerializer(bridgeResponse)
        finalR = model_to_dict(bridgeResponse)

        return HttpResponse(json.dumps(finalR))