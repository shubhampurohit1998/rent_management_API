# from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from UserApp.models import *
from UserApp.serializers import *
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

User = get_user_model()

""" APIView based view """


# In APIView we have to override all builtin methods such as get, delete, put, patch, post etc....


class UserList(APIView):

    def get(self, request, format=None):  # Here format is to specify which format we are going to send/receive data
        # like json
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_obj = self.get_object(pk)
        user_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" APIView based view """

# class PropertyList(APIView):
#
#     def get(self, request):
#         property = Property.objects.all()
#         serializer = PropertySerializer(property, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = PropertySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PropertyDetail(APIView):
#
#     def get_object(self, pk):
#         try:
#             return Property.objects.get(pk=pk)
#         except Property.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         property_obj = self.get_object(pk)
#         serializer = PropertySerializer(property_obj)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         property_obj = self.get_object(pk)
#         # import pdb;pdb.set_trace()
#         serializer = PropertySerializer(property_obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         property_obj = self.get_object(pk)
#         property_obj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""mixin(generic views) These views provide builtin features with GenericAPIView"""


# Provide concise way to write code (Rest of things depends on circumstances of user need)
# Behind the scene GenericAPIView extends APIView

class PropertyList(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   generics.GenericAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    # Don't specify  serializer_class as
    # "serializer_class = UserSerializer(user)"  otherwise it gonna start problem

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PropertyDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserPropertyList(mixins.ListModelMixin,
                       generics.GenericAPIView):
    def get_queryset(self):
        queryset = Property.objects.filter(user_id=self.kwargs["pk"])
        return queryset

    serializer_class = PropertySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PropertyRentDetail(mixins.ListModelMixin,
                         generics.GenericAPIView):
    def get_queryset(self):
        queryset = Rent.objects.filter(property_id=self.kwargs["pk"])
        return queryset

    serializer_class = RentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


"""This is made by generic view """

# class RentList(generics.ListCreateAPIView):
#     queryset = Rent.objects.all()
#     serializer_class = RentSerializer
#
#
# class RentDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Rent.objects.all()
#     serializer_class = RentSerializer


"""This is made by Routing scheme using Viewset)"""


# class RentListViewSet(viewsets.ViewSet):
#
#     def list(self, request):
#         queryset = Rent.objects.all()
#         serializer = RentSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = RentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RentDetailViewSet(viewsets.ViewSet):
#     lookup_value_regex = '[0-9]{32}'
#
#     def get_object(self, pk):
#         try:
#             return Rent.objects.get(pk=pk)
#         except Rent.DoesNotExist:
#             raise Http404
#
#     # @action(detail=True, method=['GET'])
#     def retrieve(self, request, pk=None):
#         # import pdb;
#         # pdb.set_trace()
#         rent_obj = self.get_object(pk)
#         serializer = RentSerializer(rent_obj)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def destroy(self, request, pk=None):
#         rent_obj = self.get_object(pk)
#         # serializer = RentSerializer(data=request.data)
#         rent_obj.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def update(self, request, pk=None):
#         rent_obj = self.get_object(pk)
#         serializer = RentSerializer(rent_obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     def partial_update(self, request, pk=None):
#         # import pdb;
#         # pdb.set_trace()
#         rent_obj = self.get_object(pk)
#         serializer = RentSerializer(rent_obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     # @action(detail=True, methods=['GET'], name='Check yourself')
#     # def hello(self, request, pk=None):
#     #     rent_obj = self.get_object(pk)
#     #     serializer = RentSerializer(rent_obj)
#     #     return Response(serializer.data, status=status.HTTP_200_OK)


"""This is made by Routing scheme and GenricViewSet"""

# class RentListViewSet(mixins.ListModelMixin,
#                       mixins.CreateModelMixin,
#                       viewsets.GenericViewSet):
#     queryset = Rent.objects.all()
#     serializer_class = RentSerializer
#
#
# class RentDetailViewSet(mixins.RetrieveModelMixin,
#                         mixins.UpdateModelMixin,
#                         mixins.DestroyModelMixin,
#                         viewsets.GenericViewSet):
#     queryset = Rent.objects.all()
#     serializer_class = RentSerializer


"""This is made by Routing scheme using ModelViewSet"""


class RentListViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer


class RentDetailViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer

