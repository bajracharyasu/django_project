from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "MindsetApp"

urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("signup",views.register,name="register"),
    path("login",views.login_request,name="login"),
    path("logout",views.logout_request,name="logout"),
    path("question",views.question,name="question"),
    path("quiz/<int:disease_id>",views.quiz,name="quiz"),
    path("patient_register",views.patient_register,name="patient_register"),
    path("output",views.output,name="output"),
    path("about",views.about,name="about"),
    path("hospital",views.hospital,name="hospital"),
    path('recommendation/',views.recommendation,name="recommendation"),
    path('contact',views.contact,name="contact"),
    path('disease_detail/<int:disease_id>',views.disease_detail,name="disease_detail"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)