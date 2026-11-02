
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donorprofile',
            old_name='phone',
            new_name='contact_number',
        ),

        migrations.AlterField(
            model_name='donorprofile',
            name='contact_number',
            field=models.CharField(
                max_length=20,
                null=True,
                help_text='Private: not displayed in search results'
            ),
        ),

        migrations.AddField(
            model_name='donorprofile',
            name='full_name',
            field=models.CharField(max_length=100, null=True),
        ),

        migrations.AddField(
            model_name='donorprofile',
            name='age',
            field=models.PositiveIntegerField(null=True),
        ),

        migrations.AddField(
            model_name='donorprofile',
            name='gender',
            field=models.CharField(max_length=20, null=True),
        ),

        migrations.AddField(
            model_name='donorprofile',
            name='address',
            field=models.TextField(null=True),
        ),

        migrations.CreateModel(
            name='PatientBloodRequest',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('patient_name', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('contact_number', models.CharField(max_length=15)),
                ('blood_group', models.CharField(
                    choices=[
                        ('A+', 'A+'), ('A-', 'A-'),
                        ('B+', 'B+'), ('B-', 'B-'),
                        ('AB+', 'AB+'), ('AB-', 'AB-'),
                        ('O+', 'O+'), ('O-', 'O-'),
                    ],
                    max_length=3
                )),
                ('units_required', models.PositiveIntegerField()),
                ('hospital_name', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=100)),
                ('urgency', models.CharField(
                    choices=[
                        ('Normal', 'Normal'),
                        ('Urgent', 'Urgent'),
                        ('Emergency', 'Emergency'),
                    ],
                    default='Normal',
                    max_length=20
                )),
                ('required_date', models.DateField()),
                ('status', models.CharField(
                    choices=[
                        ('Pending', 'Pending'),
                        ('Accepted', 'Accepted'),
                        ('Completed', 'Completed'),
                        ('Cancelled', 'Cancelled'),
                    ],
                    default='Pending',
                    max_length=20
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('requested_by', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=models.SET_NULL,
                    to='auth.user'
                )),
            ],
        ),
    ]
