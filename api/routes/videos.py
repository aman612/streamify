import cv2, os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from moviepy.editor import VideoFileClip, concatenate_videoclips
from typing import Generator, Any


router = APIRouter()

CHUNK_DIR = "app/static/chunks"
THUMBNAIL_DIR = "app/static/thumbnail"
COMBINE_VIDEO_DIR = "app/static/combine"

os.makedirs(CHUNK_DIR, exist_ok=True)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)
os.makedirs(COMBINE_VIDEO_DIR, exist_ok=True)


@router.post("/combine-videos")
async def combine_videos_handler(files: list[UploadFile] = File(...)) -> dict[str, str]:
    video_paths = []
    for file in files:
        video_path = f"uploaded_{file.filename}"
        with open(video_path, "wb") as buffer:
            buffer.write(await file.read())
        video_paths.append(video_path)

    clips = [VideoFileClip(video) for video in video_paths]
    final_clip = concatenate_videoclips(clips)
    output_path = f"{COMBINE_VIDEO_DIR}/combined_video.mp4"
    final_clip.write_videofile(output_path, codec="libx264")

    os.remove(video_path)

    return {"message": "Combine Video Created Successfully!", "path": output_path}


@router.post("/create-thumbnail")
async def video_thumbnail_handler(
    file: UploadFile = File(...), time: int = 5
) -> dict[str, str]:
    video_path = f"uploaded_{file.filename}"
    thumbnail_path = f"{THUMBNAIL_DIR}/thumbnail_{file.filename}.jpg"

    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())

    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, time * 1000)
    success, frame = cap.read()

    if success:
        cv2.imwrite(thumbnail_path, frame)
    cap.release()

    os.remove(video_path)

    return {"message": "Thumbnail Created Successfully!", "path": thumbnail_path}


@router.post("/chunk-video")
async def video_chunk_handler(
    file: UploadFile = File(...), chunk_length: int = 5
) -> dict[str, str]:
    video_path = f"uploaded_{file.filename}"
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())

    video = VideoFileClip(video_path)
    duration = video.duration

    for i in range(0, int(duration), chunk_length):
        start = i
        end = min(i + chunk_length, duration)
        chunk = video.subclip(start, end)
        chunk.write_videofile(
            f"{CHUNK_DIR}/chunk_{i // chunk_length}.mp4", codec="libx264"
        )

    os.remove(video_path)

    return {"message": "Video Chunked Successfully!", "path": CHUNK_DIR}


@router.get("/stream-video")
async def video_stream_handler(video_path: str) -> StreamingResponse:
    def generate_frames(video_path) -> Generator[bytes, Any, None]:
        cap = cv2.VideoCapture(video_path)
        while True:
            success, frame = cap.read()
            if not success:
                break
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    return StreamingResponse(
        generate_frames(video_path),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
