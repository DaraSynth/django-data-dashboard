from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    اجازهٔ ویرایش/حذف فقط به صاحب (owner) آبجکت داده می‌شود.
    بقیه فقط می‌توانند بخوانند (SAFE_METHODS).
    """
    def has_object_permission(self, request, view, obj):
        # متدهای امن (GET, HEAD, OPTIONS) همیشه مجازند
        if request.method in permissions.SAFE_METHODS:
            return True
        # برای متدهای تغییر دهنده فقط اگر کاربر صاحب باشد اجازه بده
        return getattr(obj, "owner", None) == request.user