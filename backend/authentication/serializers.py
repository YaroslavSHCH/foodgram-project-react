from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer


class EmailAuthTokenSerializer(AuthTokenSerializer):
    username = None
    email = serializers.CharField(label=("Email"))
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = ('Не удалось распознать комбинацию для входа.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('"email" и "password" обязательные поля.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
