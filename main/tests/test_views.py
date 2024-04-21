from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class PageTests(SimpleTestCase):

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_csrf_token_in_context(self):
        response = self.client.get('/')
        self.assertTrue('csrf_token' in response.context)

class LoginRequiredTests(TestCase):
    fixtures = ['main.json']

    def test_redirect_where_nonlogin(self):
        response = self.client.get("/post/5/")
        self.assertEqual(response.status_code, 302)

    def test_access_where_login(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/post/5/')
        self.assertEqual(response.status_code, 200)

    def test_used_correct_template(self):
        response = self.client.get("/posts/")
        self.assertTemplateUsed(response, 'main/post_list.html')