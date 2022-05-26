from moviepy.editor import VideoFileClip

clip = VideoFileClip('output\\final\\timelapse_official.mp4')
clip.write_videofile('output\\final\\timelapse_optimized.mp4')