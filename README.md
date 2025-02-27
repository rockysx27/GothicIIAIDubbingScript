# GothicIIAIDubbingScript

What can this code do?

* You can find completely undubbed scripts, in your mods.
* Auto-dubbing for scripts (You have to set the voice manually for each character).
* Export to wav from mp3.


# EN

1. Install Python.
2. Open CMD in Admin.
2. 1. Paste into console: 
pip install pandas elevenlabs tkinter
3. Read Files inside 'INPUT_DUBBING' and 'OUTPUT_DUBBING', do what they say and remove them.
4. Open [Easy Gothic Mod Translator_V1.1](https://worldofplayers.ru/threads/41696/).
4. 1. Select the first language as the language you want to Dub - it doesn't matter what you select as the second language as we are not translating
4. 2. Skip 'Select Database'.
4. 3. Select the scripts.vdf from gothic/data for your mod (the name can vary) in Load 'Mod-file'.
4. 4. Skip 'Google Translation'.
4. 5. export BOTH in 'Export Database' section DB call 'DIALOGUES.csv' and the MT call 'REFERENCE.csv' - save them to the directory same as script.
4. 6. Skip to 'Translate Mod' or might break your translation.
5. Open 'START.py' in Notepad
5. 1. Change text API KEY and API VOICE KEY to your own [ElevenLabs](https://elevenlabs.io/app/settings/api-keys).
6. After generation, the files will be saved in .mp3 format. You can change them – find instructions for this in WAV_EXPORT.

# RU

1. Установите Python.
2. Откройте CMD от имени администратора.
2. 1. Вставьте в консоль:
pip install pandas elevenlabs tkinter
3. Прочитайте файлы в папках 'INPUT_DUBBING' и 'OUTPUT_DUBBING', выполните указания и удалите их.
4. Откройте [Easy Gothic Mod Translator_V1.1](https://worldofplayers.ru/threads/41696/).
4. 1. Выберите первый язык как язык, на который хотите дублировать — второй язык не имеет значения, так как мы не переводим.
4. 2. Пропустите 'Select Database'.
4. 3. Выберите файл scripts.vdf из gothic/data для вашего мода (имя может варьироваться) в разделе 'Load Mod-file'.
4. 4. Пропустите 'Google Translation'.
4. 5. Экспортируйте ОБА файла в разделе 'Export Database': базу данных (DB) под названием 'DIALOGUES.csv' и таблицу MT под названием 'REFERENCE.csv' — сохраните их в той же директории, что и скрипт.
4. 6. Пропустите 'Translate Mod', иначе перевод может сломаться.
5. Откройте 'START.py' в Блокноте.
5. 1. Измените текст API KEY и API VOICE KEY на ваши собственные ключи от [ElevenLabs](https://elevenlabs.io/app/settings/api-keys).
6. После генерации файлы будут сохранены в формате .mp3. Вы можете изменить их – инструкции по этому найдете в WAV_EXPORT.

# PL

1. Zainstaluj Pythona.
2. Otwórz CMD jako administrator.
2. 1. Wklej do konsoli:
pip install pandas elevenlabs tkinter
3. Przeczytaj pliki w folderach 'INPUT_DUBBING' i 'OUTPUT_DUBBING', wykonaj instrukcje i usuń je.
4. Otwórz [Easy Gothic Mod Translator_V1.1](https://worldofplayers.ru/threads/41696/).
4. 1. Wybierz pierwszy język jako język, na który chcesz dubbingować — nie ma znaczenia, jaki wybierzesz drugi język, ponieważ nie tłumaczymy.
4. 2. Pomiń 'Select Database'.
4. 3. Wybierz plik scripts.vdf z gothic/data dla twojego moda (nazwa może się różnić) w sekcji 'Load Mod-file'.
4. 4. Pomiń 'Google Translation'.
4. 5. Wyeksportuj OBA pliki w sekcji 'Export Database': bazę danych (DB) o nazwie 'DIALOGUES.csv' oraz tabelę MT o nazwie 'REFERENCE.csv' — zapisz je w tym samym katalogu co skrypt.
4. 6. Pomiń 'Translate Mod', inaczej może zepsuć twój tłumaczenie.
5. Otwórz 'START.py' w Notatniku.
5. 1. Zmień tekst API KEY i API VOICE KEY na swoje własne klucze z [ElevenLabs](https://elevenlabs.io/app/settings/api-keys).
6. Po wygenerowaniu pliki będą zapisane w formacie .mp3. Możesz je zmienić - znajdź instrukcje do tego w WAV_EXPORT.
