try:
    from django.test.runner import DiscoverRunner
except ImportError:
    # Django < 1.6
    from discover_runner import DiscoverRunner


class TestRunner(DiscoverRunner):
    pass
