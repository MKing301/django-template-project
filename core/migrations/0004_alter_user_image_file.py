# Generated by Django 4.1.5 on 2023-02-12 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_board_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image_file',
            field=models.ImageField(default='images/default.jpg', max_length=125, upload_to='images/'),
        ),
    ]