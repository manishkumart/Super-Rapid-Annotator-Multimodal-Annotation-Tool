
# 🌟 Super Rapid Annotator 🌟

Welcome to the **Super Rapid Annotator** project! This tool is designed to revolutionize video annotation by leveraging advanced multimodal vision and language models. 🚀

## 📚 Problem Statement

Annotating videos, especially identifying specific entities and their temporal relationships, is a complex and time-consuming task. Traditional methods lack efficiency and accuracy, particularly in handling multiple videos simultaneously. Our Super Rapid Annotator addresses these challenges by integrating state-of-the-art multimodal models with sophisticated spatial-temporal analysis, streamlining the annotation process.

## 🌟 Features

- **Automatic Video Annotation**: Uses PG-Video-LLaVA model for rapid and accurate annotation.
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

## 🎯 Goal and Objectives

Our main goal is to connect the Multimodal vision language model LLaVA-V1.5-13b with an annotation framework. The specific objectives include:

1. **Model Replication and Interface Integration**:
   - Replicate the PG-Video-LLaVA model.
   - Integrate the model within a Gradio interface on Hugging Face.

2. **Development and Enhancement of Processing Capabilities**:
   - Develop a class to structure LLM responses into formatted JSON.
   - Enable the processing of multiple videos in Gradio.
   - Implement the Instructor class to parse JSON structures from LLM responses.

3. **Testing and Validation**:
   - Perform initial tests with the JSON parser.
   - Ensure accurate capture and storage of annotations within a data frame.

4. **Comprehensive Evaluation**:
   - Conduct thorough testing to validate the entire annotation and integration process.

## 📈 Methods and High-Level Design

Our implementation is based on the PG-Video-LLaVA model, chosen for its superior spatio-temporal and entity extraction capabilities. The workflow involves:

1. **Input**: Video and JSON inputs.
2. **Video Processing**:
   - Scene Detection: Breaks down videos into frames for entity extraction.
   - Vision and Language Adapter: Processes video frames for spatial and temporal feature extraction.
3. **Text Processing**:
   - JSON Parsing: Extracts structured outputs from LLM responses.
4. **Output**: JSON parsing results are compiled into a CSV file.

## 🖼️ High-Level Design
![prop_arch](https://github.com/manishkumart/Super-Rapid-Annotator-Multimodal-Annotation-Tool/assets/37763863/c34d8b34-4c77-4803-b0c4-c35823643e20)


## ⏱️ Performance

- Initial Model Load: 3 seconds
- Grounding & Tracking (5s Video): 1 second
- Entity Matching: 1 second
- Multimodal Vision: 1 second
- LLM Response: 1 second
- JSON Parsing: 1 second
- Annotation Saving: 1 second

Total annotation time for 50 videos (~5 seconds each) is approximately 5.05 minutes using an RTX 3090 Ti.

## 📝 Progress/Blog

- **Blog-0**: [My Journey with Red Hen Labs at GSOC '24](https://medium.com/@manish.thota1999/my-journey-with-red-hen-labs-at-gsoc-24-0ebc7f9f7ba6)
- **Blog-1**: [Why Google Summer of Code? 2.77% of the Applicants were Accepted into Google Summer of Code 2024](https://medium.com/@manish.thota1999/why-google-summer-of-code-2-77-of-the-applicants-were-accepted-into-google-summer-of-code-2024-ec73a857b0ce)


## 🙏 Acknowledgment

Special thanks to **Raúl Sánchez Sánchez** for his continuous support and guidance throughout this project.

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request.

## 📧 Contact

For any questions, please reach out to me at [manish.thota1999@gmail.com](mailto:manish.thota1999@gmail.com).
