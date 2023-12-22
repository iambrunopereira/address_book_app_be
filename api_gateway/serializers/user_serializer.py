from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(source='login.uuid')
    picture = serializers.CharField(source='picture.thumbnail')
    fullName = serializers.SerializerMethodField()
    firstName = serializers.CharField(source='name.first')
    lastName = serializers.CharField(source='name.last')
    email = serializers.EmailField()
    phone = serializers.CharField()
    cell = serializers.CharField()
    gender = serializers.CharField()
    address = serializers.SerializerMethodField()
    nat = serializers.CharField()

    def get_fullName(self, obj):
        return f"{obj['name']['first']} {obj['name']['last']}"

    def get_address(self, obj):
        return {
            "street": obj['location']['street']['number'],
            "city": obj['location']['city'],
            "state": obj['location']['state'],
            "country": obj['location']['country'],
            "postcode": obj['location']['postcode'],
        }
