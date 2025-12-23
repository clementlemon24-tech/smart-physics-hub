import pyttsx3
import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import ImageSequenceClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import re
import os

def text_to_speech(text, filename='audio.wav'):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()

def create_text_clip(text, duration, fontsize=50, color='white', size=(400, 400)):
    return TextClip(text, fontsize=fontsize, color=color, bg_color='transparent', size=size).set_duration(duration)

def extract_key_calculations(text):
    # Simple extraction: find patterns like number op number = number
    pattern = r'(\d+\s*[\+\-\*\/]\s*\d+\s*=\s*\d+)'
    matches = re.findall(pattern, text)
    return matches

def create_avatar_frames(duration, fps=24):
    frames = []
    fig, ax = plt.subplots(figsize=(4, 4))
    # Simple avatar: head, body, mouth
    head = plt.Circle((0.5, 0.7), 0.1, color='yellow')
    body = plt.Rectangle((0.4, 0.3), 0.2, 0.4, color='blue')
    mouth = plt.Rectangle((0.45, 0.55), 0.1, 0.05, color='red')
    ax.add_patch(head)
    ax.add_patch(body)
    ax.add_patch(mouth)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    for frame in range(int(duration * fps)):
        # Animate mouth: open and close every 10 frames
        if (frame // 5) % 2 == 0:
            mouth.set_height(0.05)  # closed
        else:
            mouth.set_height(0.08)  # open
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        frames.append(image)
    plt.close(fig)
    return frames

def create_video(frames, audio_file, output_file='video.mp4', fps=24):
    clip = ImageSequenceClip(frames, fps=fps)
    audio = AudioFileClip(audio_file)
    clip = clip.set_audio(audio)
    clip.write_videofile(output_file, fps=fps, codec='libx264', audio_codec='aac')

def generate_teaching_video(lesson, output_file='lesson_video.mp4'):
    text = lesson.content
    audio_file = 'temp_audio.wav'
    text_to_speech(text, audio_file)
    audio = AudioFileClip(audio_file)
    duration = audio.duration
    frames = create_avatar_frames(duration)

    # Create main video clip
    main_clip = ImageSequenceClip(frames, fps=24).set_audio(audio)

    # Create title overlay
    title_clip = create_text_clip(lesson.topic, 3, fontsize=40).set_position('center').fadein(1).fadeout(1)

    # Extract key calculations
    calculations = extract_key_calculations(text)
    calc_text = '\n'.join(calculations) if calculations else ''
    calc_clip = None
    if calc_text:
        calc_clip = create_text_clip(calc_text, duration, fontsize=30).set_position(('center', 'bottom')).set_start(3)

    # Prepare clips for compositing
    clips = [title_clip]
    clips.append(main_clip.set_start(3))
    if calc_clip:
        clips.append(calc_clip.set_start(3))

    final_clip = CompositeVideoClip(clips)

    # Write video
    final_clip.write_videofile(output_file, fps=24, codec='libx264', audio_codec='aac')

    os.remove(audio_file)
    return output_file