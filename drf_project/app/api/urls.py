from django.urls import path
from rest_framework.routers import DefaultRouter


# from .models import Address, Teacher, Student, TeacherProfile
# from app.api.one import AddressApiView
from app.api.two import (
    TeacherViewSet,
    StudentModelViewSet,
    TeacherProfileModelViewSet,
    TeacherListMixinView,
    AddressViewSet)
from .one import AddressListApiView, AddressCreateApiView, AddressDeleteView, AddressUpdateView

app_name = 'app'

router = DefaultRouter()
router.register(r'students', StudentModelViewSet)  # ViewSet responsible for crud on student table
router.register(r'profiles', TeacherProfileModelViewSet)  # ViewSet responsible for crud on teacher profile table
router.register(r'addressviewset', AddressViewSet) # ViewSet responsible for crud on address

# urlpatterns = router.urls

user_list_create = TeacherViewSet.as_view({'get': 'list', 'post': 'create'})
user_detail_update = TeacherViewSet.as_view({'get': 'retrieve', 'put': 'update'})

urlpatterns = [
    path('address/', AddressListApiView.as_view(),
         name='address_list'),  # list address
    path('address/create/', AddressCreateApiView.as_view(),
         name='address_create'),  # create address
    path('address/<int:pk>/delete/', AddressDeleteView.as_view(),
         name='address_delete'),  # delete address
    path('address/<int:pk>/update/', AddressUpdateView.as_view(),
         name='address_update'),  # update address

    path('teachers/', user_list_create,
         name='user_list_create'),  # list and create teachers
    path('teachers/<int:pk>/', user_detail_update,
         name='user_retrieve_update'),  # update and retrieve teachers

    # path('teacherlistmixin/', TeacherListMixinView.as_view(), name='teacher_list_mixin')


    # path('students/', student_create, name='create_student'),
]

urlpatterns += router.urls