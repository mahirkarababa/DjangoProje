# Generated by Django 3.0.4 on 2020-06-05 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_faq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=models.TextField(max_length=255),
        ),
    ]