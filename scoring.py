import librosa
from speech_inference import *
from speech_rate import *
from tokenizer_all import *
from audio_preprocessing import *
from flask import Flask, render_template, request, redirect, jsonify
import json 
import os 
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)

# 혹시 몰라 백업해야하면 사용하려고
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/voice', methods = ['GET', 'POST'])
def voice_scoring():
     # 테스트
     video_file = request.files['file']
     print(video_file)
     print("LOCAL FILE: FORM DATA RECEIVED")
          
     # post 테스트용. mp4 임시로 저장.
     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_video_file:
          video_file.save(tmp_video_file.name)
          input_video_path = tmp_video_file.name
          
     videoname = secure_filename(video_file.filename)
     filename = videoname.split('.')[0]+'.wav'
     audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
     extract_audio(input_video_path, audio_path)

     result = {}

     lang, text = whisper_inference(audio_path)
     
     result['language'] = lang
     result['inference'] = text
     
     audio, sample_rate = librosa.load(audio_path, sr=None)
     print("audio, sample_rate: ", audio, sample_rate)

     duration = librosa.get_duration(y=audio, sr=sample_rate)
     print(f"Audio Duration: {duration}")

     voice_level = get_mean_volume(audio_path, log=False)
     base_score = 100

     # 언어는 한(ko), 영(en)만 제공할 거라서 만약 한국어가 아니라면 당연히 영어
     if lang == 'ko':
          voice_intj = interjection_ko(text)
          syllable_count = tokenizer_ko(text)
          voice_speed = speech_rate_ko(duration, syllable_count)
          
          # speed 벌점 계산
          lower_speed, upper_speed = 4.0, 4.2
          
          if voice_speed < lower_speed:
               penalty_speed = (lower_speed - voice_speed) * 100 / lower_speed
          elif voice_speed > upper_speed:
               penalty_speed = (voice_speed - upper_speed) * 100 / (10 - upper_speed)
          else:
               penalty_speed = 0  # 범위(4.0~4.2) 내에 속하면 벌점X
          
          final_speed = base_score - penalty_speed

     else:
          voice_intj = interjection_en(text)
          word_count = tokenizer_en(text)
          voice_speed = speech_rate_en(duration, word_count)
          
          # speed 벌점 계산
          # WPM 범위
          lower_wpm, upper_wpm = 100, 150
          
          # 벌점 계산
          if voice_speed < lower_wpm:
               penalty_speed = (lower_wpm - voice_speed) * 2
          elif voice_speed > upper_wpm:
               penalty_speed = voice_speed - upper_wpm
          else:
               penalty_speed = 0  # 범위 내에 속하면 벌점 없음
          
          penalty_speed = min(penalty_speed, base_score)
          
          # 최종 점수 계산
          final_speed = base_score - penalty_speed
     
     # level:speed:intj=3:4:3 비율로 계산해서 voice_score 저장 필요
     
     # level 벌점 계산
     lower_level, upper_level = -25, -10
    
     # 벌점 계산
     if voice_level < lower_level:
          penalty_level = min(100, (lower_level - voice_level) * 2)
     elif voice_level > upper_level:
          if voice_level > 0:
               penalty_level = min(100, (voice_level - upper_level) * 5)
          else:
               penalty_level = min(100, (voice_level - upper_level) * 2)
     else:
          penalty_level = 0  # 범위(-25~-10) 내에 속하면 벌점X

     final_level = base_score - penalty_level

     
     # intj 벌점 계산
     standard_intj = 3
     if voice_intj > standard_intj:
          penalty_intj = (voice_intj-standard_intj) * 10
     else:
          penalty_intj = 0    # 잉여표현 3번 안 넘어가면 벌점X
     final_intj = base_score - penalty_intj
     
     # 최종 점수 계산
     voice_score = final_level*0.3 + final_speed*0.4 + final_intj*0.3
     
     result['voice_level'] = final_level
     result['voice_speed'] = final_speed
     result['voice_intj'] = final_intj
     result['voice_score'] = voice_score
     
     response = json.dumps(result, indent=4, ensure_ascii=False)
     print(response)
     print(type(response))
     
     return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)