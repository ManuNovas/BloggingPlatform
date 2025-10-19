from django.test import TestCase

# Create your tests here.
class TestPost(TestCase):
    def test_create_post_success(self):
        response = self.client.post('/posts/', {
            'title': 'Job classes in Final Fantasy',
            'content': 'This article explains the job classes in Final Fantasy.',
            'category': 'Jobs',
            'tags': [
                'Final',
                'Fantasy',
                'Jobs'
            ]
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_create_post_invalid_data(self):
        response = self.client.post('/posts/', {
            'title': 'Job classes in Final Fantasy',
            'category': 'Jobs',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_post_invalid_method(self):
        response = self.client.put('/posts/', {
            'title': 'Job classes in Final Fantasy',
            'content': 'This article explains the job classes in Final Fantasy.',
            'category': 'Jobs',
            'tags': [
                'Final',
                'Fantasy',
                'Jobs'
            ]
        }, content_type='application/json')
        self.assertEqual(response.status_code, 405)
