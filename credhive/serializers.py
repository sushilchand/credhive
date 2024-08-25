from rest_framework import serializers


# Base Serializer to define common fields like id
class BaseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        abstract = True
