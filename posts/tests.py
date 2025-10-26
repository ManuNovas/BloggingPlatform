from django.test import TestCase
from django.urls import reverse

from posts.models import Post


# Create your tests here.
class TestPost(TestCase):
    @staticmethod
    def create_post(title=None, content=None, category=None, tags=None):
        return Post.objects.create(title='Job classes in Final Fantasy' if title is None else title,
                                   content='This article explains the job classes in Final Fantasy.' if content is None else content,
                                   category='Jobs' if category is None else category,
                                   tags=['Final', 'Fantasy', 'Jobs'] if tags is None else tags)

    def test_create_post_success(self):
        response = self.client.post(reverse('posts:index'), {
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
        response = self.client.post(reverse('posts:index'), {
            'title': 'Job classes in Final Fantasy',
            'category': 'Jobs',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_post_invalid_method(self):
        response = self.client.put(reverse('posts:index'), {
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

    def test_update_post_success(self):
        post = self.create_post()
        response = self.client.put(reverse('posts:pk', args=[post.id]), {
            'title': 'Job classes in Final Fantasy updated',
            'content': 'This article explains the job classes in Final Fantasy updated.',
            'category': 'Jobs updated',
            'tags': [
                'Final',
                'Fantasy',
                'Jobs',
                'Updated',
            ]
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.get(id=post.id).title, 'Job classes in Final Fantasy updated')

    def test_update_post_invalid_data(self):
        post = self.create_post()
        response = self.client.put(reverse('posts:pk', args=[post.id]), {
            'title': 'Job classes in Final Fantasy updated',
            'category': 'Jobs updated',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Post.objects.get(id=post.id).title, 'Job classes in Final Fantasy')

    def test_update_post_invalid_method(self):
        post = self.create_post()
        response = self.client.post(reverse('posts:pk', args=[post.id]), {
            'title': 'Job classes in Final Fantasy updated',
            'content': 'This article explains the job classes in Final Fantasy updated.',
            'category': 'Jobs updated',
            'tags': [
                'Final',
                'Fantasy',
                'Jobs',
                'Updated',
            ]
        }, content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Post.objects.get(id=post.id).title, 'Job classes in Final Fantasy')

    def test_update_post_not_found(self):
        post = self.create_post()
        response = self.client.put(reverse('posts:pk', args=[1024]), {
            'title': 'Job classes in Final Fantasy updated',
            'content': 'This article explains the job classes in Final Fantasy updated.',
            'category': 'Jobs updated',
            'tags': [
                'Final',
                'Fantasy',
                'Jobs',
                'Updated',
            ]
        }, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Post.objects.get(id=post.id).title, 'Job classes in Final Fantasy')

    def test_delete_post_success(self):
        post = self.create_post()
        response = self.client.delete(reverse('posts:pk', args=[post.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.filter(pk=post.id).exists(), False)

    def test_delete_post_not_found(self):
        post = self.create_post()
        response = self.client.delete(reverse('posts:pk', args=[1024]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Post.objects.filter(pk=post.id).exists(), True)

    def test_get_post_success(self):
        post = self.create_post()
        response = self.client.get(reverse('posts:pk', args=[post.id]), accept='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], post.title)

    def test_get_post_not_found(self):
        self.create_post()
        response = self.client.get(reverse('posts:pk', args=[1024]))
        self.assertEqual(response.status_code, 404)

    def test_get_posts_success(self):
        post = self.create_post()
        response = self.client.get(reverse('posts:index'), accept='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], post.title)

    def test_get_posts_by_term_success(self):
        self.create_post()
        post = self.create_post(
            title='Magic types in Final Fantasy',
            content='This article explains the magic types in Final Fantasy.',
            category='Magic',
            tags=['Final', 'Fantasy', 'Magic']
        )
        response = self.client.get(reverse('posts:index') + '?term=Magic', accept='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], post.title)

    def test_get_posts_by_term_invalid_data(self):
        self.create_post()
        response = self.client.get(reverse('posts:index') + '?term=jo', accept='application/json')
        self.assertEqual(response.status_code, 400)
