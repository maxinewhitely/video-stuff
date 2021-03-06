# Import requirements
from moviepy.editor import *
from ConfigParser import SafeConfigParser

#Read configuration file
parser = SafeConfigParser()
parser.read('example-data.ini')

#GLOBAL VARIABLES 
#Lists to hold text and video sub-clips
txt_clip_list = [i for i in range(len(parser.sections()))]
med_clip_list = [i for i in range(len(parser.sections()))]

#Finds length of all inputted media to determine global audio track duration
audio_duration = 0
def audioLength():
	global audio_duration
	audioBegin = 0
	audioEnd = 0	
	for m in parser.sections():
		audioBegin += parser.getint(m, 'start_time')
		audioEnd += parser.getint(m, 'end_time')
		audio_duration = audioEnd - audioBegin
	return audio_duration

#Makes individual text, media, and audio clips and then stitches them into one video
def compileVideo():
	#Global list indexers for inside the for loop
	i = 0
	j = 0

	#CONSTANT VARIABLES - values that apply to the entire video
	#Text
	tColor = parser.get('video0', 'text_color')
	tHighlight = parser.get('video0', 'text_highlight_color')
	tSize = parser.getint('video0', 'text_size')
	tBackground = parser.get('video0', 'text_background')
	#Audio
	global_audio = parser.get('video0', 'video_audio')
	audio_bool = parser.getboolean('video0', 'audio_setting')
	audio_length = audioLength()
	#File
	vid_fps = parser.getint('video0', 'frames_per_second')
	vid_codec = parser.get('video0', 'video_codec')
	file_name = parser.get('video0', 'save_as')

	for m in parser.sections():
		#For each video, set all variables via configuration file
		text = parser.get(m, 'clip_text')
		media = parser.get(m, 'media_link')
		tAlign = parser.get(m, 'text_align')
		tPlace = parser.get(m, 'text_place')
		clip_start = parser.getint(m, 'start_time')
		clip_end = parser.getint(m, 'end_time')
		text_duration = clip_end - clip_start

		#Make the text asset for each video in the config file
		txt_clip = TextClip(text, fontsize=tSize,color=tColor)
		txt_clip = txt_clip.set_position((20, 80)).set_duration(text_duration).fadein(.35).fadeout(.35)
		txt_clip_list[i] = txt_clip
		i += 1

		#Make the video asset for each video in the config file
		med_clip = VideoFileClip(media).subclip(clip_start, clip_end).fadein(.35).fadeout(.35)
		med_clip_list[j] = med_clip
		j += 1

	#Put together individual text/video clips into one successive text or video clip
	text_vid = concatenate_videoclips(txt_clip_list)
	media_vid = concatenate_videoclips(med_clip_list)
	audioclip = AudioFileClip(global_audio).set_duration(audio_length, change_end=True)

	#Overlay concatenated text clip onto concatenated video clip and output the final video
	video = CompositeVideoClip([media_vid, text_vid])
	video = video.set_audio(audioclip)
	video.write_videofile("knight_lab.mp4", fps=vid_fps, codec=vid_codec, audio=audio_bool)

compileVideo()
