# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.insert
# NOTES:
# 1. This sample code uploads a file and can't be executed via this interface.
#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/guides/code_samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload

import os

from google_auth_oauthlib.flow import Flow

import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "cfg/google_client_id.json"

class PrometeyYouTube():

    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.flow = Flow.from_client_secrets_file(
            client_secrets_file,
            scopes=self.scopes,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob')


    def get_auth_url(self):
        # Tell the user to go to the authorization URL.
        auth_url, _ = self.flow.authorization_url(prompt='consent')
        return auth_url

    def set_auth_code(self, code):
        self.flow.fetch_token(code=code)

    def upload_file(self, path):
        youtube = googleapiclient.discovery.build(
             api_service_name, api_version, credentials=self.flow.credentials, cache_discovery=False)
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "categoryId": "22",
                    "description": "Description of uploaded video.",
                    "title": "Test video upload."
                },
                "status": {
                    "privacyStatus": "private"
                }
            },
            #       with a pointer to the actual file you are uploading.
            media_body=MediaFileUpload(path)
        )
        response = request.execute()
        return response

if __name__ == "__main__":
    youtube = PrometeyYouTube()
    print(youtube.get_auth_url())
    youtube.set_auth_code(input())
    print(youtube.upload_file('22test2-landscape.mp4'))