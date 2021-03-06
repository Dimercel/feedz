# Generated by Django 2.2 on 2020-12-04 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aggregator', '0004_Add_user_field_in_Category_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='channel',
            options={'verbose_name': 'rss-канал', 'verbose_name_plural': 'rss-каналы'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='aggregator.Category', verbose_name='категория'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='создан'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='last_seen',
            field=models.DateTimeField(verbose_name='последний просмотр'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='last_sync',
            field=models.DateTimeField(verbose_name='синхронизация'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(max_length=50, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='post_limit',
            field=models.PositiveSmallIntegerField(default=100, verbose_name='максимум постов'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='url',
            field=models.URLField(max_length=500, unique=True, verbose_name='урл'),
        ),
    ]
