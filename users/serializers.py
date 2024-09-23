from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password_first = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_second = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password_first', 'password_second', 'email', 'first_name', 'last_name', 'username')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password_first'] != attrs['password_second']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password_first'])
        user.save()
        return user