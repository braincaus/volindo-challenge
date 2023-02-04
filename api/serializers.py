from rest_framework import serializers

from core.models import Activity, Ticket


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.SlugRelatedField(slug_field='type', read_only=True)

    class Meta:
        model = Activity
        fields = (
            'id', 'url', 'activity', 'type', 'capacity', 'participants', 'price', 'date', 'key', 'accessibility',
        )


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)
    activity = ActivitySerializer()

    class Meta:
        model = Ticket
        fields = '__all__'
