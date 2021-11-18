# Generated by Django 3.2.5 on 2021-11-17 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patching', '0003_auto_20211114_0659'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualMachineInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vm_username', models.CharField(max_length=100)),
                ('vm_password', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='hypervisorinfo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
