from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

# Tests retrieved from https://saasitive.com/tutorial/django-rest-framework-reset-password/

class PasswordResetTest(APITestCase):
    
    # endpoints needed
    register_url = "/api/v1/users/"
    activate_url = "/api/v1/users/activation/"
    login_url = "/api/v1/token/login/"
    send_reset_password_email_url = "/api/v1/users/reset_password/"
    confirm_reset_password_url = "/api/v1/users/reset_password_confirm/"
    
    # user infofmation
    user_data = {
        "email": "test@example.com", 
        "username": "test_user", 
        "password": "verysecret"
    }
    login_data = {
        "username": "test_user", 
        "password": "verysecret"
    }

    def test_reset_password(self):
        # register the new user
        response = self.client.post(self.register_url, self.user_data, format="json")
        # expected response 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # expected one email to be send
        self.assertEqual(len(mail.outbox), 1)
        
        # parse email to get uid and token
        email_lines = mail.outbox[0].body.splitlines()
        activation_link = [l for l in email_lines if "/activate/" in l][0]
        uid, token = activation_link.split("/")[-2:]
        
        # verify email
        data = {"uid": uid, "token": token}
        response = self.client.post(self.activate_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # reset password
        data = {"email": self.user_data["email"]}
        response = self.client.post(self.send_reset_password_email_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # parse reset-password email to get uid and token
        # it is a second email!
        email_lines = mail.outbox[1].body.splitlines()
        reset_link = [l for l in email_lines if "/reset_password/" in l][0]
        uid, token = activation_link.split("/")[-2:]

        # confirm reset password
        data = {"uid": uid, "token": token, "new_password": "NewPassword1234"}
        response = self.client.post(self.confirm_reset_password_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # login to get the authentication token with old password
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # login to get the authentication token with new password
        login_data = dict(self.login_data)
        login_data["password"] = "NewPassword1234"
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_inactive_user(self):
        # register the new user
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # reset password for inactive user
        data = {"email": self.user_data["email"]}
        response = self.client.post(self.send_reset_password_email_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # the email wasnt sent
        self.assertEqual(len(mail.outbox), 1)
    
    def test_reset_password_wrong_email(self):
        data = {"email": "wrong@email.com"}
        response = self.client.post(self.send_reset_password_email_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # the email wasnt send
        self.assertEqual(len(mail.outbox), 0)

class EmailVerificationTest(APITestCase):

    # endpoints needed
    register_url = "/api/v1/users/"
    activate_url = "/api/v1/users/activation/"
    login_url = "/api/v1/token/login/"
    user_details_url = "/api/v1/users/"
    resend_verification_url = "/api/v1/users/resend_activation/"
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
        user_details = response.json()["results"]
        # self.assertEqual(len(response.json()), 1) expected json must have changed
        self.assertEqual(user_details[0]["email"], self.user_data["email"])
        self.assertEqual(user_details[0]["username"], self.user_data["username"])

        
    def test_register_resend_verification(self):
        # register the new user
        response = self.client.post(self.register_url, self.user_data, format="json")
        # expected response 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # expected one email to be send
        self.assertEqual(len(mail.outbox), 1)

        # login to get the authentication token
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertTrue("auth_token" in response.json())
        token = response.json()["auth_token"]
        print(response.json())

        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # try to get user details
        response = self.client.get(self.user_details_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # clear the auth_token in header
        self.client.credentials()
        # resend the verification email
        data = {"email": self.user_data["email"]}
        response = self.client.post(self.resend_verification_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # there should be two emails in the outbox
        self.assertEqual(len(mail.outbox), 2)

        # parse the last email
        email_lines = mail.outbox[1].body.splitlines()
        activation_link = [l for l in email_lines if "/activate/" in l][0]
        uid, token = activation_link.split("/")[-2:]
        
        # verify the email
        data = {"uid": uid, "token": token}
        response = self.client.post(self.activate_url, data, format="json")
        # email verified
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
    def test_resend_verification_wrong_email(self):
        # register the new user
        response = self.client.post(self.register_url, self.user_data, format="json")
        # expected response 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # resend the verification email but with WRONG email
        data = {"email": self.user_data["email"]+"_this_email_is_wrong"}
        response = self.client.post(self.resend_verification_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_activate_with_wrong_uid_token(self):
        # register the new user
        response = self.client.post(self.register_url, self.user_data, format="json")
        # expected response 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # verify the email with wrong data
        data = {"uid": "wrong-uid", "token": "wrong-token"}
        response = self.client.post(self.activate_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

