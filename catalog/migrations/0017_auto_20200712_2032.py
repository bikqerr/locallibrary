# Generated by Django 3.0.3 on 2020-07-12 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20200712_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(blank=True, null=True, related_name='author', to='catalog.Author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='translate',
            field=models.ManyToManyField(blank=True, null=True, related_name='translate', to='catalog.Author'),
        ),
    ]
