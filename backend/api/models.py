from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class IssueWebhook(models.Model):
    received_at = models.DateTimeField(help_text="When we received the event.")
    payload = models.JSONField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["received_at"]),
        ]

    def __str__(self):
        model_name = self.__class__.__name__
        fields_str = ", ".join((f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields))
        return f"{model_name}({fields_str})"

class GithubUser(AbstractBaseUser):
    github_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=200, unique=True)

    USERNAME_FIELD = 'username'

class Label(models.Model):
    github_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)

    def __str__(self):
        model_name = self.__class__.__name__
        fields_str = ", ".join((f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields))
        return f"{model_name}({fields_str})"

class Issue(models.Model):
    class IssueState(models.TextChoices):
        OPEN = "open",
        CLOSED = "closed"
        ALL = "all"

    github_id = models.IntegerField(unique=True)
    url = models.URLField(unique=True)
    title = models.CharField(max_length=200)
    body = models.TextField(default="", blank=True)
    state = models.CharField(
        max_length=200,
        choices=IssueState.choices,
        default=IssueState.OPEN
    )
    opened_by = models.ForeignKey(GithubUser, on_delete=models.PROTECT, related_name="opened_issue")
    closed_by = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name="closed_issue", null=True, blank=True)
    last_updated_by = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name="updated_issue", null=True, blank=True)
    assignees = models.ManyToManyField(GithubUser, related_name="assigned_issues", blank=True)
    labels = models.ManyToManyField(Label, blank=True)

    def __str__(self):
        model_name = self.__class__.__name__
        fields_str = ", ".join((f"{field.name}={getattr(self, field.name)}" for field in self._meta.fields))
        return f"{model_name}({fields_str})"






