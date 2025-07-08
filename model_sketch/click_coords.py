import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import TextBox, Button # GUI 위젯을 시각화에 삽입하기 위한 도구
import json
'''
!!! 수정 및 확인해야하는 사항
1. pdf->image 변환하는 작업
2. image에서 좌표를 지정했을 때 크롭하는 함수에서 정상적인 좌표로 크롭이 되는지
2-1. 좌표 json 형태가 크롭하는 함수에서 어떻게 받는지
2-2. 해당 좌표로 잘 크롭이 되는지
'''
def click_coords_with_gui(image_path, save_path="model_sketch/coords_labeled.json"): # 전체 인터페이스를 담당하는 메인 GUI 함수
    coords = []  # 클릭된 좌표를 저장할 리스트
    labeled_bbox = [] # 리스트로 딕셔너리(객체)들 묶기
    current_label = [""] # TextBox에서 받은 텍스트 저장. 리스트로 감싸야 내부 함수에서 변경 가능 (클로저 문제 때문) ??
    '''
    클로저란?
    함수 안에서 정의된 내부 함수가 바깥 함수의 지역 변수에 접근할 수 있는 구조를 의미
    리스트로 감싸는 이유는 리스트가 mutable 객체로 내부 함수에서도 내용 변경이 가능해지기 때문에
    
    ""의 의미
    빈 문자를 의미함
    리스트 안에 빈 문자를 넣어서 "current_label[0] =" 사용하여 덮어쓰기를 하는 것
    ""가 없이 그냥 리스트를 쓰는 경우 비어있는 리스트이기 때문에 current_label[0] 위치에 존재하는 것이 없어 오류가 발생함
    또한 최신 하나의 값만을 가지고 관리할 수 있어 통제가 간단해짐
    '''
    img = mpimg.imread(image_path)
    fig, ax = plt.subplots()
    # 하단 버튼 공간 확보를 위해
    plt.subplots_adjust(bottom=0.25)  # 서브플롯의 위치 및 여백을 수동으로 조정하는 함수 (하단으로부터 0.25 이후 이미지 시작)

    ax.imshow(img)
    ax.set_title("Click 2 points for each box, then enter label and click 'Save Box'")

    # TextBox (라벨 입력창)
    axbox = plt.axes([0.1, 0.1, 0.3, 0.05])  # [left, bottom, width, height] 창 내 위치 비율
    label_text_box = TextBox(axbox, "Label: ") #TextBox() 사용자가 입력할 수 있는 GUI 텍스트 박스

##########################################################

    # 클릭 이벤트에 반응하는 인터렉션을 정의하는 함수
    def onclick(event):
        if event.inaxes == ax and event.xdata and event.ydata :
            if len(coords) < 2 :
                x, y = event.xdata, event.ydata
                coords.append([x,y])
                ax.plot(x,y,'ro')
                fig.canvas.draw()
                print(f"좌표 선택됨 : ({x:1f}, {y:1f})")
            else :
                print("이미 2개의 좌표가 선택됨. 저장 후 다음 박스를 지정하세요.")
    '''
    fig : 전체 플롯을 담는 최상위 객체
    .canvas : 그림판 역할을 하는 하위 객체 (시각화 이벤트를 실제로 처리함)
    .mpl_connect : 핸들러 함수를 등록하기 위한 연결 함수
    'button_press_event' : 마우스 클릭 시 발생하는 이벤트 (matplotlib에서 사용하는 이벤트 정의)
    onclick : 사용자가 클릭했을 때 실행될 함수
    '''
    fig.canvas.mpl_connect('button_press_event', onclick)

##########################################################

    def submit_label(text) : # 사용자가 TextBox에 텍스트 입력 후 Enter 누르면 실행됨
        current_label[0] = text.strip() # 입력값은 current_label[0] 위치에 저장
        print("임시 저장되었습니다.")
    '''
    label_text_box. : 사용자가 텍스트를 입력할 수 있는 작은 입력창
    .on_submit : label_text_box에서 엔터를 눌렀을 때 자동으로 실행될 핸들러 함수를 지정하는 역할
    '''
    label_text_box.on_submit(submit_label) # 핸들러 함수를 TextBox에 연결함

##########################################################

    # Button (저장버튼)
    axbutton = plt.axes([0.5, 0.1, 0.15, 0.05]) # 버튼 위치 및 크기
    '''
    Button : 그래픽 인터페이스 상에서 버튼을 생성함
    axbutton : 이 버튼이 그려질 위치를 정의한 Axes 객체
    "Save box" : 버튼에 표시될 텍스트
    '''
    button = Button(axbutton, "Save box") # 버튼 객체 생성

    def save_box(event) : # 버튼 클릭 시 실행되는 함수
        if len(coords) == 2 and current_label[0] != "": # 좌표에 2개, 라벨이 비어있지 않은 상태 조건
            labeled_bbox.append({
                "label": current_label[0],
                "bbox": coords.copy()
            })
            print(f"저장 완료: label = {current_label[0]}, bbox = {coords}")
            coords.clear() # 좌표값 초기화
            ax.set_title("Click 2 points for next box")
            fig.canvas.draw() # ? 이건 왜 있는거지
        else:
            print("❗ 박스 좌표 2개와 라벨을 입력하세요.")
    '''
    button : 위에서 만든 버튼 객체
    .on_clicked : 버튼을 클릭했을 때 실행할 핸들러 함수 등록
    save_box : 버튼이 눌릴 때 실행될 함수 이름
    '''
    button.on_clicked(save_box) # 버튼 객체에 save_box() 함수 연결

    plt.show()
    
    # 저장
    with open(save_path, "w") as f:
        json.dump(labeled_bbox, f, indent=2)
    print(f"\n✅ 전체 {len(labeled_bbox)}개 박스가 저장되었습니다 → {save_path}")

if __name__ == "__main__" :
    click_coords_with_gui("model_sketch/page_1.jpg")