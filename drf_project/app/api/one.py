from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet

from .serializers import AddressSerializer
from ..models import Address

GenericViewSet


class AddressListApiView(APIView):
    """
    List Address
    """

    def get(self, *args, **kwargs):
        queryset = Address.objects.all()
        serialized_data = AddressSerializer(queryset, many=True)
        return Response(serialized_data.data, status.HTTP_200_OK)


class AddressCreateApiView(APIView):

    """
    Create New Address
    """

    def post(self, request, *args, **kwargs):
        serialized_data = AddressSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(serialized_data.data, status.HTTP_201_CREATED)


class AddressDeleteView(APIView):
    """
    Delete Address
    """

    def delete(self, *args, **kwargs):
        address_obj = get_object_or_404(Address, pk=kwargs.get('pk'))
        if address_obj:
            address_obj.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Address Object doesnot Exist'})


class AddressUpdateView(APIView):
    """
    Update Address
    """

    def patch(self, request, *args, **kwargs):
        ser = AddressSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status.HTTP_200_OK)
