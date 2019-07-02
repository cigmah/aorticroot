from notes.models import Note

def add_note_combinations():
    """
    Adds notes for all combinations of specialties and topics in
    the Note model.
    """

    for specialty in Note.SPECIALTY_CHOICES:
        for topic in Note.TOPIC_CHOICES:

            title = (
                specialty[1].lower().replace("_"," ").title() +
                " - " +
                topic[1].lower().replace("_", " ").title()
            )

            Note.objects.get_or_create(
                specialty=specialty[0],
                topic=topic[0],
                title=title,
                content="",
            )

    return Note.objects.all()
