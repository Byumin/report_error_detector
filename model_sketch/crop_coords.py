from PIL import Image # 이미지 열고 자르고 저장
import json
import os

def crop_or_export(pdf_path, dpi_value, image_path, coords_path, output_path): # 크롭할 대상 이미지 경로, 크롭할 좌표, 크롭 결과 저장경로
    os.makedirs(output_path, exist_ok=True)
    text_in_box = None
    def img_coord_to_pdf_coord(dpi_value, export_box) :
        scale = 72 / dpi_value # 이미지 좌표를 pdf 좌표로 변환할 때의 스케일
        pdf_box = (coord * scale for coord in export_box) # pdf의 좌표값을 하나씩 coord에 담아서 이미지 좌표 스케일로 보정
        return pdf_box
    
    def pdf_crawling(pdf_box, pdf_path) :
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]

            # 추출할 좌표 영역 정의 (x0, top, x1, bottom)
            bbox = pdf_box

            # ① crop 영역 내 텍스트 전체 추출
            cropped_page = page.within_bbox(bbox)
            text_in_box = cropped_page.extract_text()
            print("해당 좌표 내 텍스트:")
            print(text_in_box)

            # ② crop 영역 내 단어별 정보 추출
            words_in_box = cropped_page.extract_words()
            for word in words_in_box:
                print(f"{word['text']:<20} (x0={word['x0']:.1f}, y0={word['top']:.1f})")
        return text_in_box
    
    try :
        img = Image.open(image_path)
        img_name = image_path.split("/")[-1]
        img_name = img_name.split(".")[0]
        print(img_name)
        print('이미지 불러옴', img)

        try :
            with open(coords_path, "r") as f :
                raw_coords = json.load(f)
                print('좌표 로딩 완료', raw_coords)
                for idx in range(len(raw_coords)) :
                    print(raw_coords[idx])
                    item = raw_coords[idx]
                    if item['label'] in ['bar', 'line'] :
                        (x0, y0) = item['bbox'][0]
                        (x1, y1) = item['bbox'][1]
                        crop_box = (x0, y0, x1, y1)
                        cropped = img.crop(crop_box)
                        out_path = os.path.join(output_path, f'{img_name}_crop_{item['label']}_{idx+1}.jpg')
                        cropped.save(out_path)
                        print(f'saged : {out_path}')
                    elif item['label'] in ['table'] :
                        print('크롭할 대상이 아님')
                        (x0, y0) = item['bbox'][0]
                        (x1, y1) = item['bbox'][1]
                        export_box = (x0, y0, x1, y1)
                        pdf_box = img_coord_to_pdf_coord(dpi_value, export_box)
                        text_in_box = pdf_crawling(pdf_box, pdf_path)
            
        except Exception as e :
            print('좌표 로딩 실패', e)
    except Exception as e :
        print('이미지 로딩 실패', e)
    return text_in_box

if __name__ == "__main__":
    pdf_path = "model_sketch/kcmii2_001.pdf"
    dpi_value = 300
    image_path = "model_sketch/page_1.jpg"
    coords_path = "model_sketch/coords_labeled.json"
    output_path = "model_sketch/cropped_images"

    crop_or_export(pdf_path, dpi_value, image_path, coords_path, output_path)