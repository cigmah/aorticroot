from rest_framework import permissions


class IsContributorOrReadOnly(permissions.BasePermission):
    """ Custom permission to only allow creators of a question to edit it.
    """

    def has_object_permission(self, request, view, object):
        # Reading does not require authentication.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return object.contributor == request.user


class IsParentContributorOrReadOnly(permissions.BasePermission):
    """ Custom permission to only allow creators of a question choice's parent to edit it.
    """

    def has_object_permission(self, request, view, object):
        # Reading does not require authentication.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return object.question.contributor == request.user