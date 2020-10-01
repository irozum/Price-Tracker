# Generated by Django 3.1.1 on 2020-10-01 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0007_auto_20201001_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('domain', models.CharField(max_length=60)),
            ],
        ),
        migrations.RemoveField(
            model_name='link',
            name='website_name',
        ),
        migrations.AddField(
            model_name='link',
            name='website',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='scraper.website'),
        ),
    ]
