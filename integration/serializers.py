from rest_framework import serializers

class AddNoteForPersonSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=10000,allow_null=False,allow_blank=False,required=True)
    person_id = serializers.IntegerField(allow_null=False,required=True)

class UpdatePersonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10000,allow_null=False,allow_blank=False,required=True)
    owner_id = serializers.IntegerField(allow_null=False,required=True)
    org_id = serializers.IntegerField(allow_null=False,required=True)
    email = serializers.ListField(
        child=serializers.EmailField(allow_null=False,allow_blank=False,required=True),
        allow_null=False,
        allow_empty=True,
        required=True
    )
    phone = serializers.ListField(
        child=serializers.CharField(max_length=10,allow_null=False,allow_blank=False,required=True),
        allow_null=False,
        allow_empty=True,
        required=True
    )
    visible_to = serializers.CharField(max_length=10000,allow_null=False,allow_blank=False,required=True)



