from import os.path import join
from glob import glob
import imageio.v2 as imageio
from tqdm import tqdm

def imgs2gif(ani, imgs):
  
  with imageio.get_writer(ani, mode='I') as writer:
      li = sorted(glob(join(imgs, '*.png')))
      print(f"Find {len(li)} picture(s)")
      for it in tqdm(li):
          image = imageio.imread(it)
          writer.append_data(image)
  
