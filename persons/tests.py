from django.test import TestCase
from .models import Person, Comment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PersonModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_person_creation(self):
        person = Person.objects.create(
            first_name='Jonte',
            last_name='Mdoe',
            age=25,
            location='Nairobi',
            description='Some description',
            is_found=False,
            reported_by=self.user
        )
        self.assertEqual(person.first_name, 'Jonte')
        self.assertEqual(person.last_name, 'Mdoe')
        self.assertEqual(person.age, 25)
        self.assertEqual(person.location, 'Nairobi')
        self.assertEqual(person.description, 'Some description')
        self.assertFalse(person.is_found)
        self.assertEqual(person.reported_by, self.user)

    def test_person_str_representation(self):
        person = Person.objects.create(
            first_name='Jonte',
            last_name='Mdoe',
            age=25,
            location='Nairobi',
            description='Some description',
            is_found=False,
            reported_by=self.user
        )
        self.assertEqual(str(person), 'Mdoe')


    def test_location_field_validation(self):
        with self.assertRaises(ValidationError):
            invalid_person = Person(
                first_name='Jonte',
                last_name='Mdoe',
                age=25,
                location='',  # Invalid location
                description='Some description',
                is_found=False,
                reported_by=self.user
            )
            invalid_person.full_clean()

    def test_reported_by_user_relationship(self):
        person = Person.objects.create(
            first_name='Jonte',
            last_name='Mdoe',
            age=25,
            location='Nairobi',
            description='Some description',
            is_found=False,
            reported_by=self.user
        )
        self.assertEqual(person.reported_by, self.user)
        self.assertIn(person, self.user.persons_reported.all())        


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.person = Person.objects.create(
            first_name='Jonte',
            last_name='Mdoe',
            age=25,
            location='Nairobi',
            description='Some description',
            is_found=False,
            reported_by=self.user
        )



    def test_comment_default_active_value(self):
        comment = Comment.objects.create(
            user=self.user,
            person=self.person,
            comment='Some comment'
        )
        self.assertTrue(comment.active)

    def test_comment_ordering(self):
        comment1 = Comment.objects.create(
            user=self.user,
            person=self.person,
            comment='First comment'
        )
        comment2 = Comment.objects.create(
            user=self.user,
            person=self.person,
            comment='Second comment'
        )
        self.assertGreater(comment2.created, comment1.created)


    # cover field validations and model relationships
    def test_user_relationship(self):
        comment = Comment.objects.create(
            user=self.user,
            person=self.person,
            comment='Some comment'
        )
        self.assertEqual(comment.user, self.user)
        self.assertIn(comment, self.user.comments.all())

    def test_person_relationship(self):
        comment = Comment.objects.create(
            user=self.user,
            person=self.person,
            comment='Some comment'
        )
        self.assertEqual(comment.person, self.person)
        self.assertIn(comment, self.person.comments.all())        
 
