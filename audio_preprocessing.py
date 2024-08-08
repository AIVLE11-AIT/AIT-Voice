import ffmpeg
import re

def extract_audio(input_video_path, output_audio_path):
    try:
        probe = ffmpeg.probe(input_video_path)
        has_audio = any(stream for stream in probe['streams'] if stream['codec_type'] == 'audio')
        
        if not has_audio:
            raise ValueError(f"입력 파일 {input_video_path}에 오디오 스트림이 없습니다.")
        
        ffmpeg.input(input_video_path).output(output_audio_path).overwrite_output().run()
        print(f"저장된 오디오 파일 경로: {output_audio_path}")
    except ffmpeg.Error as e:
        print("FFmpeg 오류:", e)
        print("FFmpeg stderr 출력:", e.stderr.decode())
        raise
    except ValueError as ve:
        print("ValueError:", ve)
        raise


def get_mean_volume(audio_file, log=False):
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
