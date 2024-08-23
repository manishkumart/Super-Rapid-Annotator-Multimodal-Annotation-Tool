import warnings
warnings.filterwarnings("ignore")
import gradio as gr
import re
from typing import Dict, List
import os
import gc
import torch
import pandas as pd
from src.video_model import describe_video 
from src.utils import parse_string, parse_annotations

# Function to save data to a CSV file using pandas
def save_to_csv(observations: List[Dict], output_dir: str = "outputs") -> str:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(observations)
    
    # Specify the CSV file path
    csv_file = os.path.join(output_dir, "video_observations.csv")
    
    # Save the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)
    
    return csv_file

# Function to process a single video and return the observation data
def process_single_video(video_path, standing, hands, location, screen) -> Dict:
    video_name = os.path.basename(video_path)  # Extract video name from the path
    query = "Describe this video in detail and answer the questions"
    additional_info = []
    if standing:
        additional_info.append("Is the subject in the video standing or sitting?\n")
    if hands:
        additional_info.append("Is the subject holding any object in their hands?\n")
    if location:
        additional_info.append("Is the subject present indoors?\n")
    if screen:
        additional_info.append("Is the subject interacting with a screen in the background by facing the screen?\n")
    
    end_query = """Provide the results in <annotation> tags, where 0 indicates False, 1 indicates True, follow these example below\n:
        <annotation>indoors: 0</annotation>
        <annotation>standing: 1</annotation>
        <annotation>hands.free: 0</annotation>
        <annotation>screen.interaction_yes: 0</annotation>
        """
    
    final_query = query + " " + " ".join(additional_info)
    final_prompt = final_query + " " + end_query
    
    # Assuming your describe_video function handles the video processing
    response = describe_video(video_path, final_prompt)
    final_response = f"<video_name>{video_name}</video_name>" + " \n" + response

    # Parse the response to extract video name and annotations
    parsed_content = parse_string(final_response, ["video_name", "annotation"])
    video_name = parsed_content['video_name'][0] if parsed_content['video_name'] else None
    annotations_dict = parse_annotations(parsed_content['annotation']) if parsed_content['annotation'] else {}

    # Return the observation as a dictionary
    return {'video_name': video_name, **annotations_dict}

# Function to process all videos in a folder
def process_multiple_videos(video_files: List[str], standing, hands, location, screen):
    all_observations = []

    for video_path in video_files:
        observation = process_single_video(video_path, standing, hands, location, screen)
        if observation['video_name']:  # Only add valid observations
            all_observations.append(observation)
        else:
            print("Error processing video:", video_path)  # Log any errors

        # Clear GPU cache
        torch.cuda.empty_cache()
        gc.collect() 

    # Save all observations to a CSV file and return the file path
    csv_file = save_to_csv(all_observations)
    return "Processing completed. Download the CSV file.", csv_file

# Gradio interface
def gradio_interface(video_files, standing, hands, location, screen):
    video_file_paths = [video.name for video in video_files]  # Extract file paths from uploaded files
    return process_multiple_videos(video_file_paths, standing, hands, location, screen)

# Inputs
video_files = gr.File(file_count="multiple", file_types=["video"], label="Upload multiple videos")
standing = gr.Checkbox(label="Standing")
hands = gr.Checkbox(label="Hands Free")
location = gr.Checkbox(label="Indoors")
screen = gr.Checkbox(label="Screen Interaction")

# Outputs
response = gr.Textbox(label="Status")
download_link = gr.File(label="Download CSV")

# Gradio interface setup
interface = gr.Interface(
    fn=gradio_interface,
    inputs=[video_files, standing, hands, location, screen],
    outputs=[response, download_link],
    title="GSoC Super Rapid Annotator - Batch Video Annotation",
    description="Upload multiple videos and process them sequentially, saving the results to a downloadable CSV file.",
    theme=gr.themes.Soft(primary_hue="red", secondary_hue="red"),
    allow_flagging="never"
)

# Launch interface
interface.launch(debug=False)
