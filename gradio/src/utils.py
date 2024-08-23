# Importing the requirements
from PIL import Image
from decord import VideoReader, cpu
import re


# Maximum number of frames to use
MAX_NUM_FRAMES = 15  # If CUDA OOM, set a smaller number


def parse_string(string, tags):
    """
    Extracts the content between the specified HTML tags from the given string.

    Args:
        string (str): The input string to search for the tag content.
        tags (list): A list of HTML tags to search for.

    Returns:
        dict: A dictionary with tags as keys and lists of content as values.

     Example:
        >>> parse_string("<code>Hello, World!</code><note>Important</note>", ["code", "note"])
        {'code': ['Hello, World!'], 'note': ['Important']}
    """
    results = {}
    
    for tag in tags:
        pattern = rf"<{tag}>(.*?)</{tag}>"
        matches = re.findall(pattern, string, re.DOTALL)
        results[tag] = matches if matches else None

    return results


def parse_annotations(annotations_list):
    """
    Converts a list of annotations into a dictionary of key-value pairs.
    Args:
        annotations_list (list): A list of annotations in the format 'key: value'.
    Returns:
        dict: A dictionary with annotation keys and values.
    """
    annotations_dict = {}
    for annotation in annotations_list:
        key, value = annotation.split(': ')
        annotations_dict[key] = int(value)
    return annotations_dict




def encode_video(video_path):
    """
    Encodes a video file into a list of frames.

    Args:
        video_path (str): The path to the video file.

    Returns:
        list: A list of frames, where each frame is represented as an Image object.
    """

    def uniform_sample(l, n):
        """
        Uniformly samples elements from a list.

        Args:
            - l (list): The input list.
            - n (int): The number of elements to sample.

        Returns:
            list: A list of sampled elements.
        """
        gap = len(l) / n
        idxs = [int(i * gap + gap / 2) for i in range(n)]
        return [l[i] for i in idxs]

    # Read the video file and sample frames
    vr = VideoReader(video_path, ctx=cpu(0))
    sample_fps = round(vr.get_avg_fps() / 1)  # FPS
    frame_idx = [i for i in range(0, len(vr), sample_fps)]

    # Uniformly sample frames if the number of frames is too large
    if len(frame_idx) > MAX_NUM_FRAMES:
        frame_idx = uniform_sample(frame_idx, MAX_NUM_FRAMES)

    # Extract frames from the video
    frames = vr.get_batch(frame_idx).asnumpy()
    frames = [Image.fromarray(v.astype("uint8")) for v in frames]

    # Return video frames
    return frames
