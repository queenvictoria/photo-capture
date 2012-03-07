from fabric.api import local, cd
from datetime import datetime
import os
import glob


def capture(interval=5, source_directory=None):
  """
  Capture stills to the local drive.
  """
  interval = int(interval)
  if not source_directory:
    source_directory = datetime.now().strftime("%Y%m%d-%H%M%S")
    print source_directory
    try:
      os.mkdir(source_directory)
    except:
      pass
  with cd(source_directory):
# http://sourceforge.net/apps/mediawiki/gphoto/index.php?title=Capture_examples
#Capture_Targets

    try:
      local("gphoto2 \
        --set-config capturetarget=0 \
        --capture-image-and-download \
        -I %d"
        % (interval))
    except:
      pass

  return source_directory


def composite(source_directory=".", extension="jpg", dest_file="output.mp4",
  rotate=None, size=(1920, 1024)):
  """
  Stitch stills in to a compliant mp4 video.
  """
# if the input format isn't understood by ffmpeg normalize the images first
  new_extension = extension
  preprocess = False
  args = [
    "-size %dx%d" % (size[0], size[0]),
    "-resize %dx%d" % (size[0], size[0]),
    "-gravity Center",
    "-crop %dx%d+0+0 +repage" % (size[0], size[1]),
    "-depth 8",
    "-colorspace RGB"]
  if extension == "cr2":
    args.append(" -format png")
    new_extension = "png"
  if rotate:
    args.append("-rotate %d" % int(rotate))
  if preprocess:
    local("mogrify %s %s/*.%s" % (" ".join(args), source_directory, extension))

#  command = "ffmpeg -f image2 -r 25 -i %s/%s.%s -b 1000k %s" %
# (source_directory, "%d", new_extension, dest_file)

#	loop through the directory symlinking images to their index numbers
  i = 1
  local("rm %s/symlink-*.%s" % (source_directory, new_extension))
  for filename in sorted(glob.glob(os.path.join(source_directory, '*.%s' % new_extension))):
    symlink = os.path.join(source_directory, 'symlink-%d.%s' % (i, new_extension))
    local("ln -sf %s %s" % (filename, symlink))
    i += 1

  command = "ffmpeg -f image2 \
    -r 25 \
    -i %s/%s.%s \
    -ab 1000k \
    -vb 2000k \
    -vpre hq \
    -acodec libfaac \
    -vcodec libx264 \
    -%s" % (source_directory, "symlink-%d", new_extension, dest_file)
  error = local(command, capture=True)
  print error
  
  local("rm %s/symlink-*.%s" % (source_directory, new_extension))

def distribute():
  """
  Upload to a social video service.
  """
  pass
