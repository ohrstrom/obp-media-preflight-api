# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

from .serializers import CheckSerializer
from ..models import Check


class CheckViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    queryset = Check.objects.all().order_by('-created')
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = CheckSerializer
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):

        queryset = Check.objects.filter().order_by('-created')

        serializer = CheckSerializer(
            queryset,
            many=True,
            context={'request': request}
        )

        return Response({
            'num_processing': queryset.filter(status=Check.STATUS_PROCESSING).count(),
            'results': serializer.data
        })

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        media_file_obj = self.request.data['media_file']
        serializer.save(media_file=media_file_obj)
        media_file_obj.close()

    def perform_update(self, serializer):

        media_file_obj = self.request.data['media_file']
        serializer.save(media_file=media_file_obj, status=Check.STATUS_INIT)
        media_file_obj.close()


    def get_or_create_detail(self, request, *args, **kwargs):

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        except Exception as e:
            pass
            #print(e)

        # data = request.data
        # data.update({
        #     'uuid': kwargs.get('uuid')
        # })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)


        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     instance.status = Check.STATUS_PENDING
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     return Response(serializer.data)



check_list = CheckViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
check_detail = CheckViewSet.as_view({
    'get': 'retrieve',
    'put': 'get_or_create_detail',
    'patch': 'update',
    'delete': 'destroy',
})
