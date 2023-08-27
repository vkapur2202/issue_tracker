import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import viewsets
from api.serializers import IssueSerializer, UserSerializer, LabelSerializer
from api.models import IssueWebhook, Issue, GithubUser, Label

@csrf_exempt
@require_POST
def issue_webhook(request):
    payload = json.loads(request.body)
    IssueWebhook.objects.create(
        received_at=timezone.now(),
        payload=payload,
    )
    process_webhook_payload(payload)
    
def process_webhook_payload(payload):
    action = payload["action"]
    issue_obj = payload["issue"]
    user_obj = issue_obj["user"]
    user = GithubUser.objects.get_or_create(
        github_id=user_obj["id"],
        username=user_obj["login"]
    )

    try: 
        if action == "opened":
            handle_opened_issue(issue_obj, user.id)
        elif action == "closed":
            handle_closed_issue(issue_obj["id"], user.id)
        elif action == "reopened":
            handle_reopened_issue(issue_obj["id"], user.id)
        elif action == "edited":
            handle_changed_issue(issue_obj["id"], user.id, payload["changes"])
        elif action == "assigned" or action == "unassigned":
            handle_assignee_change(issue_obj["id"], issue_obj["assignees"])
        elif action == "labeled" or action == "unlabeled":
            handle_label_change(issue_obj["id"], issue_obj["labels"])
            
    except Exception as e: 
        if type(e) == ObjectDoesNotExist:
            return HttpResponse(str(e), status=404)
        else:
            return HttpResponse(str(e), status=400)
    else:
        return HttpResponse("Webhook ingested Successfully", status=200)

def set_issue_assignees(issue, assignees):
    users_to_assign = []
    for assignee in assignees:
        user_to_assign = GithubUser.objects.get_or_create(
            github_id=assignee["id"],
            username=assignee["login"],
        )
        users_to_assign.append(user_to_assign)

    issue.assignees.set(users_to_assign)

def handle_assignee_change(issue_id, assignees):
    issue_to_update = Issue.objects.get(github_id=issue_id)
    set_issue_assignees(assignees, issue_to_update)
    issue_to_update.save()

def handle_opened_issue(issue_obj, user_id):
    created_issue = Issue.objects.create(
        github_id = issue_obj["id"],
        url = issue_obj["url"],
        title = issue_obj["title"],
        body = issue_obj["body"],
        opened_by = user_id,
        last_updated_by = user_id,
    )
    set_issue_assignees(created_issue, issue_obj["assignees"])

def handle_closed_issue(issue_id, user_id):
    issue_to_update = Issue.objects.get(github_id=issue_id)
    issue_to_update.state = Issue.IssueState.CLOSED
    issue_to_update.closed_by = user_id
    issue_to_update.last_updated_by = user_id
    issue_to_update.save()
    issue_to_update.opened_by.send_mail()

def handle_reopened_issue(issue_id, user_id):
    issue_to_update = Issue.objects.get(github_id=issue_id)
    issue_to_update.state = Issue.IssueState.OPEN
    issue_to_update.opened_by = user_id
    issue_to_update.last_updated_by = user_id
    issue_to_update.save()

def handle_changed_issue(issue_id, user_id, changes):
    issue_to_update = Issue.objects.get(github_id=issue_id)
    if "body" in changes:
        issue_to_update.body = changes["body"]
    if "title" in changes:
        issue_to_update.title = changes["title"]
    issue_to_update.last_updated_by = user_id
    issue_to_update.save()

def set_issue_labels(issue, labels):
    issue_labels = []
    for label in labels:
        label_to_add = Label.objects.get_or_create(
            github_id=label["id"],
            color=label["color"],
            name=label["name"],
            description=label["description"],
            url=label["url"],
        )
        issue_labels.append(label_to_add)
    issue.labels.set(issue_labels)

def handle_label_change(issue_id, labels):
    issue_to_update = Issue.objects.get(github_id=issue_id)
    set_issue_labels(issue_to_update, labels)
    issue_to_update.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = GithubUser.objects.all()
    serializer_class = UserSerializer

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer