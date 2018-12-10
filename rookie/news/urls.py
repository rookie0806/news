from django.urls import path
from . import views
from django.conf.urls import url
app_name = "users"

urlpatterns = [
    url(
        regex=r'^search/$',
        view=views.getData.as_view(),
        name='getData'
    ),
    url(
        regex=r'^pgword/$',
        view=views.getProgressWord.as_view(),
        name='getword1'
    ),
    url(
        regex=r'^npgword/$',
        view=views.getNotProgressWord.as_view(),
        name='getword2'
    )
]
