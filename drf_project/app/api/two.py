from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
# from .models import Address, Teacher, Student, TeacherProfile
from .serializers import AddressSerializer, TeacherSerializer, StudentSerializer, TeacherProfileSerializer, \
    StudentOnlySerializer
from ..models import Address, Teacher, TeacherProfile, Student
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView


class TeacherViewSet(ViewSet):

    """
    A simple ViewSet for listing or retrieving Teachers.
    """

    def list(self, request):
        queryset = Teacher.objects.all()
        serializer = TeacherSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Teacher.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = TeacherSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        ser = TeacherSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status.HTTP_201_CREATED)

    # def update(self, request, pk=None):
    #     import ipdb; ipdb.set_trace()


class StudentViewSet(ViewSet):

    def create(self, request, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        ser = StudentSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()


class StudentModelViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherProfileModelViewSet(ModelViewSet):

    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer


class TeacherListMixinView(mixins.ListModelMixin, GenericAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TeacherListMixinView(mixins.UpdateModelMixin, GenericAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class StudentOnlyModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer



