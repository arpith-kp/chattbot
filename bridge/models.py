import uuid

from django.db import models
from django.http import JsonResponse

'''

{
  "requestId": "UUID",
  "requestedAction": "SET_PERMISSIONS",
  "requestPayload":{
    "folderName": "",
    "userName": "",
    "priv": "READ|READWRITE|RWD"
  }
}


{
  
  "requestId": "UUID",
  "requestedAction": "SET_PERMISSIONS"
  "statusCode": 200, 
  "responsePayload" : {
   “responseStatus": “AMBIGUOUS",
“originalRequest" : :{
    "folderName": "",
    "userName": "",
    “priv": "READ|READWRITE|RWD"
  },
 “folderPaths" : [
{“folderName":"abc",
“folderPath":"/s/g/abc"},
{“folderName":"abcdef",
“folderPath":"/s/g/abcdef"}
]
}
  "errors": {
    "message": ""
  }
    
}


'''
# Create your models here.
class Payload(models.Model):
    pid  =models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    folderName = models.CharField(max_length=1000, blank=False)
    userName = models.CharField(max_length=10000, blank=False)
    priv = models.CharField(max_length=100, blank=False)


class Bridge(models.Model):
    requestId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requestedAction = models.CharField(max_length=1000, blank=False)
    requestedPayload = models.ForeignKey(Payload, on_delete=models.CASCADE)


class BridgeResponseFolders(models.Model):
    folderId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    folderPath = models.FilePathField()


class BridgeResponseErrorPayload(models.Model):
    errorId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.CharField(max_length=10000, blank=True, null=True)


class BridgeResponsePayload(models.Model):
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    responseStatus = models.CharField(max_length=100, blank=False)
    originalRequest = models.OneToOneField(Payload, on_delete=models.CASCADE)
    folderPaths = models.ForeignKey(BridgeResponseFolders, on_delete=models.CASCADE)
    errors = models.OneToOneField(BridgeResponseErrorPayload, on_delete=models.CASCADE)


class BridgeResponse(models.Model):
    requestId = models.UUIDField(primary_key=True)
    requestedAction = models.CharField(max_length=1000, blank=False)
    statusCode = models.CharField(max_length=100, blank=False)
    responsePayload = models.ForeignKey(BridgeResponsePayload, on_delete=models.CASCADE)

    def __str__(self):
        return JsonResponse(self)