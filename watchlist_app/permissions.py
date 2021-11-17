from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # admin_permission=bool(request.user and request.user.is_staff) # same means of both lines
        # admin_permission=super().has_permission(request,view)
        # return request.method == 'GET' or admin_permission
        if request.method in permissions.SAFE_METHODS:
            return True
        else :
            return bool(request.user and request.user.is_staff)

class IsReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else :
            return request.user == obj.review_user or request.user.is_staff # as obj is obj which is getting or admin can also edit the review it may be inactive anyone's review