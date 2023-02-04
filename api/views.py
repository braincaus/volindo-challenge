from django.utils import timezone
from rest_framework import viewsets, permissions, mixins, status, authentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ActivitySerializer, TicketSerializer
from core.models import Activity, Ticket


# Create your views here.

class ActivityViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = [
        authentication.BasicAuthentication, authentication.SessionAuthentication, authentication.TokenAuthentication
    ]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        queryset = super(ActivityViewSet, self).get_queryset()
        queryset = queryset.filter(date__gte=timezone.now())
        return queryset

    @action(
        methods=('get',), detail=False, url_path='my_activities', url_name='my_activities',
        permission_classes=[IsAuthenticated])
    def my_activities(self, request):
        activities = Activity.objects.filter(ticket__user=request.user, ticket__status=False, ticket__canceled=False)
        activities = ActivitySerializer(instance=activities, many=True, context={'request': request})
        return Response(data=activities.data, status=status.HTTP_200_OK)

    @action(
        methods=('get', 'post'), detail=True, url_path='purchase', url_name='purchase',
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
                ticket = TicketSerializer(instance=ticket, context={'request': request})
                return Response(data=ticket.data, status=status.HTTP_201_CREATED)

            ticket = TicketSerializer(instance=ticket, context={'request': request})
            return Response(data=ticket.data, status=status.HTTP_200_OK)

        return Response(
            data={'error': "Activity has more places available or it's not able to reserve."},
            status=status.HTTP_204_NO_CONTENT
        )


class TicketViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [
        authentication.BasicAuthentication, authentication.SessionAuthentication, authentication.TokenAuthentication
    ]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = super(TicketViewSet, self).get_queryset()
        queryset = queryset.filter(user=self.request.user).filter(status=False, canceled=False)
        return queryset

    @action(
        methods=('get', 'post'),
        detail=True,
        url_path='done',
        url_name='done'
    )
    def done(self, request, pk):
        ticket = self.get_object()
        if ticket.activity.date < timezone.now():
            if not ticket.status and not ticket.canceled:
                ticket.status = True
                ticket.save()
                return Response(data=None, status=status.HTTP_204_NO_CONTENT)
            elif ticket.status:
                return Response(data={"error": "It is already marked done."}, status=status.HTTP_400_BAD_REQUEST)
            elif ticket.canceled:
                return Response(data={"error": "It was cancelled before."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"error": "It is no possible to mark done yet"}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=('get', 'post'),
        detail=True,
        url_path='cancel',
        url_name='cancel'
    )
    def cancel(self, request, pk):
        ticket = self.get_object()
        if not ticket.status and not ticket.canceled:
            ticket.canceled = True
            ticket.activity.participants -= 1
            ticket.activity.save()
            ticket.save()
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)

        elif ticket.status:
            return Response(data={"error": "It is already marked done."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"error": "It was cancelled before."}, status=status.HTTP_400_BAD_REQUEST)
