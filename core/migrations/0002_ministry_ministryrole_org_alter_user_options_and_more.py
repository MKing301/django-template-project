# Generated by Django 4.1.5 on 2023-02-12 00:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ministry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Ministries',
            },
        ),
        migrations.CreateModel(
            name='MinistryRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('ministry_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ministry', verbose_name='Ministries')),
            ],
            options={
                'verbose_name_plural': 'MinistryRoles',
            },
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('org_city', models.CharField(max_length=100)),
                ('org_state', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Orgs',
            },
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': 'Users'},
        ),
        migrations.CreateModel(
            name='MinistryTeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ministry_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ministry', verbose_name='Ministries')),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Users')),
                ('team_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ministryrole', verbose_name='MinistryRoles')),
            ],
        ),
        migrations.AddField(
            model_name='ministry',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.org', verbose_name='Orgs'),
        ),
    ]