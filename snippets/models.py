from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# get_all_styles : Return generator for all styles by name, both builtin and plugin.
# Reference: https://kite.com/python/docs/pygments.styles.get_all_styles

# Create your models here.
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICE = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICE = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    # linenos : line number
    linenos = models.BooleanField(default=False)
    # choices 옵션은 2중 튜플에서 앞의 값은 DB에 저장되도록 하며 뒤의 값은 admin 페이지나 폼에서 표시됨.
    language = models.CharField(choices=LANGUAGE_CHOICE, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICE, default='friendly', max_length=100)

    # Meta Class는 필드 선언 밑에 한 줄 띄고 위치함.
    # Meta Class : class container with some options(metadata) attached to the model
    class Meta:
        ordering = ['created']
