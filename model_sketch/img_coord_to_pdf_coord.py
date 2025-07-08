def img_coord_to_pdf_coord(dpi_value, export_box) :
        scale = 72 / dpi_value # 이미지 좌표를 pdf 좌표로 변환할 때의 스케일
        pdf_box = (coord * scale for coord in export_box) # pdf의 좌표값을 하나씩 coord에 담아서 이미지 좌표 스케일로 보정
        return pdf_box