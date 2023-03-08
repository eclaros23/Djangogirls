from django.test import TestCase
from .models import Post
from django.contrib.auth import get_user_model # author
from django.utils.timezone import now
User = get_user_model()

class PostListTest (TestCase):
  def setUp(self): # setting up username and password for every test
      user = User.objects.create(username = "test_user")
      user.set_password("password123")
      user.save()
      self.client.login(username = "test_user", password = "password123")
    
  def test_noteposts(self): 
      """When there are no posts on the page then the page loads successfully"""
      response = self.client.get("/") # url 
      self.assertEqual(response.status_code, 200) # django assertEqual method (status code of 200 = success)
      self.assertEqual(response.context["posts"].count(), 0) #loading list of posts without posts

  def test_postsvisible(self): 
      """When there are posts on the page then the page loads successfully"""
      author = User.objects.create(username = "user1") # author created
      Post.objects.create(title = "Post1", text = "Hello", author = author, published_date = now())
      Post.objects.create(title = "Post2", text = "Great", author = author)
      response = self.client.get("/") # url of a page is /
      self.assertEqual(response.status_code, 200) # check if page loaded successfully (status code of 200 = success)
      self.assertEqual(response.context["posts"].count(), 1) # checking that there is one post on page

  def test_loggedout(self):
      """When user is logged out they should be able to read posts"""
      self.client.logout()
      author = User.objects.create(username = "user1") # author created
      Post.objects.create(title = "Post1", text = "Hello", author = author, published_date = now())
      Post.objects.create(title = "Post2", text = "Great", author = author)
      response = self.client.get("/") # url of a page is /
      self.assertEqual(response.status_code, 200) # check if page loaded successfully (status code of 200 = success)
      self.assertEqual(response.context["posts"].count(), 1) # checking that there is one post on page


class PostDetailTest (TestCase):
  def setUp(self): # setting up username and password for every test
      user = User.objects.create(username = "test_user")
      user.set_password("password123")
      user.save()
      self.client.login(username = "test_user", password = "password123")

  def test_postpublished(self):
    """If a post is published then the user should see it"""
    author = User.objects.create(username = "user1") # author created
    published_post = Post.objects.create(title = "Post01", text = "Hey", author = author, published_date = now())
    response = self.client.get(f"/post/{published_post.pk}/") # f string allows you to put things in {}
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context["post"], published_post)

  def test_postunpublished(self):
    """If a post is unpublished then the user should not see it"""
    author = User.objects.create(username = "user1")
    unpublished_post = Post.objects.create(title = "Post02", text = "Great", author = author)
    response = self.client.get(f"/post/{unpublished_post.pk}/")
    self.assertEqual(response.status_code, 404) # 404 means not found

  def test_loggedout(self):
      """When user is logged out they should be able to read published posts but not unpublished posts"""
      self.client.logout()
      author = User.objects.create(username = "user1") 
      published_post = Post.objects.create(title = "Post01", text = "Hey", author = author, published_date = now())
      response = self.client.get(f"/post/{published_post.pk}/") 
      self.assertEqual(response.status_code, 200) 
      unpublished_post = Post.objects.create(title = "Post02", text = "Great", author = author)
      response = self.client.get(f"/post/{unpublished_post.pk}/") 
      self.assertEqual(response.status_code, 404) 

  def test_doesnotexist(self):
      """If the user requests a page that does not exist there should be an error""" 
      response = self.client.get("/post/1000000/")
      self.assertEqual(response.status_code, 404)
      response = self.client.get("/post/!/")
      self.assertEqual(response.status_code, 404)

