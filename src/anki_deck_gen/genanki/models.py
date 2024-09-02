from .auto_model import AutoModel

__all__ = ["REVERSED_WITH_MEDIA_IN_FRONT"]
REVERSED_WITH_MEDIA_IN_FRONT = AutoModel(
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
