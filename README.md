# django_rest_tutorial# Django REST Framework (Serialization)

[Django REST Framework -Serializers](https://dean-kim.github.io/rest_framework/2017/05/08/Django-REST-Framework-Serializers.html)

## Tutorial 1: Serialization

### Setting Environment & Getting Started















- PyCharm에서 "New Project" 생성한 뒤 가상환경 세팅

        $ pip install django
        $ pip install djangorestframework
        $ pip install pygments

- 프로젝트 및 앱 생성

        $ django-admin startproject tutorial
        $ cd tutorial
        $ python manage.py startapp snippets

    ![Django%20REST%20Framework%20Serialization/Untitled.png](Django%20REST%20Framework%20Serialization/Untitled.png)

- INSTALLED_APPS에 'rest_framework', 'snippets.apps.SnippetsConfig' 추가

### Creating a model to work with

- "rest_tutorial/snippets/models.py"

    ![Django%20REST%20Framework%20Serialization/Untitled%201.png](Django%20REST%20Framework%20Serialization/Untitled%201.png)

    - Meta Class
        - 모델의 옵션을 담고 있는 클래스

    [How does Django's Meta class work?](https://stackoverflow.com/questions/10344197/how-does-djangos-meta-class-work)

- migration

        $ python manage.py makemigrations snippets
        $ python manage.py migrate

### Creating a Serializer Class

- "rest_tutorial/snippets/serializers.py"

![Django%20REST%20Framework%20Serialization/Untitled%202.png](Django%20REST%20Framework%20Serialization/Untitled%202.png)

![Django%20REST%20Framework%20Serialization/Untitled%203.png](Django%20REST%20Framework%20Serialization/Untitled%203.png)

    >>> serializer = SnippetSerializer(snippet)
    >>> seriaizer.data
    # {'id' : 2, 'title': '', 'code': 'print("hello, world")\n', ...}
    
    >>> serializer = SnippetSerializer(data=data)
    >>> serializer.is_valid()
    >>> serializer.validated_data

- data: is_valid() 후에 볼 수 있는 dict
- validated_data: is_valid() && is_valid()==True 후에 볼 수 있는 Ordered Dict

- 예시
    - "views.py"

    ![Django%20REST%20Framework%20Serialization/Untitled%204.png](Django%20REST%20Framework%20Serialization/Untitled%204.png)

    - "serializers.py"

    ![Django%20REST%20Framework%20Serialization/Untitled%205.png](Django%20REST%20Framework%20Serialization/Untitled%205.png)

### Difference between Serializer and ModelSerializer

- ModelSerializer 클래스는 Model fields에 해당하는 field가 있는 Serializer 클래스를 자동으로 만들어줌. → Django model definitions와 밀접하게 매핑되는 serializer가 필요한 경우
- ModelSerializer는 아래 사항들을 제외하고는 일반 Serializer 클래스와 동일
    - 모델을 기반으로 set of fields가 자동으로 생성됨.
    - unique_together validator와 같은 serializer에 대한 validator를 자동으로 생성함.
    - .create() 및 .update()의 간단한 default implementations를 포함함.

[Django REST Framework -Serializers](https://dean-kim.github.io/rest_framework/2017/05/08/Django-REST-Framework-Serializers.html)

### Using ModelSerializers

- 기존의 코드

![Django%20REST%20Framework%20Serialization/Untitled%206.png](Django%20REST%20Framework%20Serialization/Untitled%206.png)

- 변경 후

![Django%20REST%20Framework%20Serialization/Untitled%207.png](Django%20REST%20Framework%20Serialization/Untitled%207.png)

- ModelSerializer 클래스를 사용하게 되면 serializer 필드와 관계(relationship)은 자동으로 생성됨. 자동으로 생성된 필드들을 확인하는 방법

        >>> from snippets.serailizers import SnippetSerializer
        >>> serializer = SnippetSerializer()
        >>> print(repr(serializer))

    ![Django%20REST%20Framework%20Serialization/Untitled%208.png](Django%20REST%20Framework%20Serialization/Untitled%208.png)

### JsonResponse

- HttpResponse의 subclass로, JSON-encoded response를 생성할 수 있게 해줌.
- 대부분의 기능은 superclass에서 상속받음.
- default Content-Type header = application/json

    >>> from django.http import JsonResponse
    >>> response = JsonResponse({'foo': 'bar'})
    # 첫 번째 argument는 dict여야 함.
    # dict가 아닌 경우 두 번째 argument로 safe=False를 설정해야 함.
    >>> response.content
    # result : {"foo": "bar"}

- JsonResponse 사용 목적
    - http status code에 더하여 메시지를 커스터마이징 하여 전달하고 싶을 때 사용함.

### Writing regular Django views using our Serializer

- **#1 "rest_tutorial/snippets/views.py"**

    ![Django%20REST%20Framework%20Serialization/Untitled%209.png](Django%20REST%20Framework%20Serialization/Untitled%209.png)

    - many = True 세팅 이유
        - Telling drf that queryset contains multiple items (a list of items)

    [What does 'many = True' do in Django Rest FrameWork?](https://stackoverflow.com/questions/51223456/what-does-many-true-do-in-django-rest-framework/51229456)

    >>> snippets = Snippet.objects.all()
    # <QuerySet [<Snippet: Snippet object(1)>, <Snippet: Snippet object(2)>, <Snippet: Snippet object (3)>]>
    
    >>> serializer = SnippetSerializer(snippets, many=True)
    >>> serializer.data
    # [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly'
    )]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('styl
    e', 'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'pyth
    on'), ('style', 'friendly')])]
    
    >>> from django.http import JsonResponse
    >>> JsonResponse(serializer.data, safe=False)
    # <JsonResponse status_code=200, "application/json">

- **#2 "rest_tutorial/snippets/views.py"**

    ![Django%20REST%20Framework%20Serialization/Untitled%2010.png](Django%20REST%20Framework%20Serialization/Untitled%2010.png)

    >>> snippet = Snippet.objects.get(pk=1)
    >>> serializer = SnippetSerializer(snippet)
    >>> serializer.data
    # {'id': 1, 'title': '', 'code': 'foo = "bar"\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
    >>> JsonResponse(serializer.data)
    # <JsonResponse status_code=200, "application/json">

- get()과 filter()의 차이

        >>> Snippet.objects.all()
        # <QuerySet [<Snippet: Snippet object (1)>, <Snippet: Snippet object (2), <Snippet: Snippet object (3)>]>
        
        >>> Snippet.objects.filter(pk=1)
        # <QuerySet [<Snippet: Snippet object (1)>]>
        
        >>> Snippets.objects.get(pk=1)
        # <Snippet: Snippet object(1)>

- **"rest_tutorial/snippets/urls.py"**

    ![Django%20REST%20Framework%20Serialization/Untitled%2011.png](Django%20REST%20Framework%20Serialization/Untitled%2011.png)

- **"rest_tutorial/rest_tutorial/urls.py"**

    ![Django%20REST%20Framework%20Serialization/Untitled%2012.png](Django%20REST%20Framework%20Serialization/Untitled%2012.png)

### Testing our first attempt at a WebAPI

![Django%20REST%20Framework%20Serialization/Untitled%2013.png](Django%20REST%20Framework%20Serialization/Untitled%2013.png)

![Django%20REST%20Framework%20Serialization/Untitled%2014.png](Django%20REST%20Framework%20Serialization/Untitled%2014.png)

## Tutorial 2: Request and Responses
