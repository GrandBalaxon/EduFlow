import re
from rest_framework.serializers import ValidationError


class YouTubeLinkValidator:
    """ Проверяет отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com """

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if value:
            youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
            if not re.match(youtube_regex, value):
                raise ValidationError(f'{self.field} должен содержать ссылку только на youtube.com')
