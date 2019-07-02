from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    """
    This model contains notes - atomic pieces of information
    related to medicine, intended as contextual background on which
    questions and cases are based.
    """

    # This model contains a number of tags which are specified as
    # hard-coded enums. The expectation is that these tags are
    # stable so do not require an extra table.
    # The original version of this database had these in a separate
    # table, but the logic overhead for joining across tables and
    # supporting ad-hoc creation was deemed unnecessary.

    # Specialty constants. These specialties
    # are based on the groupings of our curriculum
    # guides for each year.
    # The boilerplate is high, but this should be a one-time
    # cost.
    #
    #
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

    # Specialty choices for the model. This list is easy to generate
    # with a good text editor from the above list.
    # An example command to do this with evil Emacs is, in a
    # scratch buffer, :%s/\([A-Z_]*\)\s+=\s+\d+/(\1, '\1'), on the above list.
    SPECIALTY_CHOICES = [
        (PRINCIPLES                          , 'PRINCIPLES'),
        (CARDIOVASCULAR                      , 'CARDIOVASCULAR'),
        (RESPIRATORY                         , 'RESPIRATORY'),
        (GASTROINTESTINAL                    , 'GASTROINTESTINAL'),
        (RENAL_AND_UROLOGICAL                , 'RENAL_AND_UROLOGICAL'),
        (MUSCULOSKELETAL_AND_RHEUMATOLOGICAL , 'MUSCULOSKELETAL_AND_RHEUMATOLOGICAL'),
        (NEUROLOGICAL                        , 'NEUROLOGICAL'),
        (HAEMATOLOGICAL                      , 'HAEMATOLOGICAL'),
        (ENDOCRINE                           , 'ENDOCRINE'),
        (MENTAL_AND_BEHAVIOURAL              , 'MENTAL_AND_BEHAVIOURAL'),
        (OBSTETRIC_AND_GYNAECOLOGICAL        , 'OBSTETRIC_AND_GYNAECOLOGICAL'),
        (OTOLARYNGOLOGICAL                   , 'OTOLARYNGOLOGICAL'),
        (OPHTHALMOLOGICAL                    , 'OPHTHALMOLOGICAL'),
        (DERMATOLOGICAL                      , 'DERMATOLOGICAL'),
    ]

    # Topic choices, as subtopics for each specialty.
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
    DISORDERS_SPECIFIC                = 14
    DISORDERS_PAEDIATRIC              = 15
    DISORDERS_PRIMARY_CARE_PREVENTION = 16
    DISORDERS_TRAUMA_EXTERNAL         = 17
    MISCELLANEOUS_TOPICS              = 18


    TOPIC_CHOICES = [
        (OVERVIEW                          , 'OVERVIEW'),
        (GLOBAL_ISSUES                     , 'GLOBAL_ISSUES'),
        (DEVELOPMENT                       , 'DEVELOPMENT'),
        (CELL_LEVEL_STRUCTURE              , 'CELL_LEVEL_STRUCTURE'),
        (ORGAN_LEVEL_STRUCTURE             , 'ORGAN_LEVEL_STRUCTURE'),
        (THEORY_OF_NORMAL_FUNCTION         , 'THEORY_OF_NORMAL_FUNCTION'),
        (THEORY_OF_ABNORMAL_FUNCTION       , 'THEORY_OF_ABNORMAL_FUNCTION'),
        (MEDICATIONS                       , 'MEDICATIONS'),
        (CLINICAL_HISTORY                  , 'CLINICAL_HISTORY'),
        (CLINICAL_EXAM                     , 'CLINICAL_EXAM'),
        (CLINICAL_INVESTIGTIONS            , 'CLINICAL_INVESTIGTIONS'),
        (CLINICAL_PROCEDURES               , 'CLINICAL_PROCEDURES'),
        (DISORDERS_INFECTIOUS              , 'DISORDERS_-_INFECTIOUS'),
        (DISORDERS_NEOPLASTIC              , 'DISORDERS_-_NEOPLASTIC'),
        (DISORDERS_SPECIFIC                , 'DISORDERS_-_SPECIFIC'),
        (DISORDERS_PAEDIATRIC              , 'DISORDERS_-_PAEDIATRIC'),
        (DISORDERS_PRIMARY_CARE_PREVENTION , 'DISORDERS_-_PRIMARY_CARE_&_PREVENTION'),
        (DISORDERS_TRAUMA_EXTERNAL         , 'DISORDERS_-_TRAUMA_EXTERNAL'),
        (MISCELLANEOUS_TOPICS              , 'MISCELLANEOUS_TOPICS'),
    ]


    contributor = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )

    specialty = models.IntegerField(
        choices=SPECIALTY_CHOICES,
        default=PRINCIPLES,
    )

    topic = models.IntegerField(
        choices=TOPIC_CHOICES,
        default=OVERVIEW,
    )

    title = models.CharField(
        max_length=60,
        unique=True
    )

    # The content is expected to be in markdown.
    content = models.TextField()

    class Meta:
        # Ensure there is only one note per specialty and topic combination.
        unique_together = ("specialty", "topic")

    def __str__(self):
        return self.title


class NoteComment(models.Model):
    """
    This model contains comments that users can add to notes.
    """

    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='note_comment',
    )

    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    content = models.TextField()

    def __str__(self):
        return self.content
