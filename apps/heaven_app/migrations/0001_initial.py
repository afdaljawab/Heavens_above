# Generated by Django 2.2.4 on 2020-12-24 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=45)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('price', models.FloatField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isAdmin', models.BooleanField()),
                ('isUser', models.BooleanField(null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=45)),
                ('address', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=45)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role', to='heaven_app.Role')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heaven_app.Product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heaven_app.User')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='like',
            field=models.ManyToManyField(related_name='liked_products', to='heaven_app.User'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('date_of_birth', models.DateField()),
                ('place_of_birth', models.CharField(max_length=60)),
                ('phone', models.CharField(max_length=10)),
                ('total_price', models.FloatField(default=0.0)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heaven_app.Product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heaven_app.User')),
            ],
        ),
    ]
