# Contributing

If your name isn't Ernie, then first off, thanks for checking out the project!
Otherwise, here's a refresher.

## General

Unless you want to modify the tooling, you can find source files to update in
the `media` directory. Compilation instructions are deck-specific.

## L'Odyssée (TTS Quebec)

Run `python .` to build the L'Odyssée deck. This will work until another
subcommand is added, at which point I believe the command you have to use is
`python . l-odyssee`.

The command-line tool will auto-discover new audio files, so you do not need to
worry about editing the lockfile yourself. Files without associated audio files
will be silently ignored. All you need to do is insert new audio files and run
the tool. If you have a list of words, phrases, or corrections you'd like to
submit, file an issue instead and I will generate the audio for you.

Audio is generated at <https://hearling.com/clips>, with Language set to French,
Dialect set to French (Canada), and Voice set to B Standard Male. Uncertain if
this is the most Quebecois-sounding option, might have to ask the French
speakers I know.
