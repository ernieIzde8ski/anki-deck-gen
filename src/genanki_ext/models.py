from .model_data import read_model
from .str_classes import Model

__all__ = ["REVERSED_WITH_MEDIA_IN_FRONT", "REVERSED_WITH_FRONT_MEDIA_AND_TEXT_INPUT"]


REVERSED_WITH_MEDIA_IN_FRONT = Model(
    1760852270,
    "Basic & reversed media card (anki-deck-gen)",
    fields=[
        {"name": "MediaFile"},
        {"name": "Front", "font": "Arial"},
        {"name": "Back", "font": "Arial"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Front}}<br><br>{{MediaFile}}",
            "afmt": "{{Back}}\n\n<hr id=answer>\n\n{{FrontSide}}",
        },
        {
            "name": "Card 2",
            "qfmt": "{{Back}}",
            "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}<br>{{MediaFile}}",
        },
    ],
    css=".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n",
)

REVERSED_WITH_FRONT_MEDIA_AND_TEXT_INPUT = read_model("reversed_front_media_text_input")
