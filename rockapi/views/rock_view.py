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

        # Get query string parameter
        owner_only = self.request.query_params.get("owner", None)

        try:
            # Start with all rows
            rocks = Rock.objects.all()

            # If `?owner=current` is in the URL
            if owner_only is not None and owner_only == "current":
                # Filter to only the current user's rocks
                rocks = rocks.filter(user=request.auth.user)

            serializer = RockSerializer(rocks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
            

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            rock = Rock.objects.get(pk=pk)
            if rock.user.id == request.auth.user.id:
                rock.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'You do not own that rock'}, status=status.HTTP_403_FORBIDDEN)

        except Rock.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


    user = RockOwnerSerializer(many=False)
    # because type has a relationship field (foreign key to rock model), need to specify how to serialize this relationship:
    # type = serializers.ReadOnlyField(source='type.label') #example for a FK field
    type = RockTypeSerializer(many=False)

    class Meta:
        model = Rock
        fields = ( 'id', 'name', 'weight', 'user', 'type', )