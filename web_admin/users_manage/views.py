from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import Pay_dataSerializer
from .models import Pay_data
from hashlib import md5





class CartItemViews(APIView):
    def get(self, request):
        return Response( 'Ваш баланс будет пополнен в течении 3 мин.')
    def post(self, request):
        # print(request.data.get("order_id"))
        data = {"order_id":request.data.get("order_id"),  "pay_id": request.data.get("pay_id"), "amount": request.data.get("amount"), "sign": request.data.get("sign"),"us_key":12,}
       
   
        serializer = Pay_dataSerializer(data=data )
       
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            # return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)