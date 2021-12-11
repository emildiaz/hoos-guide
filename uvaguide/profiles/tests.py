from django.test import TestCase
from .models import Profile
from django.test import TestCase, Client
from django.contrib.auth.models import User
from maps.models import Place, Review

"""
Test for creating a profile for a user
"""

class ProfileTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='b27', password='password')
        self.client1 = Client()
        self.client1.force_login(self.user1)
        #make a profile object
        self.profile1=Profile.objects.create(
            user=self.user1,
            pfp ="",
            bio = "xxxx"
        )
        self.profile1.save()
        
        self.user2 = User.objects.create_user(username='b28', password='password')
        self.client2 = Client()
        self.client2.force_login(self.user2)
        #make a profile object
        self.profile2=Profile.objects.create(
            user=self.user2,
            pfp ="",
            bio = "yyyyy"
        )
        self.profile2.save()
        self.response1 = self.client1.get('/profile/') 
        self.response2 = self.client2.get('/profile/')

    def test_profile_page_loads(self):
        status1 = self.response1.status_code
        status2 = self.response2.status_code

        self.assertEquals(status1, 200, "Page failed to load for user1.")
        self.assertEquals(status2, 200, "Page failed to load for user2.")

    def test_correct_profile_loads(self):
        name1 = self.response1.context['user'].username
        name2 = self.response2.context['user'].username

        self.assertEquals(name1, self.profile1.user.username, "Wrong Profile loads.")
        self.assertEquals(name2, self.profile2.user.username, "Wrong Profile loads.")

    def test_profile_fields_load(self):
        name = self.response1.context['user_profile'].user.username
        bio = self.response1.context['user_profile'].bio
        
        self.assertEquals(name, self.profile1.user.username, "Wrong Profile name.")
        self.assertIn(bio, self.profile1.bio, "Wrong Profile bio.")

    # def test_add_friends_correctness(self):
    #     friend = Profile.objects.get(User.username=="b28")
    #     self.profile1.friends.add(friend.user)
    #     self.profile1.save()
        

class FriendsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='b27', password='password')
        self.profile1=Profile.objects.create(
            username='b27',
            user=self.user1,
            pfp ="",
            bio = "xxxx"
        )
        self.profile1.save()
        self.user2 = User.objects.create_user(username='b28', password='password')
        self.profile2=Profile.objects.create(
            username='b28',
            user=self.user2,
            pfp ="",
            bio = "yyyyy"
        )
        self.profile2.save()

        self.client = Client()
        self.client.force_login(self.user1)
        self.response = self.client.get('/profile/friends/') 
    
    def test_friends_page_loads(self):
        status = self.response.status_code
        self.assertEqual(status, 200, "Friends page did not load.")
    
    def test_all_possible_friends_loaded_on_page(self):
        name1 = self.profile1.username
        name2 = self.profile2.username
        html = str(self.response.content)

        self.assertEquals(len(Profile.objects.all()), 2, "Not all profiles saved.")
        self.assertNotIn(name1, html, "User1 in friends page when logged in")
        self.assertIn(name2, html, "User2 not in friends page")
    
    def test_add_friend_button_disappearing_after_already_friends(self):
        self.profile1.friends.add(self.user2)
        html = str(self.client.get('/profile/friends/').content)
        friend_req_sent = "Friend Request Sent!"
        self.assertIn(friend_req_sent, html, "Add Friend button remains after sent friend request.")
    
    def test_add_friend_button_present_for_non_friends(self):
        html = str(self.response.content)
        add_friend = "Add Friend"
        self.assertIn(add_friend, html, "Add Friend button not available.")

"""
TESTS FOR THE RECENT ACTIVITIES SECTION ON PROFILE PAGE
"""
class RecentActivitiesTest(TestCase):
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
        self.client = Client()
        self.client.login(username='b27', password='password')
        self.response = self.client.get(f'/profile/')
        self.html = str(self.response.content)
    
    def test_no_recent_activities(self):
        no_recent_activity = 'No Recent Activity!'
        self.assertIn(no_recent_activity, self.html, "There is an activity when there should not be.")
    
    def test_comment_activity(self):
        review1 = Review.objects.create(
            author = self.profile,
            place = self.place1,
            content="i love the rotunda",
        )
        review1.save()
        new_response = self.client.get('/profile/')
        self.assertIn(review1.content, str(new_response.content), "Comment did not show up in recent activities.")
    
    def test_like_activity(self):
        self.place1.likes.add(self.profile)
        self.place1.save()
        like_message = f'<small>liked <span style="color: #E57200;">{self.place1.name}</span></small>'
        new_response = self.client.get('/profile/')
        self.assertIn(like_message, str(new_response.content), "Like did not show up in recent activities.")