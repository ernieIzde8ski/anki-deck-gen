# CHANGELOG

## 1.0.0

First major release. Expect breakage.

## devel

breaking changes:

- added new subclass of Note, overriding genanki's goofy
  `guid` implementation. This broke the Odyssée deck in the
  process.
  - First breakage I "solved" by deleting my original deck.
  - Second breakage was easy with this package:
    <https://ankiweb.net/shared/info/55394168>

new:

- add modules:
  - ankidg_core.base_model
  - ankidg_core.strtools
  - genanki_ext.model_data
  - genanki_ext.str_classes
- add note types:
  - REVERSED_WITH_FRONT_MEDIA_AND_TEXT_INPUT: similar to the
    other Reversed card I have, but requiring text input.
    Has a bunch of funny centering div logic.
- fix missing `__all__` attribute in genanki_ext.str_classes module
- add "Normal" and "Challenge" decks to L'Odyssée
- add log level customization
- add `--copy` flag to the `odyssee` command
- add CHANGELOG
