# Generated by Django 2.1.4 on 2018-12-25 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20181225_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookid', models.CharField(max_length=100)),
                ('capterid', models.CharField(max_length=100)),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users')),
            ],
        ),
    ]
