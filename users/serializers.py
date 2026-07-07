from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "phone_number",
            "city",
            "avatar"
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
