# Generated by Django 3.2.19 on 2024-01-10 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chargingstations', '0002_auto_20240110_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chgerId', models.CharField(max_length=50)),
                ('chgerType', models.CharField(max_length=50)),
                ('stat', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Charger',
            },
        ),
        migrations.RemoveField(
            model_name='chargingstation',
            name='chgerId',
        ),
        migrations.RemoveField(
            model_name='chargingstation',
            name='chgerType',
        ),
        migrations.RemoveField(
            model_name='chargingstation',
            name='stat',
        ),
        migrations.AddField(
            model_name='chargingstation',
            name='charger',
            field=models.ManyToManyField(to='chargingstations.Charger'),
        ),
    ]
