from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Course, Lesson
from users.models import User, Subscription


class BaseTestCase(APITestCase):
    """ Базовый класс с общими тестовыми данными. """
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


class LessonCRUDTestCase(BaseTestCase):
    """ Тесты CRUD операций для уроков. """
    def setUp(self):
        super().setUp()
        # URLs
        self.lesson_list_url = reverse('core:lesson_list', kwargs={'course_pk': self.course.pk})
        self.lesson_detail_url = reverse('core:lesson_details', kwargs={'course_pk': self.course.pk, 'pk': self.lesson.pk})
        self.lesson_create_url = reverse('core:lesson_create', kwargs={'course_pk': self.course.pk})
        self.lesson_update_url = reverse('core:lesson_update', kwargs={'course_pk': self.course.pk, 'pk': self.lesson.pk})
        self.lesson_delete_url = reverse('core:lesson_delete', kwargs={'course_pk': self.course.pk, 'pk': self.lesson.pk})


    # метод LIST
    def test_owner_can_list_lessons(self):
        """ Владелец может видеть список своих уроков """
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_other_user_cannot_list_lessons(self):
        """ Другой пользователь не видит чужие уроки """
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_moderator_can_list_all_lessons(self):
        """ Модератор видит все уроки """
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_unauthenticated_cannot_list_lessons(self):
        """ Неавторизованный не может смотреть уроки """
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # метод CREATE
    def test_owner_can_create_lesson(self):
        """ Владелец курса может создать урок """
        self.client.force_authenticate(user=self.owner)
        data = {
            'title': 'Новый урок',
            'description': 'Описание нового урока',
            'course': self.course.pk,
            'video_link': 'https://youtube.com/watch?v=new'
        }
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.last().owner, self.owner)

    def test_other_user_cannot_create_lesson_in_foreign_course(self):
        """ Другой пользователь не может создать урок в чужом курсе """
        self.client.force_authenticate(user=self.other_user)
        data = {
            'title': 'Урок от другого',
            'description': 'Описание',
            'video_link': 'https://youtube.com/watch?v=other',
            'course': self.course.pk
        }
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_moderator_cannot_create_lesson(self):
        """ Модератор не может создавать уроки """
        self.client.force_authenticate(user=self.moderator)
        data = {
            'title': 'Урок от модератора',
            'description': 'Описание',
            'course': self.course.pk
        }
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_create_lesson(self):
        """ Неавторизованный не может создать урок """
        data = {
            'title': 'Анонимный урок',
            'description': 'Описание',
            'course': self.course.pk
        }
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # метод UPDATE
    def test_owner_can_update_lesson(self):
        """ Владелец может обновить свой урок """
        self.client.force_authenticate(user=self.owner)
        data = {'title': 'Обновлённый урок', 'description': 'Новое описание'}
        response = self.client.patch(self.lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Обновлённый урок')

    def test_other_user_cannot_update_lesson(self):
        """ Другой пользователь не может обновить чужой урок """
        self.client.force_authenticate(user=self.other_user)
        data = {'title': 'Взломанный урок'}
        response = self.client.patch(self.lesson_update_url, data)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_moderator_can_update_any_lesson(self):
        """ Модератор может обновить любой урок """
        self.client.force_authenticate(user=self.moderator)
        data = {'title': 'Отредактировано модератором'}
        response = self.client.patch(self.lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Отредактировано модератором')


    # метод DELETE
    def test_owner_can_delete_lesson(self):
        """ Владелец может удалить свой урок """
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_other_user_cannot_delete_lesson(self):
        """ Другой пользователь не может удалить чужой урок """
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.lesson_delete_url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
        self.assertEqual(Lesson.objects.count(), 1)

    def test_moderator_cannot_delete_lesson(self):
        """ Модератор не может удалять уроки """
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)


class SubscriptionTests(BaseTestCase):
    """Тесты функционала подписки на курс"""
    def setUp(self):
        super().setUp()
        self.subscription_url = reverse('core:subscription', kwargs={'course_pk': self.course.pk})


    def test_subscribe_to_course(self):
        """ Пользователь может подписаться на курс """
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(self.subscription_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(response.data['is_active'])

    def test_unsubscribe_from_course(self):
        """ Пользователь может отписаться от курса """
        self.client.force_authenticate(user=self.other_user)
        self.client.post(self.subscription_url)
        response = self.client.post(self.subscription_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка отключена')
        self.assertFalse(response.data['is_active'])

    def test_resubscribe_to_course(self):
        """ Пользователь может возобновить подписку """
        self.client.force_authenticate(user=self.other_user)
        self.client.post(self.subscription_url)
        self.client.post(self.subscription_url)
        response = self.client.post(self.subscription_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка возобновлена')
        self.assertTrue(response.data['is_active'])

    def test_unauthenticated_cannot_subscribe(self):
        """ Неавторизованный не может подписаться """
        response = self.client.post(self.subscription_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
