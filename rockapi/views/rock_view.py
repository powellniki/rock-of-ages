from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rockapi.models import Rock, Type


class RockView(ViewSet):
    """Rock view set"""


    def create(self, request):
        """Handle POST operations"""

        # get the related types from the database using the request body value
        type_id = request.data["typeId"]
        type_instance = Type.objects.get(pk=type_id)

        # create a new rock instance
        rock = Rock()

        # assign the values for each 
        # use Rock instance as the value of the model property
        rock.user = request.auth.user
        rock.weight = request.data["weight"]
        rock.name = request.data["name"]
        rock.type = type_instance


        try:
            rock.save()
            serializer = RockSerializer(rock)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        # You will implement this feature in a future chapter

        # return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            rocks = Rock.objects.all()
            serializer = RockSerializer(rocks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class RockSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Rock
        fields = ( 'id', 'name', 'weight', 'type', )