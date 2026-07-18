from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone_number", "city", "avatar"]


class UserPrivateSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "phone_number", "city", "avatar", "payments"]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'validators': [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="Пользователь с таким email уже существует."
                    )
                ]
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
