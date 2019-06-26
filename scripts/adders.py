from notes.models import Note

def add_notes_from_file(filename, year_level):
    """
    Adds notes from a specified file for a specified year level.
    """

    with open(filename) as infile:
        data = infile.readlines()

    adder = 'Note.objects.get_or_create(year_level=Note.{year_level}, specialty=Note.{specialty}, title="{title}", content="")\n'

    for line in data:
        print(line)
        specialty, title = line.split(', ')

        specialty = specialty.strip()
        title = title.strip()

        add_line = adder.format(
            year_level=year_level,
            specialty=specialty,
            title=title,
        )

        exec(add_line)

    return Note.objects.filter(year_level=Note.YEAR_4C)

def add_year4c():
    """
    Produces side effect of adding the year 4c note stubs.
    Should only be run once at initiation.
    """

    return add_notes_from_file("./data/year_4c.csv", 'YEAR_4C')