class PostEdit(TestCase):
  def setUp(self): # setting up username and password for every test
      user = User.objects.create(username = "test_user")
      user.set_password("password123")
      user.save()
      self.client.login(username = "test_user", password = "password123")

  def test_get_postpublished(self):
    """If a post is published then the user should see it"""
    author = User.objects.create(username = "user1") 
    published_post = Post.objects.create(title = "Post01", text = "Hey", author = author, published_date = now())
    response = self.client.get(f"/post/{published_post.pk}/edit/") 
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context["form"].instance, published_post)

  def test_get_postunpublished(self):
    """If a post is unpublished then the user should not see it"""
    author = User.objects.create(username = "user1")
    unpublished_post = Post.objects.create(title = "Post02", text = "Great", author = author)
    response = self.client.get(f"/post/{unpublished_post.pk}/edit/")
    self.assertEqual(response.status_code, 200)

  def test_get_loggedout(self):
    """If user is logged out they won't be able to edit posts"""
    self.client.logout()
    author = User.objects.create(username = "user1") 
    published_post = Post.objects.create(title = "Post01", text = "Hey", author = author, published_date = now())
    response = self.client.get(f"/post/{published_post.pk}/edit/") 
    self.assertEqual(response.status_code, 404) 
    unpublished_post = Post.objects.create(title = "Post02", text = "Great", author = author)
    response = self.client.get(f"/post/{unpublished_post.pk}/edit/") 
    self.assertEqual(response.status_code, 404) 

  def test_post_published(self):
    """If a post is published then the user should be able to edit posts"""
    author = User.objects.create(username = "user1") 
    published_post = Post.objects.create(title = "Post01", text = "Hey", author = author, published_date = now())
    response = self.client.post(f"/post/{published_post.pk}/edit/", {"title": "new title", "text": "new text"}) 
    self.assertRedirects(response, f"/post/{published_post.pk}/")
    published_post.refresh_from_db()
    self.assertEqual(published_post.title, "new title")
    self.assertEqual(published_post.text, "new text")

  def test_post_unpublished(self):
    """If a post is unpublished then the user should be able to edit it"""
    author = User.objects.create(username = "user1")
    unpublished_post = Post.objects.create(title = "Post02", text = "Great", author = author)
    response = self.client.post(f"/post/{unpublished_post.pk}/edit/", {"title": "new title", "text": "new text"})
    self.assertRedirects(response, f"/post/{unpublished_post.pk}/")
    unpublished_post.refresh_from_db()
    self.assertEqual(unpublished_post.title, "new title")
    self.assertEqual(unpublished_post.text, "new text")

  def test_post_loggedout(self):
    """If user is logged out they won't be able to edit posts"""
    self.client.logout()
    author = User.objects.create(username = "user1") 
    published_post = Post.objects.create(title = "Post01", text = "Hey", author = author, published_date = now())
    response = self.client.post(f"/post/{published_post.pk}/edit/") 
    self.assertEqual(response.status_code, 404) 
    unpublished_post = Post.objects.create(title = "Post02", text = "Great", author = author)
    response = self.client.post(f"/post/{unpublished_post.pk}/edit/") 
    self.assertEqual(response.status_code, 404) 

  def test_post_nonexistent(self):
    """If post does not exist the user won't be able to edit posts"""
    response = self.client.post("/post/1000000/edit/")
    self.assertEqual(response.status_code, 404)
    response = self.client.post("/post/!!!!!/edit/")
    self.assertEqual(response.status_code, 404)
  
class PostNewTest (TestCase):
  def setUp(self): # setting up username and password for every test
      user = User.objects.create(username = "test_user")
      user.set_password("password123")
      user.save()
      self.client.login(username = "test_user", password = "password123")

  def test_get(self):
    """Getting the page to create a new post"""
    response = self.client.get('/post/new/') 
    self.assertEqual(response.status_code, 200)

  def test_post_invalid_data(self):
    """Getting the page to create a new post"""
    response = self.client.post('/post/new/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context["form"].errors, {"title": ["This field is required."], "text": ["This field is required."]})

  def test_post_valid_data(self):
    response = self.client.post('/post/new/', {"title": "new title", "text": "new text"})
    new_post = Post.objects.get(title = "new title", text = "new text")
    self.assertRedirects(response,f"/post/{new_post.pk}/")

  def test_post_loggedout(self):
    """If user is not logged in they should not create new posts"""
    self.client.logout() 
    response = self.client.post("/post/new/")
    self.assertEqual(response.status_code, 404)
    response = self.client.post("/post/new/", {"title": "new title", "text": "new text"})
    self.assertEqual(response.status_code, 404)

  def test_post_title_exists(self):
    """If user creates post with the same title as another post that exists they should get an error"""
    response = self.client.post('/post/new/')
    author = User.objects.create(username = "user1") 
    published_post = Post.objects.create(title = "Post01", text = "Good", author = author)
    response = self.client.post('/post/new/', {"title": "Post01", "text": "Good"})
    self.assertEqual(response.context["form"].errors, {"__all__": ["Post Title Exists!"]})
    self.assertEqual(response.status_code, 200)
    unpublished_post = Post.objects.create(title = "Post02", text = "Great", author = author)
    response = self.client.post('/post/new/', {"title": "Post02", "text": "Nice"})
    self.assertEqual(response.context["form"].errors, {"__all__": ["Post Title Exists!"]})
    self.assertEqual(response.status_code, 200)