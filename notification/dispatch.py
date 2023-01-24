from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.utils import timezone

from .models import Notification

UserModel = get_user_model()


def notification(
    user,
    actor,
    verb,
    notification_type=Notification.notification_type.default,
    timestamp=timezone.now(),
    action_object=None,
    target=None,
    description=None,
):
    """
    Create notification for user or queryset of user or list of user.

    Notifications are actually actions events, which are categorized by four main components.

    Actor. The object that performed the activity.
    Verb. The verb phrase that identifies the action of the activity.
    Action Object. (Optional) The object linked to the action itself.
    Target. (Optional) The object to which the activity was performed.

    Actor, Action Object and Target are GenericForeignKeys to any arbitrary Django object.
    An action is a description of an action that was performed (Verb) at some instant in time by some Actor on some
    optional Target that results in an Action Object getting created/updated/deleted

    Use '{actor} {verb} {action_object(optional)} on {target(optional)}' as description if description is not provided

    This function is wrapper around UserModel.notify() function and can be used for calling single user or multiple
    users with help of queryset or list of users
    """
    if isinstance(user, (QuerySet, list)) and all(
        isinstance(u, UserModel) for u in user
    ):
        users = user
    elif isinstance(user, UserModel):
        users = [user]
    else:
        raise TypeError("Only UserModel or queryset or list of UserModel is supported")
    for user_obj in users:
        user_obj.notify(
            actor,
            verb,
            notification_type,
            timestamp,
            action_object,
            target,
            description,
        )
