from api.models import GithubUser, Issue, Label
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubUser
        fields="__all__"


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields="__all__"

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields="__all__"