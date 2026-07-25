from rest_framework import serializers
from .models import Pay_data




class Pay_dataSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()
    pay_id = serializers.IntegerField()
    amount = serializers.FloatField()
    sign = serializers.CharField()
    us_key = serializers.CharField(required=False)
    # def create(self, validated_data):
    #     return Pay_data.objects.create(**validated_data)
    # def update(self, instance, validated_data):
    #     instance.order_id = validated_data.get('order_id', instance.order_id)
    #     instance.pay_id = validated_data.get('pay_id', instance.pay_id)
    #     instance.amount = validated_data.get('amount', instance.amount)
    #     instance.us_key = validated_data.get('us_key', instance.us_key)
    #     instance.save()
    #     return instance
    class Meta:
        model = Pay_data
        fields = ('__all__')