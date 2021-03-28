from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation, authenticate
from users.models import Offer, AthleteFile
from django import forms
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer
from  django.core.mail import send_mail

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password1 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "url",
            "id",
            "email",
            "username",
            "password",
            "password1",
            "athletes",
            "coach",
            "workouts",
            "coach_files",
            "athlete_files",
        ]

    def validate_password(self, value):
        data = self.get_initial()

        password = data.get("password")
        password1 = data.get("password1")

        try:
            password_validation.validate_password(password)
        except forms.ValidationError as error:
            raise serializers.ValidationError(error.messages)

        if password != password1:
            raise serializers.ValidationError("Passwords must match!")

        return value

    def validate_username(self, value):
        data = self.get_initial()

        username = data.get("username")
        if len(username) < 4 or len(username) > 21:
            raise serializers.ValidationError("Username must be at least 5 characters long, but no longer than 21!")

        return value

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        send_mail("Test", "/activate/uid/token", None, [email], fail_silently=False,)
        user_obj = get_user_model()(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

class UserGetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "url",
            "id",
            "email",
            "username",
            "athletes",
            "coach",
            "workouts",
            "coach_files",
            "athlete_files",
        ]


class UserPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["athletes"]

    def update(self, instance, validated_data):
        athletes_data = validated_data["athletes"]
        instance.athletes.set(athletes_data)

        return instance

User = get_user_model()

class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        # We changed only below line
        if self.user: # and self.user.is_active: 
            return attrs
        self.fail("invalid_credentials")


class AthleteFileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = AthleteFile
        fields = ["url", "id", "owner", "file", "athlete"]

    def create(self, validated_data):
        return AthleteFile.objects.create(**validated_data)


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Offer
        fields = [
            "url",
            "id",
            "owner",
            "recipient",
            "status",
            "timestamp",
        ]
