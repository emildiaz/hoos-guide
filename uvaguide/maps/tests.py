from django.test import TestCase, Client
from .models import Place,Review,Profile,User
from maps.forms import ReviewForm

# """
# Tests for the places albums
# """
class PlacesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='b27', password='password')
        self.client = Client()
        self.client.force_login(self.user)
        #make Place objects
        self.place1 = Place(
            name="Rotunda", 
            address="123 Rotunda", 
            image="",
            description="fun place"
            )
        self.place1.save()
        self.response = self.client.get('/places/')
    
    def test_places_page_loads(self):
        status = self.response.status_code
        self.assertEquals(status, 200, "Page failed to load.")

    def test_all_place_objects_on_default_page(self):
        self.assertIn(self.place1.name, str(self.response.content))
    
    def test_place_not_on_page(self):
        search = self.client.get('/places/?search=Eiffel+Tower')
        self.assertEquals(search.status_code, 200, "Page failed to load.")
        self.assertIn("No place matches your search!", str(search.content))
    
    def test_search_on_valid_place(self):
        search = self.client.get('/places/?search=Rotunda')
        self.assertIn(self.place1.name, str(search.content))
        
# """Rice
# Tests for the detailed Reviews"
# """
class ReviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='b27', password='password')
        self.profile = Profile.objects.create(
            user=self.user,
            pfp="",
            bio="i am b27"
        )
        self.profile.save()
        self.place1 = Place(
            name="Rotunda", 
            address="123 Rotunda", 
            image="",
            description="fun place"
            )
        self.place1.save()
        self.review1 = Review.objects.create(
            author = self.profile,
            place = self.place1,
            content="i love the rotunda",
        )
        self.review1.save()
        self.client = Client()
        self.client.login(username='b27', password='password')
        self.response = self.client.get(f'/places/{self.place1.id}/')
        self.html = str(self.response.content)

    def test_review_page_loads(self):
        status = self.response.status_code
        self.assertEquals(status, 200, "Page failed to load.")
    
    def test_correct_place_loads(self):
        place = self.response.context['place']
        self.assertEquals(place, self.place1, "Wrong place loads.")

    def test_place_fields_load(self):
        name = self.place1.name
        description = self.place1.description
        address = self.place1.address
        
        self.assertIn(name, self.html)
        self.assertIn(description, self.html)
        self.assertIn(address, self.html)
    
    def test_review_on_page(self):
        review_author = self.review1.author.username
        review_content = self.review1.content
        self.assertIn(review_author, self.html)
        self.assertIn(review_content, self.html)
    
    def test_review_form_invalid(self):
        form_data = {'author': 'what a wonderful place'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_review_form_valid(self):
        form_data = {'content': 'what a wonderful place'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_review_submission_on_page(self):
        content = 'what a wonderful place'
        form_data = {'content': content}
        submission_response = self.client.post(f'/places/{self.place1.id}/', data=form_data)

        self.assertEqual(submission_response.status_code, 200, "Page failed to load after submission.")
        self.assertIn(content, str(submission_response.content), "New review not in page.")
        self.assertEqual(len(Review.objects.all()), 2, "Wrong amount of review objects.")