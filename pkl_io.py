import pickle              # import module first
import sys 

def read_pkl(fname):
	f = open(fname, 'r')   # 'r' for reading; can be omitted
	mydict = pickle.load(f)         # load file content as mydict
	f.close()     
	return mydict
	    

def write_pkl(d, fname):
	pickle.dump(d, open(fname, 'w'))


def create_dict():
	data = {}
	data['labels'] = ['brush_hair', 'catch', 'clap', 'climb_stairs', 'golf', 'jump', 'kick_ball', 'pick', 'pour', 'pullup', 'push', 'run', 'shoot_ball', 'shoot_bow', 'shoot_gun', 'sit', 'stand', 'swing_baseball', 'throw', 'walk', 'wave']
	data['gttubes'] = []
	data['nframes'] = {'walk/kestrel':450}
	data['train_videos'] = []
	data['test_videos'] = [['walk/kestrel']]
	data['resolution'] = {'walk/kestrel':(240, 360)}
	
	return data 


# data = read_pkl(sys.argv[1])
# print(data['labels'])

data = create_dict()
write_pkl(data, sys.argv[1])



# format of pkl cache ######### 
# labels: [label1, label2, ...]
# gttubes: [..]
# nframes: number of frames for each folder : {vid_name : frame_size} 
# train_videos: [['vid_name'], [], []]  # three parts
# test_videos: same 
# resolution: {vid_name : (hei, wid)}


