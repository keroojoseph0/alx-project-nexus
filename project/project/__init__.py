try:
    from .celery import app as celery_app
except ImportError:
    pass

__all__ = ('celery_app',)
