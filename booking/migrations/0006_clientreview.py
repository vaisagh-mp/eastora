# Generated by Django 5.2 on 2025-07-17 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_enquiry_related_package'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Client Review',
                'verbose_name_plural': 'Client Reviews',
                'ordering': ['-created_at'],
            },
        ),
    ]
