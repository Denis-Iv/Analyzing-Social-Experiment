from moviepy.editor import VideoFileClip

clip = VideoFileClip('output\\temp\\timelapse_original.mp4')
clip.write_videofile('output\\timelapse_optimized.mp4')