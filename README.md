# 🌟 Super Rapid Annotator 🌟

## Development is in progress 👨🏻‍💻

Welcome to the **Super Rapid Annotator** project! This tool is designed to revolutionize video annotation by leveraging advanced multimodal vision and language models. 🚀

## 📚 Problem Statement

Annotating videos, especially identifying specific entities and their temporal relationships, is a complex and time-consuming task. Traditional methods lack efficiency and accuracy, particularly in handling multiple videos simultaneously. Our Super Rapid Annotator addresses these challenges by integrating state-of-the-art multimodal models with sophisticated spatial-temporal analysis, streamlining the annotation process.

## 🌟 Features

- **Automatic Video Annotation**: Uses the best vision language models for rapid and accurate annotation.
- **Multimodal Capabilities**: Combines vision and language models to enhance understanding and entity detection.
- **User-Friendly Interface**: Accessible through a Gradio application on Hugging Face.
- **Concurrent Processing**: Efficiently processes multiple videos at once.
- **CSV Output**: Annotations are compiled into a user-friendly CSV format.

## 🛠️ Tech Stack

- **Python** 🐍
- **PyTorch** 🔥
- **Hugging Face** 🤗
- **Gradio** 🎨
- **Pydantic** 🧩
- **CUDA** ⚙️
- **OpenCV** 📸
- **FFmpeg** 🎞️
- **FastAPI** 🚀

## 🎯 Goal and Objectives

Our main goal is to connect the best vision language models with an annotation framework. The specific objectives include:

1. **Model Replication and Interface Integration**:
   - Replicate the best vision language models.
   - Integrate the models within a Gradio interface on Hugging Face.

2. **Development and Enhancement of Processing Capabilities**:
   - Develop a class to structure LLM responses into formatted JSON.
   - Enable the processing of multiple videos in Gradio.
   - Implement the Instructor class to parse JSON structures from LLM responses.

3. **Testing and Validation**:
   - Perform initial tests with the JSON parser.
   - Ensure accurate capture and storage of annotations within a data frame.

4. **Comprehensive Evaluation**:
   - Conduct thorough testing to validate the entire annotation and integration process.

## 📖 Blog Posts

- **Vertical Scaling in Video Annotation with Large Language Models: A Journey with GSoC’24 @ Red Hen Labs**: [Read here](https://medium.com/@manish.thota1999/vertical-scaling-in-video-annotation-with-large-language-models-a-journey-with-gsoc24-a5dc9d6ffc87)
- **My Journey with Red Hen Labs at GSoC ’24**: [Read here](https://medium.com/@manish.thota1999/my-journey-with-red-hen-labs-at-gsoc-24-0ebc7f9f7ba6)
- **Why Google Summer Of Code?**: [Read here](https://medium.com/@manish.thota1999/why-google-summer-of-code-2-77-of-the-applicants-were-accepted-into-google-summer-of-code-2024-ec73a857b0ce)


## 📑 Findings and Insights

### Motivation
At Red Hen Labs, through Google Summer of Code, I am contributing to vertical growth by developing an annotation product for the video space using large language models. This approach ensures that we build effective, domain-specific applications rather than generic models.

### Importance of Structuring Models
We cannot always use models out of the box; hence, we must structure them well to achieve the desired outputs. Following the recommendations from the mentors, my first step is to test the capabilities of Video Large Language Models by annotating the following four key entities among many others:

1. **Screen Interaction**: Determine if the subject in the video is interacting with a screen in the background.
2. **Hands-Free**: Check if the subject’s hands are free or if they are holding anything.
3. **Indoors**: Identify whether the subject is indoors or outdoors.
4. **Standing**: Observe if the subject is sitting or standing.

### The Journey Ahead
We are in an era where new open-source models emerge monthly, continuously improving. This progress necessitates focusing on developing great products around these models, which involve vertical scaling, such as fine-tuning models for specific domains. This approach not only optimizes the use of existing models but also accelerates the development of practical and effective solutions.

### Dataset Preview
Here is a glimpse of the news dataset that we will be annotating, showcasing the real-world application of our annotation models.

### Video Frames and Key Entities
All of the video frames we analyzed are sourced from news segments, each lasting approximately 4–5 seconds. To accurately capture the main key entities from these models, I have extensively experimented with prompt engineering, employing multiple variations and different models. The most effective prompt, yielding outstanding results, is provided below.

### The Golden Prompt
For each question, analyze the given video carefully and base your answers on the observations made.

1. Examine the subject’s right and left hands in the video to check if they are holding anything like a microphone, book, paper (white color), object, or any electronic device, try segmentations and decide if the hands are free or not.
2. Evaluate the subject’s body posture and movement within the video. Are they standing upright with both feet planted firmly on the ground? If so, they are standing. If they seem to be seated, they are seated.
3. Assess the surroundings behind the subject in the video. Do they seem to interact with any visible screens, such as laptops, TVs, or digital billboards? If yes, then they are interacting with a screen. If not, they are not interacting with a screen.
4. Consider the broader environmental context shown in the video’s background. Are there signs of an open-air space, like greenery, structures, or people passing by? If so, it’s an outdoor setting. If the setting looks confined with furniture, walls, or home decorations, it’s an indoor environment.

By taking these factors into account when watching the video, please answer the questions accurately.

### Selecting the Best Model During the Coding Period (Research is Key)
During the coding period, extensive research was conducted to identify the best model for video processing. Among the latest research, the best model turned out to be Chat-UniVi. Kudos to the team behind it. The processing and description of the video using Chat-UniVi is by far the best.

Below is a comparison table of the various models we researched. This table includes a brief description and a link to each model’s repository for further exploration.

### Outstanding Features of Chat-UniVi
Chat-UniVi excels in processing and describing video content by capturing the spatial details necessary for images and the comprehensive temporal relationships required for videos. This model’s ability to handle both aspects makes it a standout choice for video processing tasks.

### Sample Input Video

#### Chat-UniVi Generated Output — Step 1

The woman in the video is standing and holding a microphone. She is standing in front of a bus and a news reporting set. The woman is not interacting with any visible screens, and there are no signs of greenery or people passing by in the background. Therefore, the setting is an Outdoor environment.

#### Structured Pydantic Output — Step 2

```json
{
  "screen_interaction_yes": 0,
  "hands_free": 0,
  "indoors": 0,
  "standing": 1
}

### 📂 Code References
# Project Directory Structure

## src
- **llm_helper.py**: Contains helper functions for working with language models.
- **main.py**: The main script to run the application.
- **mini.jpeg**: An image file used within the project.
- **model_loader.py**: Script for loading models.
- **video_analysis.py**: Script for analyzing video content.

## 🙏 Acknowledgment

Special thanks to **Raúl Sánchez Sánchez** for his continuous support and guidance throughout this project.

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request.

## 📧 Contact

For any questions, please reach out to me at [manish.thota1999@gmail.com](mailto:manish.thota1999@gmail.com).
