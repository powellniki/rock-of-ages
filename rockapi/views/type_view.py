"""View module for handling requests for type data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rockapi.models import Type


class TypeView(ViewSet):
    """Rock API types view"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        type = Type()
        type.label = request.data["label"]

        try:
            type.save()
            serializer = TypeSerializer(type)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request):
        """Handle GET requests to get all types

        Returns:
            Response -- JSON serialized list of types
        """

        types = Type.objects.all()
        serialized = TypeSerializer(types, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single type

        Returns:
            Response -- JSON serialized type record
        """

        rock_type = Type.objects.get(pk=pk)
        serialized = TypeSerializer(rock_type)
        return Response(serialized.data, status=status.HTTP_200_OK)


class TypeSerializer(serializers.ModelSerializer):
    """JSON serializer for types"""
    class Meta:
        model = Type
        fields = ('id', 'label',)