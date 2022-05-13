from rest_framework import serializers

from bridge.models import BridgeResponse, Bridge


class BridgeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BridgeResponse
        fields = '__all__'


class BridgeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bridge
        fields = '__all__'
