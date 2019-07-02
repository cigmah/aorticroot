"""
This is a (hopefully) one-off convenience script to generate
type definitions and helper functions for the Elm frontend
from the backend definitions of specialties and topics.
"""

from notes.models import Note

# Convert choices to Elm types

outfile_path = 'converted.elm'

# clear outfile
with open(outfile_path, 'w+') as outfile:
    pass

def double_newline(outfile):
    outfile.write('\n\n')

def to_type(string):
    """
    Converts a string to a valid elm type
    """

    return string.replace("_", " ").title().replace(" ","").replace("-","").replace("&","")

def create_types(choices, name : str):
    """
    choices is a tuple of type (int, string)
    """

    with open(outfile_path, 'a') as outfile:
        double_newline(outfile)

        outfile.write(f'type {name.capitalize()} \n    = ')

        choices_processed = [to_type(choice[1]) for choice in choices]
        choices_strings = "\n    | ".join(choices_processed)

        outfile.write(choices_strings)

        double_newline(outfile)

def create_to_int(choices, name : str):

    with open(outfile_path, 'a') as outfile:

        double_newline(outfile)

        outfile.write(f'toInt : {name} -> Int\ntoInt {name.lower()} = \n    case {name.lower()} of \n')

        choices_processed = [" " * 8 + to_type(choice[1]) + " -> " + str(choice[0]) + "\n"
                            for choice in choices]

        for processed in choices_processed:
            outfile.write(processed)

        double_newline(outfile)

def create_from_int(choices, name : str):

     with open(outfile_path, 'a') as outfile:

        double_newline(outfile)

        outfile.write(f'fromInt : Int -> {name}\nfromInt int = \n    case int of \n')

        choices_processed = [" " * 8 + str(choice[0]) + " -> " + to_type(choice[1]) + "\n"
                            for choice in choices]

        for processed in choices_processed:
            outfile.write(processed)

        double_newline(outfile)


def create_to_string(choices, name : str):

    with open(outfile_path, 'a') as outfile:

        double_newline(outfile)

        outfile.write(f'toString : {name} -> String\ntoString {name.lower()} = \n    case {name.lower()} of \n')

        choices_processed = [" " * 8 + to_type(choice[1]) + " -> \""+ choice[1].replace("_", " ").title() + "\"\n"
                            for choice in choices]

        for processed in choices_processed:
            outfile.write(processed)

        double_newline(outfile)

def create_list(choices, name : str):

    with open(outfile_path, 'a') as outfile:

        double_newline(outfile)

        outfile.write(f'list : List {name}\nlist = [\n    ')
        
        outfile.write("\n    , ".join([to_type(choice[1]) for choice in choices]))

        outfile.write("\n    ]")

        double_newline(outfile)

def create_all_from_choices(choices, name : str):
    create_types(choices, name)
    create_to_int(choices, name)
    create_from_int(choices, name)
    create_to_string(choices, name)
    create_list(choices, name)


def create_all():
    create_all_from_choices(Note.SPECIALTY_CHOICES, "Specialty")
    create_all_from_choices(Note.TOPIC_CHOICES, "Topic")
