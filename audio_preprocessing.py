import ffmpeg
import re

def extract_audio(input_video_path, output_audio_path):
    print(type(input_video_path), type(output_audio_path))
    
    ffmpeg.input(input_video_path).output(output_audio_path).overwrite_output().run()

    print(f"SAVED AUDIO FILE PATH: {output_audio_path}")


def get_mean_volume(audio_file, log=True):
    try:
        # ffmpeg-python을 사용하여 FFmpeg 명령어를 설정 및 실행
        _, out = (
            ffmpeg
            .input(audio_file)
            .filter('volumedetect')
            .output('null', format='null')
            .run(capture_stdout=True, capture_stderr=True)
        )

        if log:
            print("FFmpeg 로그 출력:\n", out.decode())

        # FFmpeg stderr 로그에서 mean_volume 추출
        mean_volume_match = re.search(r"mean_volume:\s+([-+]?[\d.]+)\s+dB", out.decode())
        
        if mean_volume_match:
            mean_volume = float(mean_volume_match.group(1))
            return mean_volume
        else:
            raise ValueError("mean_volume 값을 찾을 수 없습니다.")
    except ffmpeg.Error as e:
        print(e.stderr.decode())
        raise
