from moviepy.editor import *
from skimage.filters import gaussian
from os.path import isfile, join
from os import listdir


class PrometeyEncoder:

    def __init__(self, config):
        self.config = config

    def get_duration(self, path):
        clip = VideoFileClip(path)
        duration = clip.duration
        clip.close()
        return duration

    def concat_clips(self, files, name):
        clips = [VideoFileClip(file).fx(vfx.resize, (720, 1280)) for file in files]
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(name, audio_codec='aac', temp_audiofile=f'{name}-audio.m4a', remove_temp=True)
        final_clip.close()
        for clip in clips:
            clip.close()

    def landscape_video(self, portrait_path, landscape_path):
        clip = VideoFileClip(portrait_path)

        # кропим задник
        crop_clip = clip.fx(vfx.crop, x1=0, y1=420, width=720, height=404)

        # блюр задника
        blur_clip = crop_clip.fl_image(lambda image: gaussian(image.astype(float), sigma=5))

        #перевод в fullHD задника
        back = blur_clip.fx(vfx.resize, (1920, 1080))

        #ресайз основы
        front = clip.fx(vfx.resize, (608, 1080))

        clips = [back, front.set_position("center")]

        if self.config['video_logo']:
            logo = (ImageClip(self.config['video_logo'])
              .set_duration(front.duration)
              .resize(height=130)
              .margin(right=15, bottom=15, opacity=0)
              .set_pos(("right","bottom")))
            clips.append(logo)

        final_clip = CompositeVideoClip(clips)
        final_clip.set_audio(front.audio)
        final_clip.write_videofile(f"{landscape_path}",
                                   audio_codec='aac',
                                   temp_audiofile=f'final-audio.m4a',
                                   remove_temp=True)
        back.close()
        front.close()
        for clip in clips:
            clip.close()
        final_clip.close()

if __name__ == "__main__":
    print("Test")
    path = "../temp/22/1.mp4"
    clip = VideoFileClip(path)
    print(clip.duration)

    # files = [join("21", f) for f in sorted(listdir("21")) if isfile(join("21", f))]
    # for file in files:
    #     clip = VideoFileClip(file)
    #     print(clip.size)