#!/usr/bin/env python3

"""
tts usage.
"""

import PySimpleGUI as sg
import pyttsx3
import os
import time

import asyncio
import edge_tts

from pydub import AudioSegment
from edge_tts import VoicesManager
#Edge TTS 全局变量
TEXT = "Hello World!"
VOICE = "zh-CN-YunjianNeural"
OUTPUT_FILE = "test.mp3"
async def _edgetts() -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)
# 语音包序号，默认第一个(中文)
voiceIdx = 0

# 主题色
sg.theme('DarkAmber')

# 窗口布局
layout = [
    [sg.Text('TEXT folder:'), sg.In(os.path.dirname(__file__), key='-LOADFOLDER-'), sg.FolderBrowse()],
     [sg.Text('MP3 folder:'), sg.In(os.path.dirname(__file__), key='-SAVEFOLDER-'), sg.FolderBrowse()],
    [sg.Text('请输入需要转换为语音的文字')],
    [sg.Multiline('', size=(100,10), key='textContent')],
    [sg.Text('调整速率')],
    [sg.Slider(range=(100,400), default_value=200, size=(50,15), orientation='horizontal', font=('Helvetica', 12), key='rateNumber')],
    [sg.Text('语音选项')],
    [sg.Radio('中文', 'S1', enable_events=True, key='id0', default=True),
     sg.Radio('日语', 'S1', enable_events=True, key='id1'),
     sg.Radio('英语', 'S1', enable_events=True, key='id2'),
     sg.Radio('中文(香港)', 'S1', enable_events=True, key='id3'),
     sg.Radio('中文(台湾)', 'S1', enable_events=True, key='id4'),],
    [sg.Button('试听', key='ttsButton1'), sg.Button('转换为MP3', key='ttsButton2'),sg.Button('转换为MP3(Edge)', key='ttsButton3')]
]

# 创建窗口
window = sg.Window('文字转语音工具', layout)

# 循环处理事件
while True:
    event, values = window.read()

    # 用户点击X关闭窗口或点击退出按钮
    if event == sg.WIN_CLOSED:
        break

    if event == 'id0':
        voiceIdx = 0
    if event == 'id1':
        voiceIdx = 1
    if event == 'id2':
        voiceIdx = 2
    if event == 'id3':
        voiceIdx = 3
    if event == 'id4':
        voiceIdx = 4
    print(voiceIdx)

    if event == 'ttsButton1' or event == 'ttsButton2' or event == 'ttsButton3':
        # 初始化
        tts = pyttsx3.init()

        # 获取新旧 RATE
        rate = tts.getProperty('rate')
        newRate = int(values['rateNumber'])
        # 修改 RATE
        tts.setProperty('rate', newRate)

        # # 获取 VOICES
        voices = tts.getProperty('voices')

        # # 修改 VOICE
        tts.setProperty('voice', voices[voiceIdx].id)

        # 获取文字
        textContent = values['textContent']
        
        # LOADFOLDER-
        loadfolder =values['-LOADFOLDER-']
        #print(loadfolder)
        
        # SaveFolder
        savefolder =values['-SAVEFOLDER-']
        #print(savefolder)
        # 试听
        if event == 'ttsButton1':
            tts.say(textContent)
            tts.runAndWait()
            tts.stop()

        #并转换为MP3
        if event == 'ttsButton2':
            

            # LOADFOLDER-
            loadfolder =values['-LOADFOLDER-']
            # SaveFolder
            savefolder =values['-SAVEFOLDER-']
            
            files= os.listdir(loadfolder) #得到文件夹下的所有文件名称
           
            for file in files: #遍历文件夹
                txts = []
                position = loadfolder +'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
                #print (position)           
                with open(position, "r",encoding='utf-8') as f:    #打开文件
                    data = f.read()   #读取文件
                    txts.append(data)
                textContent = ','.join(txts)#转化为非数组类型  
                #print (textContent)
                mp3Filename =  savefolder +'/'+ os.path.splitext(file)[0]+".wav"
                #print(mp3Filename)
                tts.save_to_file(textContent, mp3Filename)
                tts.runAndWait()
                song = AudioSegment.from_mp3(mp3Filename)
                song.export( savefolder +'/'+ os.path.splitext(file)[0]+'.mp3', format='mp3')
                #print(savefolder +'/'+ os.path.splitext(file)[0]+'.flac')
                #trans_mp3_to_wav(savefolder +'/'+  os.path.splitext(file)[0]+".mp3","ogg")
                info = '转换成功，详见：' + mp3Filename
                print(info)
                os.remove(savefolder +'/'+ os.path.splitext(file)[0]+".wav")
            
            #sg.popup('', info, '', title='提示')
        if event == 'ttsButton3':
            print("load ttsbutton3")
            # LOADFOLDER-
            loadfolder =values['-LOADFOLDER-']
            # SaveFolder
            savefolder =values['-SAVEFOLDER-']
            
            files= os.listdir(loadfolder) #得到文件夹下的所有文件名称
           
            for file in files: #遍历文件夹
                txts = []
                position = loadfolder +'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
                #print (position)           
                with open(position, "r",encoding='utf-8') as f:    #打开文件
                    data = f.read()   #读取文件
                    txts.append(data)
                textContent = ','.join(txts)#转化为非数组类型  
                #print (textContent)
                mp3Filename =  savefolder +'/'+ os.path.splitext(file)[0]+".mp3"
                OUTPUT_FILE=mp3Filename
                TEXT=textContent
                
                info = '转换成功，详见：' + OUTPUT_FILE
                print(info)
                if not os.path.exists(mp3Filename):
                    asyncio.get_event_loop().run_until_complete(_edgetts())
                
                    
                    #os.system("edge-tts "+ "--voice "+ VOICE+" --TEXT "+")
                    #song = AudioSegment.from_mp3(mp3Filename)
                    #song.export( savefolder +'/'+ os.path.splitext(file)[0]+'.mp3', format='mp3')
                    #print(savefolder +'/'+ os.path.splitext(file)[0]+'.flac')
                    #trans_mp3_to_wav(savefolder +'/'+  os.path.splitext(file)[0]+".mp3","ogg")
               
                    #os.remove(savefolder +'/'+ os.path.splitext(file)[0]+".wav")
            
        print("转换完毕")
            
           
            

window.close()


    
