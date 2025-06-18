from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0003_userhistory_tool_url'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserHistory',
        ),
    ] 