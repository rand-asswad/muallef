from os.path import splitext, basename
from subprocess import Popen, PIPE

output_dir = "figures/out/"


def output_name(file, format='png'):
    base = splitext(basename(file))[0]
    output = output_dir + base + '.' + format
    return output


def combine_audio_video(video_file, audio_file, output_file=None):
    if output_file:
        output_path = output_file
    else:
        output_path = output_dir + 'audio/' + basename(video_file)

    args = [
        'ffmpeg',
        '-i', video_file,
        '-i', audio_file,
        '-shortest',
        output_path,
    ]

    process = Popen(args, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    output, error = output.decode(), error.decode()
    return output, error
