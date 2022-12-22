# ESTABLISH  16-46
# -*- Coding: utf-8 -*-

import os
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
date = str(datetime.datetime.now().strftime("%d-%m-%y"))

class Routes():
#    base_text_audio_url = BASE_DIR + "/recorder/audio_texts/"
    file_wav = str(datetime.datetime.now().strftime("%d_%m_%y__%H-%M-%S")) 
    create_mkdir=os.makedirs( 'recorder/' + date ,exist_ok=True)
    #base_audio_url = BASE_DIR + "/recorder/"
    base_audio_url = BASE_DIR + "/record/"
    file_wav = str(datetime.datetime.now().strftime("%d_%m_%y__%H-%M-%S")) + "_output"
    
    
#    table_name = BASE_DIR + "/recorder/database/.audios.csv"
#    icon_delete = BASE_DIR + "/recorder/icons/trash-button.png"
#    icon_play = BASE_DIR + "/recorder/icons/play-button.png"
#    icon_stop = BASE_DIR + "/recorder/icons/stop-button.png"
#    icon_clean = BASE_DIR + "/recorder/icons/clean-button.png"
#    icon_microphone = BASE_DIR + "/recorder/icons/microphone.png"
    

class Settings():
    language="es-ES"
 #   style_btn_default = "background-color: #B2BABB; color: #17202A;"
 #   style_btn_info = "background-color: #1A5276; color: #ECF0F1;"
 #   style_btn_success = "background-color: #117864; color: #ECF0F1;"
 #   style_btn_danger = "background-color: #CB4335; color: #ECF0F1;"