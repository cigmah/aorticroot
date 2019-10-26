#!/usr/bin/env python

from notes.models import Note
import os
import glob
import dotenv
import time
import datetime
import csv

def initialise():
    """Initialise note markdown files.
    Run from python manage.py shell in the root directory.
    """
    note_id = 1
    initial_content = "There is currently no note content, however there may be EMQs available. You can check whether EMQs are available on the left hand side. We're adding notes as soon as we can, so stay tuned."
    for specialty in Note.SPECIALTY_CHOICES:
        for topic in Note.TOPIC_CHOICES:
            title = "__".join([f"{note_id:03d}", specialty[1], topic[1]])
            with open("./data/notes/" + title + ".md", "w") as file_handle:
                file_handle.write(initial_content)
            note_id += 1

def update():
    """Update any updated notes in notes directory with."""
    # Read the last updated CSV
    # Read the files in the notes directory
    note_files = sorted(glob.glob("./data/notes/*.md"))
    # Iterate through note files and check if updated
    for i, note in enumerate(note_files):
        note_id = i + 1

        with open(note, encoding="utf8") as file_handle:
            content = file_handle.read()

        note_object = Note.objects.filter(pk=note_id).get()
        note_object.content = content
        note_object.save()

        print(f"{note} was updated successfully.")
