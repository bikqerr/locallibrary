# Generated by Django 3.0.3 on 2020-07-12 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20200712_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, help_text='Select a genre for this book.', to='catalog.Genre'),
        ),
    ]
