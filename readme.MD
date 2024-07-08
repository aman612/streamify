
# FastAPI Video Processing App

This FastAPI application provides endpoints for video processing, including streaming video, chunking video, combining videos, and creating thumbnails.

## Setup

1. **Clone the repository** (if applicable):

    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install the required dependencies**:

    ```sh
    pip install fastapi opencv-python moviepy
    ```

3. **Run the FastAPI application**:

    - In Development Mode:
        ```bash
        fastapi dev main.py
        ```
    - In Production Mode
         ```bash
        fastapi run main.py
        ```

## Endpoints

### 1. Stream Video

- **Endpoint**: `/stream-video`
- **Method**: GET
- **Description**: Streams a video file.

#### Curl Script

```sh
curl -X GET "http://localhost:8000/api/video/stream-video?video_path=/path/to/your/video.mp4"
```

### 2. Chunk Video

- **Endpoint**: `/chunk_video`
- **Method**: POST
- **Description**: Chunks a video into smaller segments of specified length.

#### Curl Script

```sh
curl -X POST "http://localhost:8000/api/video/chunk_video?chunk_length=10" -F "file=@/path/to/your/video.mp4"
```

### 3. Combine Videos

- **Endpoint**: `/combine-videos`
- **Method**: POST
- **Description**: Combines multiple video files into one video.

#### Curl Script

```sh
curl -X POST "http://localhost:8000/api/video/combine-videos" -F "files=@/path/to/your/video1.mp4" -F "files=@/path/to/your/video2.mp4"
```

### 4. Create Thumbnail

- **Endpoint**: `/create-thumbnail`
- **Method**: POST
- **Description**: Creates a thumbnail from a specified time in the video.

#### Curl Script

```sh
curl -X POST "http://localhost:8000/api/video/create-thumbnail?time=5" -F "file=@/path/to/your/video.mp4"
```

## File Structure

- `chunks/`: Directory to store video chunks.
- `combined/`: Directory to store combined video.
- `thumbnails/`: Directory to store video thumbnails.

## Dependencies

- **FastAPI**: Web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **opencv-python-headless**: OpenCV library for video processing.
- **moviepy**: A Python module for video editing.

## Running Tests

You can test the endpoints using the provided curl scripts or with tools like Postman.
