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

    # Year level constants are specified here for reuse
    # when this module is imported. It's verbose, but keeps the
    # hardcoding within this module only.
    GENERAL_YEAR_LEVEL = 0
    YEAR_1 = 1
    YEAR_2A = 2
    YEAR_3B = 3
    YEAR_4C = 4
    YEAR_5D = 5

    # Year level choices
    YEAR_LEVEL_CHOICES = [
        (GENERAL_YEAR_LEVEL, "GENERAL_YEAR_LEVEL"),
        (YEAR_1, "YEAR_1"),
        (YEAR_2A, "YEAR_2A"),
        (YEAR_3B, "YEAR_3B"),
        (YEAR_4C, "YEAR_4C"),
        (YEAR_5D, "YEAR_5D"),
    ]

    # Specialty constants. These specialties
    # are based on the groupings of our curriculum
    # guides for each year.
    # The boilerplate is high, but this should be a one-time
    # cost.
    GENERAL_SPECIALTY = 0
    ANATOMY = 1
    PHYSIOLOGY = 2
    BIOCHEMISTRY = 3
    GENETICS = 4
    PHARMACOLOGY = 5
    PSYCHOLOGY = 6
    MICROBIOLOGY = 7
    SOCIAL_ISSUES = 8
    POPULATION_HEALTH = 9
    CLINICAL_SKILLS = 10
    CARDIOVASCULAR = 11
    RESPIRATORY = 12
    GASTROINTESTINAL = 13
    HEPATOBILIARY = 14
    GENITOURINARY = 15
    ENDOCRINE = 16
    NEUROLOGICAL = 17
    MUSCULOSKELETAL = 18
    HAEMATOLOGICAL = 19
    INFECTIOUS_DISEASE = 20
    DERMATOLOGICAL = 21
    PATHOLOGY = 22
    GENERAL_PRACTICE = 23
    PSYCHIATRY = 24
    OBGYN = 25
    PAEDIATRICS = 26
    LAW = 27
    ETHICS = 28

    # Specialty choices for the model. This list is easy to generate
    # with a good text editor from the above list.
    # An example command to do this with evil Emacs is, in a
    # scratch buffer, :%s/\([A-Z_]*\)\s+=\s+\d+/(\1, '\1'), on the above list.
    SPECIALTY_CHOICES = [
        (GENERAL_SPECIALTY, "GENERAL_SPECIALTY"),
        (ANATOMY, "ANATOMY"),
        (PHYSIOLOGY, "PHYSIOLOGY"),
        (BIOCHEMISTRY, "BIOCHEMISTRY"),
        (GENETICS, "GENETICS"),
        (PHARMACOLOGY, "PHARMACOLOGY"),
        (PSYCHOLOGY, "PSYCHOLOGY"),
        (MICROBIOLOGY, "MICROBIOLOGY"),
        (SOCIAL_ISSUES, "SOCIAL_ISSUES"),
        (POPULATION_HEALTH, "POPULATION_HEALTH"),
        (CLINICAL_SKILLS, "CLINICAL_SKILLS"),
        (CARDIOVASCULAR, "CARDIOVASCULAR"),
        (RESPIRATORY, "RESPIRATORY"),
        (GASTROINTESTINAL, "GASTROINTESTINAL"),
        (HEPATOBILIARY, "HEPATOBILIARY"),
        (GENITOURINARY, "GENITOURINARY"),
        (ENDOCRINE, "ENDOCRINE"),
        (NEUROLOGICAL, "NEUROLOGICAL"),
        (MUSCULOSKELETAL, "MUSCULOSKELETAL"),
        (HAEMATOLOGICAL, "HAEMATOLOGICAL"),
        (INFECTIOUS_DISEASE, "INFECTIOUS_DISEASE"),
        (DERMATOLOGICAL, "DERMATOLOGICAL"),
        (PATHOLOGY, "PATHOLOGY"),
        (GENERAL_PRACTICE, "GENERAL_PRACTICE"),
        (PSYCHIATRY, "PSYCHIATRY"),
        (OBGYN, "OBGYN"),
        (PAEDIATRICS, "PAEDIATRICS"),
        (LAW, "LAW"),
        (ETHICS, "ETHICS"),
    ]

    # Domain constants relating to specific subclassification
    # of notes - either foundation knowledge for practice, or
    # relating to specific tasks of clinical practice.
    GENERAL_DOMAIN = 0
    FOUNDATION = 1
    ASSESSMENT = 2
    INVESTIGATION = 3
    DIAGNOSIS = 4
    MANAGEMENT = 5

    # Domain choices.
    DOMAIN_CHOICES = [
        (GENERAL_DOMAIN, "GENERAL_DOMAIN"),
        (FOUNDATION, "FOUNDATION"),
        (ASSESSMENT, "ASSESSMENT"),
        (INVESTIGATION, "INVESTIGATION"),
        (DIAGNOSIS, "DIAGNOSIS"),
        (MANAGEMENT, "MANAGEMENT"),
    ]

    contributor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)

    modified_at = models.DateTimeField(auto_now=True)

    year_level = models.IntegerField(
        choices=YEAR_LEVEL_CHOICES, default=GENERAL_YEAR_LEVEL
    )

    specialty = models.IntegerField(
        choices=SPECIALTY_CHOICES, default=GENERAL_SPECIALTY
    )

    domain = models.IntegerField(choices=DOMAIN_CHOICES, default=GENERAL_DOMAIN)

    title = models.CharField(max_length=60, unique=True)

    # The content is expected to be in markdown.
    content = models.TextField()

    def __str__(self):
        return self.title


class NoteComment(models.Model):
    """
    This model contains comments that users can add to notes.
    """

    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)

    content = models.TextField()

    def __str__(self):
        return self.content
