from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password", "role"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"required": True, "write_only": True, "min_length": 3},
        }

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data.get('first_name',default='')
        last_name = validated_data.get("last_name",default='')

        return User.objects.create_user(
            email=email,password=password,first_name=first_name,last_name=last_name
        )
