from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ActivitySerializer
from core.models import Activity, Ticket


# Create your views here.

class ActivityViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        queryset = super(ActivityViewSet, self).get_queryset()
        queryset = queryset.filter(date__gte=timezone.now())
        return queryset

    @action(
        methods=('get', 'post'),
        detail=True,
        url_path='purchase',
        url_name='purchase',
        permission_classes=[IsAuthenticated])
    def purchase(self, request, pk):
        activity = self.get_object()
        if activity.participants < activity.capacity and activity.date > timezone.now():
            ticket, created = Ticket.objects.get_or_create(
                activity=activity, user=request.user, status=False, canceled=False
            )
            if created:
                activity.participants += 1
                activity.save()
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
