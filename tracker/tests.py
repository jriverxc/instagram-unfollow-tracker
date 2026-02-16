import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase


class TrackerViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_process_shows_result_immediately(self):
        followers = [{"string_list_data": [{"value": "alice"}]}]
        following = {"relationships_following": [{"title": "alice"}, {"title": "charlie"}]}

        response = self.client.post(
            '/',
            {
                'followers_file': SimpleUploadedFile('followers_1.json', json.dumps(followers).encode()),
                'following_file': SimpleUploadedFile('following.json', json.dumps(following).encode()),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'charlie')
        self.assertContains(response, 'Descargar CSV')

    def test_download_csv(self):
        response = self.client.post(
            '/download-csv/',
            {'non_followers_json': json.dumps(['charlie'])},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="non_followers.csv"', response['Content-Disposition'])
        self.assertIn('charlie', response.content.decode())
