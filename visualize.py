# This code visualizes the detection results in tubes 
# NOTE: only support single person for now. 

import cv2 
import numpy as np 
import pickle             
import sys 
import argparse
import collections

# constant vars
ACTIONS = ['brush_hair', 'catch', 'clap', 'climb_stairs', 'golf', 'jump', 'kick_ball', 
			'pick', 'pour', 'pullup', 'push', 'run', 'shoot_ball', 'shoot_bow', 
			'shoot_gun', 'sit', 'stand', 'swing_baseball', 'throw', 'walk', 'wave']

COLORS = [ (127,255,127), (255,207,127), (255,150,199), (187,127,255), 
            (150,255,200), (200,150,255), (255,255,0), (0,255,255), (255,0,255)]

FONT = cv2.FONT_HERSHEY_SIMPLEX

# parse user input 
parser = argparse.ArgumentParser()

parser.add_argument('--frame_src', dest='frame_src')
parser.add_argument('--tube_src', dest='tube_src')
parser.add_argument('--vid_dst', default='res.mp4', dest='vid_dst')
parser.add_argument('--vid_size', default=(320, 240), dest='vid_size')
parser.add_argument('--vid_fps', default=10, dest='vid_fps')

args = parser.parse_args()


def add_dict(k, v, d):
	if k in d:
		d[k].append(v)
	else:
		d[k] = [v]


class Frame:
	def __init__(self, fid_):
		self.fid = fid_

		self.top_acts = []
		self.top_bboxes = []
		self.top_conf = []

	def add_action(self, act, conf, bbox):
		for i in range(len(self.top_conf)):
			if conf > self.top_conf[i]:
				self.top_conf.insert(i, conf)
				self.top_acts.insert(i, act)
				self.top_bboxes.insert(i, bbox)

		if len(self.top_conf) == 0:
			self.top_conf.insert(0, conf)
			self.top_acts.insert(0, act)
			self.top_bboxes.insert(0, bbox)

		

class Video_helper:

	def __init__(self, vid_dst, fps, size):
		fourcc = cv2.VideoWriter_fourcc(*'MP4V')
		self.out = cv2.VideoWriter(vid_dst,fourcc, fps, size)

	def write(self, img):
		self.out.write(img)

	def close(self):
		self.out.release()


'''
# format of tube pkl:
{
	action_class: [[
					[fid, x, y, w, h, conf]
					...
				]]
}
'''
def extract_tube(fname):
	res = {}
	data = pickle.load(open(fname,'r'))
	for act in range(len(data)):				# each action class 
		if len(data[act]) == 0:
			continue 

		for d in data[act][0][0]:
			fid = int(d[0])
			conf = d[-1]
			bbox = d[1:-1]

			if conf > 0.1:
				if not fid in res:
					res[fid] = Frame(fid)
				res[fid].add_action(act, conf, bbox)

	return collections.OrderedDict(sorted(res.items()))	# return sorted frames 


######################### MAIN 

vid_helper = Video_helper(args.vid_dst, args.vid_fps, args.vid_size)
tube_data = extract_tube(args.tube_src)

ks = tube_data.keys()
print('frames: %s' % `ks`)

for fid in ks:
	if fid % 10 == 0:
		print('processing frame %d' % fid)
	
	frame = cv2.imread(args.frame_src + '{:05d}.png'.format(fid))
	if tube_data[fid].top_conf == []:
		continue 

	bboxes = tube_data[fid].top_bboxes[0 : 3]
	# print(bbox)
	acts = tube_data[fid].top_acts[0 : 3]
	# print(acts)
	confs = tube_data[fid].top_conf[0 : 3]
	# print(confs)


	for i in range(len(acts)):
		cv2.putText(frame, ACTIONS[acts[i]] + ' : %0.2f' % confs[i], 
					(10, 10 + 15 * i), 
					fontFace=FONT, fontScale=0.5, 
					color=COLORS[acts[i] % len(COLORS)], thickness=2)

		b = map(int, bboxes[len(acts) - i - 1])
		cv2.rectangle(frame, (b[0], b[1]), (b[2], b[3]), 
						color=COLORS[acts[0] % len(COLORS)], thickness=2)

	vid_helper.write(frame)

vid_helper.close()	