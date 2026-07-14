"""
audit — tiny helper for writing AuditLog rows without duplicating
boilerplate (IP extraction, username snapshotting) at every call site.
"""
from .models import AuditLog


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def log_action(request, action, detail="", user=None):
    """Write one AuditLog row. `user` defaults to request.user if authenticated."""
    actor = user or (request.user if getattr(request, 'user', None) and request.user.is_authenticated else None)
    AuditLog.objects.create(
        user=actor,
        username_snapshot=actor.username if actor else "anonymous",
        action=action,
        detail=detail,
        ip_address=_client_ip(request),
    )
