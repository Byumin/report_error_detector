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