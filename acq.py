from pseyepy import Camera, Stream, Display, cam_count
import time, sys, cv2, os

#################### PARAMS START HERE ####################

# experiment params
data_dir = os.path.join(os.getcwd(), 'data')

# camera params
resolution = Camera.RES_LARGE
fps = 30

#################### PARAMS END HERE ####################

def int_input(*args, default=10, **kwargs):
    while True:
        inp = input(*args, **kwargs)
        try:
            if inp == '':
                return default
            inp = int(inp)
            break
        except:
            pass
    return inp

# expt name
expt_name = input('\nEnter unique experiment name:\n').replace('/','-')
exp_data_dir = os.path.join(data_dir, expt_name)
if os.path.exists(exp_data_dir):
    cont = input('\nExperiment folder with this name already exists.\nAre you sure you want to continue? (y/n)\n')
    if cont != 'y':
        quit()
os.makedirs(exp_data_dir, exist_ok=True)

# setup camera
assert cam_count() > 0, '\n\nCamera not detected. Is it plugged into the computer? If so, trying unplugging and replugging, then run again.\n\n\n'
cam = Camera(resolution=resolution, fps=fps)

# main loop
ans = ''
dur = 10 # random default
used_ids = []
while True:
    ans = input("\nMain menu:\n\t'r' to record\n\t'd' to display\n\t'reset' to reset camera\n\t'q' to quit\n")

    if ans == 'q':
        break
    
    elif ans == 'd':
        # inspect camera
        d = Display(cam)
        
    elif ans == 'reset':
        cam.end()
        cam = Camera(resolution=resolution, fps=fps)
    
    elif ans == 'r':
        expt_subname = input('Enter trial ID: ').replace('/','-')
        if expt_subname in used_ids:
            print('\nTrial ID already used.')
            continue
        expt_file = os.path.join(exp_data_dir, expt_name+'_'+expt_subname)
        expt_file += '.avi'
        
        dur = int_input('\nEnter experiment duration in seconds:\nHit enter to default to previous (={} secs)\n'.format(dur), default=dur)
        
        # setup stream
        stream = Stream(cam, file_name=expt_file)

        # wait for duration of experiment
        print('Acquiring for {} seconds...'.format(dur), flush=True)
        t0 = time.time()
        while time.time()-t0 < dur:
            time.sleep(.200)

        stream.end()
        used_ids.append(expt_subname)
    
cam.end()
print('\nExperiment complete.\n\n\n', flush=True)


