
# 🌟 Super Rapid Annotator 🌟

## Development is in progress 👨🏻‍💻

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
