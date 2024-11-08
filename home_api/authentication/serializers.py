from rest_framework.serializers import (
    BooleanField,
    CharField,
    Serializer,
)


class LoginSerializer(Serializer):
    username = CharField(
        max_length=100, style={"placeholder": "Username", "autofocus": True}
    )
    password = CharField(
        max_length=100,
        style={"input_type": "password", "placeholder": "Password"},
    )
    remember_me = BooleanField()
