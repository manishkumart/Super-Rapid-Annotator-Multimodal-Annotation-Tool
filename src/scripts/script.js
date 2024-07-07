let structOutput = ''; // Variable to store the struct output
let annotationOutput = ''; // Variable to store the annotation output
let videoAnnotationOutputs = []; // Array to store the video annotation outputs
let videoFileName = ''; // Variable to store the uploaded video file name
let annotationQuestions = ''; // Variable to store the annotation questions
let annotationPrompt = ''; // Variable to store the annotation prompt
let finalOutput = ''; // Variable to store the final output from the new API
let selectedOptions = { // Initialize selected options
    standingSitting: false,
    handsFree: false,
    screenInteractions: false,
    indoorOutdoor: false
};

document.getElementById('video-upload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    videoFileName = file.name; // Store the file name
    const videoContainer = document.getElementById('video-container');
    const videoElement = document.getElementById('uploaded-video');
    
    if (file) {
        const videoURL = URL.createObjectURL(file);
        videoElement.src = videoURL;
        videoContainer.style.display = 'block'; // Show the video container
    }
});

document.getElementById('options-btn').addEventListener('click', function() {
    const standingSitting = document.getElementById('standing-sitting').checked;
    const handsFree = document.getElementById('hands-free').checked;
    const screenInteractions = document.getElementById('screen-interactions').checked;
    const indoorOutdoor = document.getElementById('indoor-outdoor').checked;

    let output = '<h3>Selected Options:</h3>';
    annotationQuestions = ''; // Reset annotation questions
    annotationPrompt = 'For each question, analyze the given video carefully and base your answers on the observations made. ';
    selectedOptions = { // Reset selected options
        standingSitting: false,
        handsFree: false,
        screenInteractions: false,
        indoorOutdoor: false
    };

    videoAnnotationOutputs = []; // Reset video annotation outputs

    if (handsFree) {
        output += '<p>Hands free</p>';
        annotationQuestions += "Is the subject's holding anything in any of their hands?";
        selectedOptions.handsFree = true;
        startVideoAnnotationTask('Hands free', "Is the subject's hand holding anything in any of their hands?");
    }
    if (standingSitting) {
        output += '<p>Standing/Sitting</p>';
        annotationQuestions += 'Is the subject standing or sitting in the video?';
        selectedOptions.standingSitting = true;
        startVideoAnnotationTask('Standing/Sitting', 'Is the subject standing or sitting in the video?');
    }
    if (screenInteractions) {
        output += '<p>Screen Interactions</p>';
        annotationQuestions += 'Assess the surroundings behind the subject in the video. Do they seem to interact with any visible screens, such as laptops, TVs, or digital billboards? If yes, then they are interacting with a screen. If not, they are not interacting with a screen. ';
        selectedOptions.screenInteractions = true;
        startVideoAnnotationTask('Screen Interactions', 'Assess the surroundings behind the subject in the video. Do they seem to interact with any visible screens, such as laptops, TVs, or digital billboards? If yes, then they are interacting with a screen. If not, they are not interacting with a screen.');
    }
    if (indoorOutdoor) {
        output += '<p>Indoor/Outdoor</p>';
        annotationQuestions += 'Consider the broader environmental context shown in the video’s background. Are there signs of an open-air space, like greenery, structures, or people passing by? If so, it’s an outdoor setting. If the setting looks confined with furniture, walls, or home decorations, it’s an indoor environment. ';
        selectedOptions.indoorOutdoor = true;
        startVideoAnnotationTask('Indoor/Outdoor', 'Consider the broader environmental context shown in the video’s background. Are there signs of an open-air space, like greenery, structures, or people passing by? If so, it’s an outdoor setting. If the setting looks confined with furniture, walls, or home decorations, it’s an indoor environment.');
    }

    if (!handsFree && !standingSitting && !screenInteractions && !indoorOutdoor) {
        output = '<p>No options selected.</p>';
    }

    document.getElementById('combined-output').innerHTML = output + `<h4>Video File Name: ${videoFileName}</h4>`;

    annotationPrompt += annotationQuestions + ' By taking these factors into account when watching the video, please answer the questions accurately.';

    const selectedOptionsData = {
        prompt: annotationPrompt,
        max_tokens: 500
    };

    // Start background tasks
    startAnnotationTask(selectedOptionsData);
});

