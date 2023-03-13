# -*- coding: utf-8 -*-
import pyttsx3
import PySimpleGUI as sg
import ntpath
import re


engine = pyttsx3.init()


def replace(txt):
    # strings to replace / remove
    # example with Page number and crlf
    regex = r'Page\|[0-9]{1,3}'
    txt = txt.replace("\n", " ").replace("\r"," ")
    txt = re.sub(regex, '', txt)
    return txt


def TTS(text, filename):
    head, tail = ntpath.split(filename)
    tail = tail.replace(".txt", "")
    outfile = tail + ".wav"
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
    engine.save_to_file(text, outfile)
    engine.runAndWait()


def getText(Path):
    file = open(Path, encoding="utf8")
    txt = file.read()
    txt = replace(txt)
    print(txt, flush=True)
    file.close()
    return txt


if __name__ == "__main__":
    layout = [[sg.Text('TXT TTS')],
              [sg.FolderBrowse(target='-USER FOLDER-'), sg.Text("Path:                                                    ")],
              [sg.Button("TTS"), sg.Button("Close")]]
    window = sg.Window('URL TTS', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == "TTS":
            filename = values["-IN-"]
            TTS(getText(filename), filename)            
            window.close()
        if event == "Close":
            window.close()
    window.close()    
