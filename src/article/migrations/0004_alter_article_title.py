# Generated by Django 5.0.6 on 2024-06-10 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_average_points_article_count_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(default='Default Title', max_length=256, unique=True),
        ),
    ]
