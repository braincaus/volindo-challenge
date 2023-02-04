from rest_framework import serializers

from core.models import Activity


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.SlugRelatedField(slug_field='type', read_only=True)

    class Meta:
        model = Activity
        fields = (
            'id', 'url', 'activity', 'type', 'capacity', 'participants', 'price', 'date', 'key', 'accessibility',
        )
