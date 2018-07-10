from django.urls import path
from rest_framework.routers import DefaultRouter


# from .models import Address, Teacher, Student, TeacherProfile
# from app.api.one import AddressApiView
from app.api.two import (
    TeacherViewSet,
    StudentViewSet,
    StudentModelViewSet,
    TeacherProfileModelViewSet,
    TeacherListMixinView,
    StudentOnlyModelViewSet)
from .one import AddressListApiView, AddressCreateApiView, AddressDeleteView, AddressUpdateView

app_name = 'app'

router = DefaultRouter()
router.register(r'students', StudentModelViewSet)
router.register(r'studentonly', StudentOnlyModelViewSet)
router.register(r'profiles', TeacherProfileModelViewSet)

# urlpatterns = router.urls

student_create = StudentViewSet.as_view({'post': 'create'})

user_list_create = TeacherViewSet.as_view({'get': 'list', 'post': 'create'})
user_detail_update = TeacherViewSet.as_view({'get': 'retrieve', 'put': 'update'})

urlpatterns = [
    path('address/', AddressListApiView.as_view(), name='address_list'),
    path('address/create/', AddressCreateApiView.as_view(), name='address_create'),
    path('address/<int:pk>/delete/', AddressDeleteView.as_view(), name='address_delete'),
    path('address/<int:pk>/update/', AddressUpdateView.as_view(), name='address_update'),

    path('teachers/', user_list_create, name='user_list_create'),
    path('teachers/<int:pk>/', user_detail_update, name='user_detail_update'),

    path('teacherlistmixin/', TeacherListMixinView.as_view(), name='teacher_list_mixin')


    # path('students/', student_create, name='create_student'),
]

urlpatterns += router.urls