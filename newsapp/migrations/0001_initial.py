# Generated by Django 3.2.4 on 2021-08-23 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('token', models.TextField(null=True)),
                ('expire_token', models.CharField(max_length=55, null=True)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]
