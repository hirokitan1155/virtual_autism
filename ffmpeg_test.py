import ffmpeg
import os
import re
import time
import whisper
import sys

model = whisper.load_model("medium")

files = os.listdir(os.getcwd())
md_files = [i for i in files if i.endswith('.csv') == True]
#print(file_list)

for F in md_files:
        basename_without_ext = os.path.splitext(os.path.basename(F))[0]
        print(basename_without_ext)

        if not os.path.exists(basename_without_ext): # ディレクトリが存在するか確認
                os.makedirs(basename_without_ext) # ディレクトリ作成
        CSV_Path=basename_without_ext+".csv"


        f = open(CSV_Path, 'r')
        
        for line in f:
                # 改行コードを取り除いてからカンマで分割
                data = line.strip().split(',')
                #print(data[2])
                dir = data[2]
                if not os.path.exists(basename_without_ext+"/"+dir): # ディレクトリが存在するか確認
                        os.makedirs(basename_without_ext+"/"+dir) # ディレクトリ作成
                new_str = re.search(r'=(.+)s',data[0]).group(1)
                new_str2 = re.search(r'=(.+)s',data[1]).group(1)
                #print(new_str,new_str2,float(new_str2)-float(new_str))
                start = float(new_str)
                duration=float(new_str2)-float(new_str)
                
                path_mp4=basename_without_ext+"/"+dir+"/"+new_str+"_"+new_str2+".mp4"
                path_mp3=basename_without_ext+"/"+dir+"/"+new_str+"_"+new_str2+".wav"
                path_trans=basename_without_ext+"/"+dir+"/"+new_str+"_"+new_str2+".trans"
                
                # audio-only
                path_source="../"+basename_without_ext+".mp4"
                stream = ffmpeg.input(path_source, ss=start, t=duration)
                stream = ffmpeg.output(stream, path_mp3, format='wav')
                
                ffmpeg.run(stream, overwrite_output=True)
                
                #image-audio
                stream2 = ffmpeg.input(path_source, ss=start, t=duration)
                stream2 = ffmpeg.output(stream2, path_mp4)
                ffmpeg.run(stream2, overwrite_output=True)
        
                # asr
                input_file = path_mp3
                result = model.transcribe(input_file, fp16=False,language="ja",initial_prompt="精神科医との対話")  # 音声データの文字起こし
                with open(path_trans,"w",encoding="utf-8-sig") as o:
        
                        for i in result['segments']:
                                print(f"{i['start']} to {i['end']}", file=o)
                                print(f"{i['text']}", file=o) 


