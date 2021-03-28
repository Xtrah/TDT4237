from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

class EmailVerificationTest(APITestCase):

    # endpoints needed
    register_url = "/api/v1/users/"
    activate_url = "/api/v1/users/activation/"
    login_url = "/api/v1/token/login/"
    user_details_url = "/api/v1/users/"
    # user information
    user_data = {
        "username": "matsfi", 
        "email": "liviaemilie@yahoo.no", 
        "password": "Bolle1234",
        "password1": "Bolle1234",
        "athletes": [
        ],
        "workouts": [
        ],
        "coach_files": [
        ],
        "athlete_files": [
        ]
    }
    login_data = {
        "username": "matsfi", 
        "password": "Bolle1234"
    }

    def test_register_with_email_verification(self):
        # register the new user
        print(self.user_data)
        response = self.client.post(self.register_url, self.user_data, format="json")

        # expected response 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # expected one email to be sent
        self.assertEqual(len(mail.outbox), 1)
        
        # parse email to get uid and token
        email_lines = mail.outbox[0].body.splitlines()
        print(email_lines)
        # you can print email to check it
        # print(mail.outbox[0].subject)
        # print(mail.outbox[0].body)
        activation_link = [l for l in email_lines if "/activate/" in l][0]
        uid, token = activation_link.split("/")[-2:]
        
        # verify email
        data = {"uid": uid, "token": token}
        response = self.client.post(self.activate_url, data, format="json")
        print(f"uid: {uid} token: {token}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # login to get the authentication token
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertTrue("auth_token" in response.json())
        token = response.json()["auth_token"]

        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # get user details
        response = self.client.get(self.user_details_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["email"], self.user_data["email"])
        self.assertEqual(response.json()[0]["username"], self.user_data["username"])