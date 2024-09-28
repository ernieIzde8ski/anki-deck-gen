# CHANGELOG

## 1.0.0

First major release. Expect breakage.

## devel

breaking changes:

- added new "Note" subclass without genanki's goofy `guid`
  implementation, breaking the Odyssée deck in the process
  - Only solution I could find was deleting the original
    deck. Bye, progress.

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
- add CHANGELOG
