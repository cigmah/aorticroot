# Generated by Django 3.0.1 on 2020-01-26 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objectives', '0002_auto_20200102_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objective',
            name='topic',
            field=models.IntegerField(choices=[(0, 'OVERVIEW'), (1, 'GLOBAL_ISSUES'), (2, 'DEVELOPMENT'), (3, 'CELL_LEVEL_STRUCTURE'), (4, 'ORGAN_LEVEL_STRUCTURE'), (5, 'THEORY_OF_NORMAL_FUNCTION'), (6, 'THEORY_OF_ABNORMAL_FUNCTION'), (7, 'MEDICATIONS'), (8, 'CLINICAL_HISTORY'), (9, 'CLINICAL_EXAM'), (10, 'CLINICAL_INVESTIGTIONS'), (11, 'CLINICAL_PROCEDURES'), (12, 'DISORDERS_-_INFECTIOUS'), (13, 'DISORDERS_-_NEOPLASTIC'), (14, 'DISORDERS_-_EMERGENCY'), (15, 'DISORDERS_-_SPECIFIC'), (16, 'DISORDERS_-_PAEDIATRIC'), (17, 'DISORDERS_-_PRIMARY_CARE_&_PREVENTION'), (18, 'DISORDERS_-_GERIATRIC'), (19, 'DISORDERS_-_TRAUMA_EXTERNAL'), (20, 'MISCELLANEOUS_TOPICS')], help_text='The topic tag for this objective.'),
        ),
    ]