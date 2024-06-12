from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rockapi.models import Rock, Type
from django.contrib.auth.models import User


class RockView(ViewSet):
    """Rock view set"""

    def create(self, request):
        """Handle POST requests for rocks

        Returns:
            Response: JSON serialized representation of newly created rock
        """

        # get an object instance of a rock type
        type_id = request.data["typeId"]
        type_instance = Type.objects.get(pk=type_id)

        # create a new rock instance
        rock = Rock()

        # assign property values
        rock.user = request.auth.user
        rock.weight = request.data["weight"]
        rock.name = request.data["name"]
        rock.type = type_instance

        try:
            rock.save()
            serialized = RockSerializer(rock, many=False)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
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

# import Type model at the top of the view and serialize it
class RockTypeSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Type
        fields = ( 'label', )

# import Person model at the top of the view and serialize it to expand on Rocks
class RockOwnerSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', )

# and then explicitly tell RockSerializer to use the new type model
class RockSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    # type = RockTypeSerializer(many=False)
    user = RockOwnerSerializer(many=False)
    type = serializers.ReadOnlyField(source='type.label')

    class Meta:
        model = Rock
        fields = ( 'id', 'name', 'weight', 'user', 'type', )