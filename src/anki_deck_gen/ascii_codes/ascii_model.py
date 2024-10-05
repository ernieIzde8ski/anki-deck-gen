from genanki_ext import Model

__all__ = []

_css = """
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}

.cloze {
    font-weight: bold;
    color: blue;
}

.nightMode .cloze {
    color: lightblue;
}

.mono {
    font-family: monospace;
}

table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}


table {
    /* Aligns this table in the center. */
    margin: 0px auto;
}

th {
    min-width: 100px;
    margin-left: 3px;
    margin-right: 3px;
    background: rgba(0, 0, 0, 0.3);
}

td {
    text-align: left;
    min-width: 200px;
    padding: 5px;
    padding-left: 20px;
    padding-right: 20px;
}
"""

CLOZE_WITH_ID = Model(
    2044012515,
    "ASCII cloze (anki-deck-gen)",
    model_type=Model.CLOZE,
    fields=[
        {"name": "Note ID"},
        {"name": "Text", "font": "Arial"},
        {"name": "Back Extra", "font": "Arial"},
    ],
    templates=[
        {
            "name": "Cloze",
            "qfmt": "{{cloze:Text}}",
            "afmt": "{{cloze:Text}}<br>\n{{Back Extra}}",
        }
    ],
    css=_css,
)
