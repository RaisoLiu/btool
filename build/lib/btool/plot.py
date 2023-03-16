import glob
import imageio.v2 as imageio

def imgs2gif(anim_file, img_folder):
  with imageio.get_writer(anim_file, mode='I') as writer:
      filenames = sorted(glob.glob(img_folder + '*.png'))
      for filename in filenames:
          image = imageio.imread(filename)
          writer.append_data(image)
      image = imageio.imread(filename)
      writer.append_data(image)
