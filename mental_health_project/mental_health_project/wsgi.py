"""
WSGI config for mental_health_project project.
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mental_health_project.settings')


def _bootstrap_vercel_sqlite():
	"""Initialize ephemeral /tmp SQLite database on Vercel cold starts."""
	if os.getenv('VERCEL') != '1' or os.getenv('DATABASE_URL'):
		return

	db_path = Path('/tmp/db.sqlite3')
	if db_path.exists():
		return

	import django
	from django.core.management import call_command

	django.setup()
	call_command('migrate', interactive=False, run_syncdb=True, verbosity=0)

	# allauth provider URLs query django.contrib.sites; ensure default site exists.
	from django.contrib.sites.models import Site

	vercel_url = os.getenv('VERCEL_URL', 'localhost')
	domain = vercel_url.replace('https://', '').replace('http://', '')
	Site.objects.update_or_create(
		id=1,
		defaults={'domain': domain, 'name': 'Mental Health Triage'}
	)


_bootstrap_vercel_sqlite()

application = get_wsgi_application()