function startAnnotationTask(selectedOptionsData) {
    fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(selectedOptionsData)
    })
    .then(response => response.json())
    .then(data => {
        annotationOutput = `<h3>Annotation Output:</h3>
                            <p>${data.result}</p>`;
    })
    .catch(error => {
        console.error('Error:', error);
        annotationOutput = `<h3>Annotation Output:</h3>
                            <p>Error processing request</p>`;
    });
}

function startVideoAnnotationTask(option, question) {
    const videoFile = document.getElementById('video-upload').files[0];
    if (!videoFile) {
        videoAnnotationOutputs.push({ option, answer: '<p>Please upload a video to proceed with annotation.</p>' });
        return;
    }

    const formData = new FormData();
    formData.append('question', question);
    formData.append('video', videoFile);

    const proxyUrl = 'http://localhost:8080/';
    const targetUrl = 'http://127.0.0.1:8100/process';

    fetch(proxyUrl + targetUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.text()) // Get raw text response
    .then(text => {
        if (isJSON(text)) {
            const data = JSON.parse(text); // Attempt to parse JSON
            console.log('Response from server:', data);
            const answer = data.answer;
            videoAnnotationOutputs.push({ option, answer }); // Store the option and answer
            // Automatically call the new API with the concatenated video annotation output
            callFinalOutputAPI(videoAnnotationOutputs.map(output => output.answer).join(' '));
        } else {
            console.error('Response is not JSON:', text);
            videoAnnotationOutputs.push({ option, answer: `Error processing the video annotation request. Response text: ${text}` });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        videoAnnotationOutputs.push({ option, answer: `Error processing the video annotation request: ${error.message}` });
    });
}

function callFinalOutputAPI(videoAnnotation) {
    const finalOutputData = {
        llm_output: videoAnnotation
    };

    const proxyUrl = 'http://localhost:8080/';
    const targetUrl = 'http://0.0.0.0:8200/process_llm_output/';

    fetch(proxyUrl + targetUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(finalOutputData)
    })
    .then(response => response.text()) // Get raw text response
    .then(text => {
        if (isJSON(text)) {
            const data = JSON.parse(text); // Attempt to parse JSON
            console.log('Response from final output API:', data);
            finalOutput = '<h3>Final Output:</h3>';
            if (selectedOptions.screenInteractions) {
                finalOutput += `<p><strong>Screen Interaction:</strong> ${data.screen_interaction_yes ? 'Yes' : 'No'}</p>`;
            }
            if (selectedOptions.handsFree) {
                finalOutput += `<p><strong>Hands Free:</strong> ${data.hands_free ? 'Yes' : 'No'}</p>`;
            }
            if (selectedOptions.indoorOutdoor) {
                finalOutput += `<p><strong>Indoors:</strong> ${data.indoors ? 'Yes' : 'No'}</p>`;
            }
            if (selectedOptions.standingSitting) {
                finalOutput += `<p><strong>Standing:</strong> ${data.standing ? 'Yes' : 'No'}</p>`;
            }
        } else {
            console.error('Response is not JSON:', text);
            finalOutput = `<h3>Final Output:</h3>
                           <p>Error processing final output request. Response text: ${text}</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        finalOutput = `<h3>Final Output:</h3>
                       <p>Error processing final output request: ${error.message}</p>`;
    });
}

function isJSON(text) {
    try {
        JSON.parse(text);
        return true;
    } catch (error) {
        return false;
    }
}

document.getElementById('prompt-btn').addEventListener('click', function() {
    document.getElementById('annotation-output').innerHTML = `<h3>Annotation Prompt:</h3><p>${annotationPrompt}</p>`;
});

document.getElementById('video-annotate-btn').addEventListener('click', function() {
    let outputHTML = '<h3>Video Annotation Output:</h3>';
    videoAnnotationOutputs.forEach(output => {
        outputHTML += `<h4>${output.option}</h4><p>${output.answer}</p>`;
    });
    document.getElementById('video-annotation-output').innerHTML = outputHTML;
});

document.getElementById('output-btn').addEventListener('click', function() {
    document.getElementById('final-output').innerHTML = finalOutput;
});
