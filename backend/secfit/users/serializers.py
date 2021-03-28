from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from users.models import Offer, AthleteFile
from django import forms
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from verify_email.email_handler import send_verification_email


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
            "is_active",
            "athletes",
            "coach",
            "workouts",
            "coach_files",
            "athlete_files",
        ]

    def validateLogin(self):
        # https://docs.djangoproject.com/en/1.10/topics/auth/customizing/
        user = authenticate(username='john', password='snow')
        if user is not None:  
            if user.is_active:   
                # Denne fjernes og byttes ut med linje 19 av sikkerhetsårsaker
                print("User is valid, active and authenticated")
            else:
                print("The password is valid, but the account has been disabled")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect. Have you remembered to activate your account?")

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
        # TODO: Send Email verification

        send_mail("Subject", "Message", None, ["livia.e.v.stokke@ntnu.no"], fail_silently=False,)
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
