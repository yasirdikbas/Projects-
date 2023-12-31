# Generated by Django 4.0.6 on 2022-07-26 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='known_error',
            name='Test_Case_ID',
        ),
        migrations.AddField(
            model_name='known_error',
            name='Order_Of_Test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Order_Of_Test_KE', to='tutorials.test_case', unique=True),
        ),
        migrations.AddField(
            model_name='known_error',
            name='Test_Case_Description',
            field=models.ForeignKey(default=None, max_length=1000, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='Test_Case_Description_KE', to='tutorials.test_case', unique=True),
        ),
        migrations.AddField(
            model_name='known_error',
            name='Test_Name',
            field=models.ForeignKey(blank=True, max_length=120, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Test_Name_KE', to='tutorials.test_list', unique=True),
        ),
        migrations.AlterField(
            model_name='test_case',
            name='Order_Of_Test',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='test_case',
            name='Test_Case_Description',
            field=models.CharField(default=None, max_length=1000),
        ),
        migrations.AlterField(
            model_name='test_case',
            name='Test_Case_ID',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='test_case',
            name='Test_ID',
            field=models.ForeignKey(blank=True, default=0, max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, to='tutorials.test_list', unique=True),
        ),
        migrations.AlterField(
            model_name='test_list',
            name='Test_ID',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
