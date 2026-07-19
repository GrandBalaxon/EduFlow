from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Course, Lesson
from users.models import User


class LessonCRUDTests(APITestCase):
    """ Тесты CRUD операций для уроков. """

    def setUp(self):
        # пользователи
        self.owner = User.objects.create_user(
            email='owner@test.com',
            password='testpass123',
            phone_number='+79001112233',
            city='Москва'
        )
        self.other_user = User.objects.create_user(
            email='other@test.com',
            password='testpass123',
            phone_number='+79004445566',
            city='Питер'
        )
        self.moderator = User.objects.create_user(
            email='moderator@test.com',
            password='testpass123',
            phone_number='+79007778899',
            city='Казань'
        )
        moderator_group, _ = Group.objects.get_or_create(name='Moderator')
        self.moderator.groups.add(moderator_group)

        # курс / урок
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
            owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание тестового урока',
            course=self.course,
            owner=self.owner,
            video_link='https://youtube.com/watch?v=test'
        )

        # URLs
        self.lesson_list_url = reverse('core:lesson_list', kwargs={'course_pk': self.course.pk})
        self.lesson_detail_url = reverse('core:lesson_details', kwargs={'course_pk': self.course.pk, 'pk': self.lesson.pk})
        self.lesson_create_url = reverse('core:lesson_create', kwargs={'course_pk': self.course.pk})
        self.lesson_update_url = reverse('core:lesson_update', kwargs={'course_pk': self.course.pk, 'pk': self.lesson.pk})
        self.lesson_delete_url = reverse('core:lesson_delete', kwargs={'course_pk': self.course.pk, 'pk': self.lesson.pk})


    # метод LIST
    def test_owner_can_list_lessons(self):
        """Владелец может видеть список своих уроков"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_other_user_cannot_list_lessons(self):
        """Другой пользователь не видит чужие уроки"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_moderator_can_list_all_lessons(self):
        """Модератор видит все уроки"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_unauthenticated_cannot_list_lessons(self):
        """Неавторизованный не может смотреть уроки"""
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
