from django.db import migrations
from django.contrib.postgres.operations import BtreeGistExtension

class Migration(migrations.Migration):
    dependencies = [
        ('finanzas', '0001_initial'),  # depende de tu primera migración
    ]

    operations = [
        BtreeGistExtension(),
    ]
