""" Models for medical learning objectives. 
"""
from django.db import models
from django.contrib.auth.models import User

class Objective(models.Model):
    """
    This model contains learning objectives.

    Learning objectives are the top-level categorisation unit for questions 
    in the AORTA database. Each learning objective is tagged with a specialty,
    a topic and a "stage" in medical training, as well as notes for that objective. 

    All questions in AORTA are then categorised under a parent learning objective. 

    Note that the specialty, topic and stage of a learning objective are specified
    here as hard-coded enums. The expectation is that these tags are stable and so 
    do not require an extra table, which simplifies the backend and frontend logic.
    """

    # Specialty constants. 
    PRINCIPLES                          = 0
    CARDIOVASCULAR                      = 1
    RESPIRATORY                         = 2
    GASTROINTESTINAL                    = 3
    RENAL_AND_UROLOGICAL                = 4
    MUSCULOSKELETAL_AND_RHEUMATOLOGICAL = 5
    NEUROLOGICAL                        = 6
    HAEMATOLOGICAL                      = 7
    ENDOCRINE                           = 8
    MENTAL_AND_BEHAVIOURAL              = 9
    OBSTETRIC_AND_GYNAECOLOGICAL        = 10
    OTOLARYNGOLOGICAL                   = 11
    OPHTHALMOLOGICAL                    = 12
    DERMATOLOGICAL                      = 13

    # Specialty choices for the model.
    # To generate these from the above, you can use a scratch buffer and a regex replace.
    # :%s/\([A-Z_]*\)\s+=\s+\d+/(\1, "\1"), on the above list.
    SPECIALTY_CHOICES = [
        (PRINCIPLES                          , "PRINCIPLES"),
        (CARDIOVASCULAR                      , "CARDIOVASCULAR"),
        (RESPIRATORY                         , "RESPIRATORY"),
        (GASTROINTESTINAL                    , "GASTROINTESTINAL"),
        (RENAL_AND_UROLOGICAL                , "RENAL_AND_UROLOGICAL"),
        (MUSCULOSKELETAL_AND_RHEUMATOLOGICAL , "MUSCULOSKELETAL_AND_RHEUMATOLOGICAL"),
        (NEUROLOGICAL                        , "NEUROLOGICAL"),
        (HAEMATOLOGICAL                      , "HAEMATOLOGICAL"),
        (ENDOCRINE                           , "ENDOCRINE"),
        (MENTAL_AND_BEHAVIOURAL              , "MENTAL_AND_BEHAVIOURAL"),
        (OBSTETRIC_AND_GYNAECOLOGICAL        , "OBSTETRIC_AND_GYNAECOLOGICAL"),
        (OTOLARYNGOLOGICAL                   , "OTOLARYNGOLOGICAL"),
        (OPHTHALMOLOGICAL                    , "OPHTHALMOLOGICAL"),
        (DERMATOLOGICAL                      , "DERMATOLOGICAL"),
    ]

    # Topic constants.
    OVERVIEW                          = 0
    GLOBAL_ISSUES                     = 1
    DEVELOPMENT                       = 2
    CELL_LEVEL_STRUCTURE              = 3
    ORGAN_LEVEL_STRUCTURE             = 4
    THEORY_OF_NORMAL_FUNCTION         = 5
    THEORY_OF_ABNORMAL_FUNCTION       = 6
    MEDICATIONS                       = 7
    CLINICAL_HISTORY                  = 8
    CLINICAL_EXAM                     = 9
    CLINICAL_INVESTIGTIONS            = 10
    CLINICAL_PROCEDURES               = 11
    DISORDERS_INFECTIOUS              = 12
    DISORDERS_NEOPLASTIC              = 13
    DISORDERS_EMERGENCY               = 14
    DISORDERS_SPECIFIC                = 15
    DISORDERS_PAEDIATRIC              = 16
    DISORDERS_PRIMARY_CARE_PREVENTION = 17
    DISORDERS_GERIATRIC               = 18
    DISORDERS_TRAUMA_EXTERNAL         = 19
    MISCELLANEOUS_TOPICS              = 20

    # Topic choices.
    TOPIC_CHOICES = [
        (OVERVIEW                          , "OVERVIEW"),
        (GLOBAL_ISSUES                     , "GLOBAL_ISSUES"),
        (DEVELOPMENT                       , "DEVELOPMENT"),
        (CELL_LEVEL_STRUCTURE              , "CELL_LEVEL_STRUCTURE"),
        (ORGAN_LEVEL_STRUCTURE             , "ORGAN_LEVEL_STRUCTURE"),
        (THEORY_OF_NORMAL_FUNCTION         , "THEORY_OF_NORMAL_FUNCTION"),
        (THEORY_OF_ABNORMAL_FUNCTION       , "THEORY_OF_ABNORMAL_FUNCTION"),
        (MEDICATIONS                       , "MEDICATIONS"),
        (CLINICAL_HISTORY                  , "CLINICAL_HISTORY"),
        (CLINICAL_EXAM                     , "CLINICAL_EXAM"),
        (CLINICAL_INVESTIGTIONS            , "CLINICAL_INVESTIGTIONS"),
        (CLINICAL_PROCEDURES               , "CLINICAL_PROCEDURES"),
        (DISORDERS_INFECTIOUS              , "DISORDERS_-_INFECTIOUS"),
        (DISORDERS_NEOPLASTIC              , "DISORDERS_-_NEOPLASTIC"),
        (DISORDERS_EMERGENCY               , "DISORDERS_-_EMERGENCY"),
        (DISORDERS_SPECIFIC                , "DISORDERS_-_SPECIFIC"),
        (DISORDERS_PAEDIATRIC              , "DISORDERS_-_PAEDIATRIC"),
        (DISORDERS_PRIMARY_CARE_PREVENTION , "DISORDERS_-_PRIMARY_CARE_&_PREVENTION"),
        (DISORDERS_GERIATRIC               , "DISORDERS_-_GERIATRIC"),
        (DISORDERS_TRAUMA_EXTERNAL         , "DISORDERS_-_TRAUMA_EXTERNAL"),
        (MISCELLANEOUS_TOPICS              , "MISCELLANEOUS_TOPICS"),
    ]

    # Medical training stage constants.
    YEAR_1    = 0
    YEAR_2A   = 1
    YEAR_3B   = 2
    YEAR_4C   = 3
    YEAR_5D   = 4
    INTERN    = 5
    RESIDENT  = 6
    REGISTRAR = 7

    # Medial training stage choices.
    STAGE_CHOICES = [
        (YEAR_1     , "YEAR_1"),
        (YEAR_2A    , "YEAR_2A"),
        (YEAR_3B    , "YEAR_3B"),
        (YEAR_4C    , "YEAR_4C"),
        (YEAR_5D    , "YEAR_5D"),
        (INTERN     , "INTERN"),
        (RESIDENT   , "RESIDENT"),
        (REGISTRAR  , "REGISTRAR"),
    ]

    # The assigned contributor is important, as this will be the only user which 
    # is allowed to modify and delete an objective once it is created.
    contributor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        help_text="The user assigned to this objective for editing and deletion."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Time of creation."
    )

    modified_at = models.DateTimeField(
        auto_now=True,
        help_text="Time of modification."
    )

    specialty = models.IntegerField(
        choices=SPECIALTY_CHOICES,
        help_text="The specialty tag for this objective."
    )

    topic = models.IntegerField(
        choices=TOPIC_CHOICES,
        help_text="The topic tag for this objective."
    )

    stage = models.IntegerField(
        choices=STAGE_CHOICES,
        help_text="The medical training stage tag for this objective"
    )

    title = models.CharField(
        max_length=280,
        unique=True,
        help_text="A brief statement of the objective, no more than 280 characters."
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text="The notes for this objective in Markdown."
    )

    def __str__(self):
        return self.title
