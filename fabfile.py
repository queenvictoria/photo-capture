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
  local("mogrify %s %s/*.%s" % (" ".join(args), source_directory, extension))

#  command = "ffmpeg -f image2 -r 25 -i %s/%s.%s -b 1000k %s" %
# (source_directory, "%d", new_extension, dest_file)
  command = "ffmpeg -f image2 \
    -r 25 \
    -i %s/%s.%s \
    -ab 1000k \
    -vb 2000k \
    -vbre hq \
    -acodec libfaac \
    -vcodec libx264 \
    -%s" % (source_directory, "%d", new_extension, dest_file)
  error = local(command, capture=True)
  print error


def distribute():
  """
  Upload to a social video service.
  """
  pass
