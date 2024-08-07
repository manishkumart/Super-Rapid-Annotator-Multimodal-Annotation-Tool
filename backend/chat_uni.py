from fastapi import FastAPI, File, UploadFile, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import torch
import os
from ChatUniVi.constants import *
from ChatUniVi.conversation import conv_templates, SeparatorStyle
from ChatUniVi.model.builder import load_pretrained_model
from ChatUniVi.utils import disable_torch_init
from ChatUniVi.mm_utils import tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria
from PIL import Image
from decord import VideoReader, cpu
import numpy as np
import asyncio
import sys

app = FastAPI()


# Global variables to store the model components
model = None
tokenizer = None
image_processor = None
loading_progress = 0

def _get_rawvideo_dec(video_path, image_processor, max_frames=MAX_IMAGE_LENGTH, image_resolution=224, video_framerate=1, s=None, e=None):
    if s is None:
        start_time, end_time = None, None
    else:
        start_time = int(s)
        end_time = int(e)
        start_time = start_time if start_time >= 0. else 0.
        end_time = end_time if end_time >= 0. else 0.
        if start_time > end_time:
            start_time, end_time = end_time, start_time
        elif start_time == end_time:
            end_time = start_time + 1

    if os.path.exists(video_path):
        vreader = VideoReader(video_path, ctx=cpu(0))
    else:
        print(video_path)
        raise FileNotFoundError

    fps = vreader.get_avg_fps()
    f_start = 0 if start_time is None else int(start_time * fps)
    f_end = int(min(1000000000 if end_time is None else end_time * fps, len(vreader) - 1))
    num_frames = f_end - f_start + 1
    if num_frames > 0:
        sample_fps = int(video_framerate)
        t_stride = int(round(float(fps) / sample_fps))

        all_pos = list(range(f_start, f_end + 1, t_stride))
        if len(all_pos) > max_frames:
            sample_pos = [all_pos[_] for _ in np.linspace(0, len(all_pos) - 1, num=max_frames, dtype=int)]
        else:
            sample_pos = all_pos

        patch_images = [Image.fromarray(f) for f in vreader.get_batch(sample_pos).asnumpy()]

        patch_images = torch.stack([image_processor.preprocess(img, return_tensors='pt')['pixel_values'][0] for img in patch_images])
        slice_len = patch_images.shape[0]

        return patch_images, slice_len
    else:
        print("video path: {} error.")

@app.on_event("startup")
async def load_model():
    global model, tokenizer, image_processor, loading_progress

    # Check if the model has already been loaded
    if model is not None:
        return

    disable_torch_init()

    model_path = "model_path"
    model_name = "ChatUniVi"

    loading_progress = 10
    await asyncio.sleep(1)  # Simulating progress step

    tokenizer, model, image_processor, context_len = load_pretrained_model(model_path, None, model_name)
    loading_progress = 50
    await asyncio.sleep(1)  # Simulating progress step

    mm_use_im_start_end = getattr(model.config, "mm_use_im_start_end", False)
    mm_use_im_patch_token = getattr(model.config, "mm_use_im_patch_token", True)
    if mm_use_im_patch_token:
        tokenizer.add_tokens([DEFAULT_IMAGE_PATCH_TOKEN], special_tokens=True)
    if mm_use_im_start_end:
        tokenizer.add_tokens([DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN], special_tokens=True)
    model.resize_token_embeddings(len(tokenizer))
    loading_progress = 70
    await asyncio.sleep(1)  # Simulating progress step

    vision_tower = model.get_vision_tower()
    if not vision_tower.is_loaded:
        vision_tower.load_model()
    image_processor = vision_tower.image_processor
    loading_progress = 100

