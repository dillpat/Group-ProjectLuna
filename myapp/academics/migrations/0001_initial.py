# Generated by Django 3.1.7 on 2021-03-10 20:53

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=100000)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=100000)),
                ('goals', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=3)),
                ('planet_representation', models.CharField(default='../static/assets/planetE.svg', max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.course')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.staffprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StudentModuleEnrolment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolment_date', models.DateField()),
                ('enrolment_completion_date', models.DateField()),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.module')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ModulePosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.module')),
                ('report_users', models.ManyToManyField(related_name='module_post_report', to=settings.AUTH_USER_MODEL)),
                ('upvote_users', models.ManyToManyField(related_name='module_post_upvote', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='academics.moduleposts')),
                ('report_users', models.ManyToManyField(related_name='module_comment_report', to=settings.AUTH_USER_MODEL)),
                ('upvote_users', models.ManyToManyField(related_name='module_comment_upvote', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_posted'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.department'),
        ),
    ]