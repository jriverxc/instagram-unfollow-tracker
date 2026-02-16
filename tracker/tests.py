import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase


class TrackerViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_view_result(self):
        followers = [{"string_list_data": [{"value": "alice"}]}]
        following = {"relationships_following": [{"title": "alice"}, {"title": "charlie"}]}

        response = self.client.post(
            '/',
            {
                'followers_file': SimpleUploadedFile('followers_1.json', json.dumps(followers).encode()),
                'following_file': SimpleUploadedFile('following.json', json.dumps(following).encode()),
                'action': 'view',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'charlie')

    def test_download_csv(self):
        followers = [{"string_list_data": [{"value": "alice"}]}]
        following = {"relationships_following": [{"title": "alice"}, {"title": "charlie"}]}

        response = self.client.post(
            '/',
            {
                'followers_file': SimpleUploadedFile('followers_1.json', json.dumps(followers).encode()),
                'following_file': SimpleUploadedFile('following.json', json.dumps(following).encode()),
                'action': 'download',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="non_followers.csv"', response['Content-Disposition'])
        self.assertIn('charlie', response.content.decode())
