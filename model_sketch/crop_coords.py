from PIL import Image # 이미지 열고 자르고 저장
import json
import os

def crop_and_save(image_path, coords_path, output_dir): # 크롭할 대상 이미지 경로, 크롭할 좌표, 크롭 결과 저장경로
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(image_path)

    with open(coords_path, "r") as f :
        raw_coords = json.load(f)
    coords = [tuple(map(float, raw_coords[i:i+2])) + tuple(map(float, raw_coords[i+2:i+4]))
              for i in range(0, len(raw_coords)-3, 4)]

    for i, (x0, y0, x1, y1) in enumerate(coords):
        crop_box = (x0, y0, x1, y1)
        cropped = img.crop(crop_box)
        out_path = os.path.join(output_dir, f"crop_{i+1}.jpg")
        cropped.save(out_path)
        print(f"Saved: {out_path}")

if __name__ == "__main__":
    image_path = "model_sketch/page_1.jpg"
    coords_path = "model_sketch/coords.json"
    output_dir = "model_sketch/cropped_images"

    crop_and_save(image_path, coords_path, output_dir)