from genanki.model import Model

from .auto_model import AutoModel

__all__ = ["REVERSED_WITH_MEDIA_IN_FRONT"]
REVERSED_WITH_MEDIA_IN_FRONT = Model(
    1760852270,
    "Basic (and reversed card) (genanki)",
    fields=[
        {"name": "Front", "font": "Arial"},
        {"name": "Back", "font": "Arial"},
        {"name": "MediaFile"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{MediaFile}}<br>{{Front}}",
            "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}",
        },
        {
            "name": "Card 2",
            "qfmt": "{{Back}}",
            "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}<br>{{MediaFile}}",
        },
    ],
    css=".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n",
)

# Documentation suggests this approach over using a GUID:
# https://docs.ankiweb.net/importing/text-files.html#guid-column
CLOZE_WITH_ID = Model(
    2044012515,
    "Cloze (anki-deck-gen)",
    model_type=AutoModel.CLOZE,
    fields=[
        {"name": "Deck ID"},
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
    css=".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n\n"
    ".cloze {\n font-weight: bold;\n color: blue;\n}\n.nightMode .cloze {\n color: lightblue;\n}",
)
