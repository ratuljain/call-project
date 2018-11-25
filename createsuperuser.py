#!/usr/bin/python
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coopproject.settings")
django.setup()

from django.contrib.auth.models import User

admin_username = os.getenv('DJANGO_ADMIN_USERNAME', 'admin')
admin_pass = os.getenv('DJANGO_ADMIN_PASSWORD', 'fortheloveofgodpleaseuseagoodpassword')
admin_email = admin_username + '@example.com'

User.objects.filter(username=admin_username).delete()
User.objects.create_superuser(admin_username, admin_email, admin_pass)

print ('============ Created superuser with username - {} and password - {} ============').format(admin_username,
                                                                                                  admin_pass)
