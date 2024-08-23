import warnings
warnings.filterwarnings("ignore")
import gradio as gr
import pandas as pd
from src.video_model import describe_video  
from src.utils import parse_string, parse_annotations
import os

# --- Function to construct the final query --- 
def process_video_and_questions(video, standing, hands, location, screen):
    video_name = os.path.basename(video)
    query = f"Answer the questions from the video\n"
    additional_info = []
    if standing:
        additional_info.append("Is the subject in the video standing or sitting?\n")
    if hands:
        additional_info.append("Is the subject holding any object in their hands?\n")
    if location:
        additional_info.append("Is the subject present indoors?\n")
    if screen:
        additional_info.append("Is the subject interacting with a screen in the background by facing the screen?\n")
    
    end_query = """Provide the results in <annotation> tags, where 0 indicates False, 1 indicates True, and None indicates that no information is present. Follow the below examples\n:
        <annotation>indoors: 0</annotation>
        <annotation>standing: 1</annotation>
        <annotation>hands.free: 0</annotation>
        <annotation>screen.interaction_yes: 0</annotation>
        """

    final_query = query + " " + " ".join(additional_info)
    final_prompt = final_query + " " + end_query
    
    response = describe_video(video, final_prompt)
    final_response = f"<video_name>{video_name}</video_name>" + " \n" + response

    conditions = {
        'standing': (standing, 'standing: 1', 'standing: None'),
        'hands': (hands, 'hands.free: 1', 'hands.free: None'),
        'location': (location, 'indoors: 1', 'indoors: None'),
        'screen': (screen, 'screen.interaction_yes: 1', 'screen.interaction_yes: None')
    }
    
    for key, (condition, to_replace, replacement) in conditions.items():
        if not condition:
            final_response = final_response.replace(to_replace, replacement)
    
    return final_response 

def output_to_csv(final_response):
    parsed_content = parse_string(final_response, ["video_name", "annotation"])
    video_name = parsed_content['video_name'][0] if parsed_content['video_name'] else None
    annotations_dict = parse_annotations(parsed_content['annotation']) if parsed_content['annotation'] else {}
    
    df = pd.DataFrame([{'video_name': video_name, **annotations_dict}])
    
    # Save the DataFrame as a CSV file
    csv_file_path = f"{video_name}_annotations.csv"
    df.to_csv(csv_file_path, index=False)
    
    return csv_file_path  # Return the path to the CSV file for download

# Examples for the interface
examples = [
    ["videos/2016-01-01_0100_US_KNBC_Channel_4_News_1867.16-1871.38_now.mp4", True, False, True, False],
    ["videos/2016-01-01_0200_US_KNBC_Channel_4_News_1329.12-1333.29_tonight.mp4", False, True, True, True],
    ["videos/2016-01-01_0830_US_KNBC_Tonight_Show_with_Jimmy_Fallon_725.45-729.76_tonight.mp4", True, False, False, True],
    ["videos/2016-01-01_0200_US_KOCE_The_PBS_Newshour_577.03-581.31_tonight.mp4", False, True, True, False],
    ["videos/2016-01-01_1400_US_KTTV-FOX_Morning_News_at_6AM_1842.36-1846.68_this_year.mp4", True, True, False, False],
    ["videos/2016-01-02_0735_US_KCBS_Late_Show_with_Stephen_Colbert_285.94-290.67_this_year.mp4", False, True, True, True],
    ["videos/2016-01-13_2200_US_KTTV-FOX_The_Doctor_Oz_Show_1709.79-1714.17_this_month.mp4", True, False, False, True],
    ["videos/2016-01-01_1400_US_KTTV-FOX_Morning_News_at_6AM_1842.36-1846.68_this_year.mp4", False, True, True, False],
    ["videos/2016-01-01_1300_US_KNBC_Today_in_LA_at_5am_12.46-16.95_this_morning.mp4", True, False, False, True],
    ["videos/2016-01-05_0200_US_KNBC_Channel_4_News_1561.29-1565.95_next_week.mp4", False, True, True, False],
    ["videos/2016-01-28_0700_US_KNBC_Channel_4_News_at_11PM_629.56-633.99_in_the_future.mp4", True, False, False, True]
]

title = "GSoC Super Raid Annotator"
description = "Annotate Videos"
article = "<p style='text-align: center'><a href='https://github.com/OpenBMB/MiniCPM-V' target='_blank'>Model GitHub Repo</a> | <a href='https://huggingface.co/openbmb/MiniCPM-V-2_6' target='_blank'>Model Page</a></p>"

custom_theme = gr.themes.Soft(primary_hue="red", secondary_hue="red")

with gr.Blocks(theme=custom_theme) as demo:
    gr.Markdown(f"# {title}")
    gr.Markdown(description)
    gr.Markdown(article)
    
    with gr.Row():
        with gr.Column():
            video = gr.Video(label="Video")
            standing = gr.Checkbox(label="Standing")
            hands = gr.Checkbox(label="Hands Free")
            location = gr.Checkbox(label="Indoors")
            screen = gr.Checkbox(label="Screen Interaction")
            submit_btn = gr.Button("Generate Annotations")
            generate_csv_btn = gr.Button("Generate CSV")
        
        with gr.Column():
            response = gr.Textbox(label="Video Description", show_label=True, show_copy_button=True)
            csv_output = gr.File(label="Download CSV", interactive=False)
    
    submit_btn.click(
        fn=process_video_and_questions,
        inputs=[video, standing, hands, location, screen],
        outputs=response
    )
    
    generate_csv_btn.click(
        fn=output_to_csv,
        inputs=response,
        outputs=csv_output
    )
    
    gr.Examples(examples=examples, inputs=[video, standing, hands, location, screen])
    
demo.launch(debug=False)
