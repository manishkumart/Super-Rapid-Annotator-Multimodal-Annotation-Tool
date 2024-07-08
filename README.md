
<p align="center">
  <a href="https://sites.google.com/case.edu/techne-public-site/red-hen-rapid-annotator">
    <img src="https://user-images.githubusercontent.com/39674365/129477873-8c9b2191-8261-4ef9-a67f-94e5b57169bd.png" alt="Logo", width="300" height="300" >
  </a>
  <h1 align="center"> 🌟 Super Rapid Annotator 🌟</h1>
  <p align="center">
    Red Hen Lab's Super Rapid Annotator Powered By Large Language Models
    <br />
    <br />
  </p>
</p>


Welcome to the **Super Rapid Annotator** project! This tool is designed for video annotation by leveraging advanced multimodal vision and language models. 🚀

## 📚 Problem Statement

Annotating videos, especially identifying specific entities and their temporal relationships, is a complex and time-consuming task. Traditional methods lack efficiency and accuracy, particularly in handling multiple videos simultaneously. Our Super Rapid Annotator addresses these challenges by integrating state-of-the-art multimodal models with sophisticated spatial-temporal analysis, streamlining the annotation process.


## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FECC00?style=for-the-badge&logo=hugging-face&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-3D4AA6?style=for-the-badge&logo=gradio&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2960D3?style=for-the-badge&logo=pydantic&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=OpenCV&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)

## Prerequisites
![GPU](https://img.shields.io/badge/GPU-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![Storage](https://img.shields.io/badge/Storage-Min20GB-blue?style=for-the-badge)


## Setup

### Clone the Repository

First, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/manishkumart/Super-Rapid-Annotator-Multimodal-Annotation-Tool.git
cd Super-Rapid-Annotator-Multimodal-Annotation-Tool
```

### Create Virtual Environment

Create a virtual environment and install the required packages:

```bash
conda create -n env python=3.10 -y
conda activate env
pip install -r requirements.txt
npm i cors-anywhere
```

### Model Downloads

Download the necessary models using the below command:

```bash
python models/download_models.py --m1 ./models/ChatUniVi --m2 ./models/Phi3
```

## Backend Servers
You need three terminals for this. Run each of the following commands in three different terminals with the full path specified:

1. Start the `chat_uni` server responsible for video annotation.

    ```bash
    python backend/chat_uni.py --model_path <full_path>
    ```

    **This server will run on port** `8100`.

2. Start the `struct_phi3` server:

    ```bash
    python backend/struct_phi3.py --model_path <full_path>
    ```

    **This server will run on port** `8200`.

3. Start the Node.js server:

    ```bash
    npm install backend/server.js
    ```

    **This server will run on port** `8080`.

## Frontend Server
Open a new terminal and paste the below command 

```bash
python frontend/serve_html.py
```

**The frontend server can be accessed at [http://localhost:5500](http://localhost:5500).**

## Steps to Follow through the UI:

![40BB8366-D842-4840-8E71-E796AFE2A9C8](https://github.com/manishkumart/Super-Rapid-Annotator-Multimodal-Annotation-Tool/assets/37763863/62337212-e9d6-4a8b-b361-64c697978af3)

1. **Upload a Video**
   - Click on the **"Upload Video"** button to select and upload your video file.

2. **Select Annotation Options**
   - Choose any combination of the available annotation options:
     - Standing/Sitting
     - Screen Interactions or not
     - Hands free or not
     - Indoor/Outdoor

3. **Start the Annotation Process**
   - Click the **"Start"** button. This will display the selected options and the name of the uploaded video.

4. **Annotate the Video**
   - Click the **"Video Annotate"** button. This will use the prompt and the uploaded video to generate annotations.

5. **View the Prompt**
   - Click on the **"Prompt"** button to see the prompt used in the background based on the selected options.

6. **Get the Output**
   - Click the **"Output"** button to receive the structured output of the annotations.

## 📖 Blog Posts
- **An Experiment to Unlock Ollama’s Potential in Video Question Answering**: [Read here](https://medium.com/@manish.thota1999/an-experiment-to-unlock-ollamas-potential-video-question-answering-e2b4d1bfb5ba)
- **Vertical Scaling in Video Annotation with Large Language Models: A Journey with GSoC’24 @ Red Hen Labs**: [Read here](https://medium.com/@manish.thota1999/vertical-scaling-in-video-annotation-with-large-language-models-a-journey-with-gsoc24-a5dc9d6ffc87)
- **My Journey with Red Hen Labs at GSoC ’24**: [Read here](https://medium.com/@manish.thota1999/my-journey-with-red-hen-labs-at-gsoc-24-0ebc7f9f7ba6)
- **Why Google Summer Of Code?**: [Read here](https://medium.com/@manish.thota1999/why-google-summer-of-code-2-77-of-the-applicants-were-accepted-into-google-summer-of-code-2024-ec73a857b0ce)


## 🌟 Features

- [x] **Automatic Video Annotation**: Uses the best vision language models for rapid and accurate annotation.
- [x] **Multimodal Capabilities**: Combines vision and language models to enhance understanding and entity detection.
- [ ] **Concurrent Processing**: Efficiently processes multiple videos at once.
- [ ] **CSV Output**: Annotations are compiled into a user-friendly CSV format.

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


## 🙏 Acknowledgment

Special thanks to **Raúl Sánchez Sánchez** for his continuous support and guidance throughout this project.

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request.

## 🌎 Connect with me


For any questions, please reach out to me at LinkedIn

<div align="center">
<a href="https://www.linkedin.com/in/manishkumarthota/" target="_blank">
<img src=https://img.shields.io/badge/linkedin-%231E77B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white alt=linkedin style="margin-bottom: 5px;" />
   