@app.post("/process")
async def process_video(question: str = Form(...), video: UploadFile = File(...)):
    try:
        video_path = f"temp_{video.filename}"
        with open(video_path, "wb") as f:
            f.write(video.file.read())

        max_frames = 100
        video_framerate = 1

        video_frames, slice_len = _get_rawvideo_dec(video_path, image_processor, max_frames=max_frames, video_framerate=video_framerate)

        if model.config.mm_use_im_start_end:
            qs = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN * slice_len + DEFAULT_IM_END_TOKEN + '\n' + question
        else:
            qs = DEFAULT_IMAGE_TOKEN * slice_len + '\n' + question

        conv = conv_templates["simple"].copy()
        conv.append_message(conv.roles[0], qs)
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()

        input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).cuda()

        stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
        keywords = [stop_str]
        stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)

        with torch.inference_mode():
            output_ids = model.generate(
                input_ids,
                images=video_frames.half().cuda(),
                do_sample=True,
                temperature=0.2,
                top_p=None,
                num_beams=1,
                output_scores=True,
                return_dict_in_generate=True,
                max_new_tokens=1024,
                use_cache=True,
                stopping_criteria=[stopping_criteria]
            )

        output_ids = output_ids.sequences
        input_token_len = input_ids.shape[1]
        n_diff_input_output = (input_ids != output_ids[:, :input_token_len]).sum().item()
        if n_diff_input_output > 0:
            print(f'[Warning] {n_diff_input_output} output_ids are not the same as the input_ids')
        outputs = tokenizer.batch_decode(output_ids[:, input_token_len:], skip_special_tokens=True)[0]
        outputs = outputs.strip()
        if outputs.endswith(stop_str):
            outputs = outputs[:-len(stop_str)]
        outputs = outputs.strip()

        return {"answer": outputs}

    except Exception as e:
        return {"error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global loading_progress
    try:
        while loading_progress < 100:
            await websocket.send_json({"progress": loading_progress})
            await asyncio.sleep(1)
        await websocket.send_json({"progress": loading_progress, "status": "Model Loaded"})
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    finally:
        await websocket.close()

### HTML Page

@app.get("/", response_class=HTMLResponse)
async def get():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Question Answering</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
            }
            .form-group input[type="text"] {
                width: 100%;
                padding: 8px;
                box-sizing: border-box;
            }
            .form-group input[type="file"] {
                width: 100%;
                padding: 8px;
                box-sizing: border-box;
            }
            .form-group button {
                padding: 10px 15px;
                background-color: #007bff;
                color: #fff;
                border: none;
                cursor: pointer;
            }
            .form-group button:hover {
                background-color: #0056b3;
            }
            .result {
                margin-top: 20px;
                padding: 10px;
                border: 1px solid #ddd;
                background-color: #f9f9f9;
            }
            .progress {
                margin-top: 20px;
                padding: 10px;
                border: 1px solid #ddd;
                background-color: #f9f9f9;
            }
            #progress-bar {
                width: 0;
                height: 20px;
                background-color: #4caf50;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Video Question Answering</h1>
            <div class="progress">
                <div id="progress-bar"></div>
            </div>
            <div class="form-group">
                <label for="question">Question:</label>
                <input type="text" id="question" name="question">
            </div>
            <div class="form-group">
                <label for="video">Upload Video:</label>
                <input type="file" id="video" name="video">
            </div>
            <div class="form-group">
                <button onclick="submitForm()">Submit</button>
            </div>
            <div class="result" id="result"></div>
        </div>
        <script>
            const progressBar = document.getElementById('progress-bar');

            const ws = new WebSocket(`ws://${window.location.host}/ws`);
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.progress) {
                    progressBar.style.width = data.progress + '%';
                    if (data.progress == 100) {
                        ws.close();
                    }
                }
                if (data.status) {
                    progressBar.innerText = data.status;
                }
            };

            async function submitForm() {
                const question = document.getElementById('question').value;
                const video = document.getElementById('video').files[0];

                const formData = new FormData();
                formData.append('question', question);
                formData.append('video', video);

                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                document.getElementById('result').innerText = result.answer || result.error;
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)
