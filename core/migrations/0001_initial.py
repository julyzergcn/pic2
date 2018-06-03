# Generated by Django 2.0.6 on 2018-06-03 13:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('computer_name', models.CharField(max_length=100)),
                ('file_dir', models.TextField()),
                ('file_name', models.CharField(max_length=255)),
                ('file_exist', models.BooleanField(default=True)),
                ('file_size', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FileCopy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('copy_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('from_file', models.TextField()),
                ('to_file', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'File Copies',
            },
        ),
        migrations.CreateModel(
            name='FileExt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_ext', models.CharField(max_length=20)),
                ('file_type', models.CharField(choices=[('Image', 'Image'), ('Video', 'Video'), ('Audio', 'Audio')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='FileHash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_hash', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileScan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scan_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('file_exist', models.BooleanField()),
                ('file_size', models.PositiveIntegerField(default=0)),
                ('file_hash', models.CharField(blank=True, max_length=32)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scans', to='core.File')),
            ],
        ),
        migrations.AddField(
            model_name='filecopy',
            name='file_hash_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copies', to='core.FileHash'),
        ),
        migrations.AddField(
            model_name='file',
            name='file_hash_obj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='core.FileHash'),
        ),
    ]
