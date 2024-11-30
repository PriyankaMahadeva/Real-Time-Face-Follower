# Real-Time-Face-Follower

Real-Time-Face-Follower is a face tracking project that uses computer vision techniques to detect and follow a person's face using a webcam. The project integrates OpenCV for image processing and Arduino for servo control, allowing for dynamic face tracking in real-time.

## Features

- Real-time face detection using Haar cascades.
- Movement detection through background subtraction.
- Face landmark detection with depth estimation using CVZone.
- Communication with Arduino for servo control based on face position.
- Visual feedback on distance to the detected face.

## Live model

![Demo Model](/Demo_image.jpg)

## Requirements

- Python 3.x
- Arduino IDE (for uploading the Arduino code)

### Python Libraries

Make sure to install the required Python libraries. You can use the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
