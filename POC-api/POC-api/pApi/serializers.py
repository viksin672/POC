from rest_framework import serializers
from pApi.models import clients


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = clients
        fields = ('title','description','client','priority','date','area')

