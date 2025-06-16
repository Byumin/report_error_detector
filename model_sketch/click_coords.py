import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json

def click_coords(image_path, save_path="coords.json"):
    coords = []  # 클릭된 좌표를 저장할 리스트

    # 클릭 이벤트에 반응하는 인터렉션을 정의하는 함수
    def onclick(event):
        if event.xdata is not None and event.ydata is not None: # event는 matplotlib의 이벤트 객체, xdata와 ydata는 moustevent의 인스턴트 객체
            x, y = event.xdata, event.ydata
            coords.append([x, y]) # 한쌍의 좌표 데이터를 coords 리스트에 저장 (리스트 형태로)
            print(f"클릭된 좌표: ({event.xdata:.2f}, {event.ydata:.2f})") # # xdata, ydata 프린팅
            ax.plot(event.xdata, event.ydata, 'ro')  # 해당 좌표 빨간 점 찍기
            fig.canvas.draw() # 빨간 점을 시각화 업데이트 해주기

            if len(coords) == 2 :
                print("2개의 점이 지정되었습니다. 해장 박스의 클래스명을 입력해주세요.")
                label = input("클래스명 (예 : bar, line, table) : ").strip()
                label #### 어떠한 구조로 저장할지 검토 중 25.06.17
    img = mpimg.imread(image_path)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_title("click_image")
    fig.canvas.mpl_connect('button_press_event', onclick)
    # fig 데이터 구성 정보만 가지고 있는 층
    # canvas 실제로 그려주는 역할 
    # mpl_connect() 인자로 액션과 그 액션에서 발생하는 함수
    plt.show()
    # 마지막에 왜 보여주는거임?
    # re : 이벤트 리스터를 명시해주고 plt.show() 실행하는 순간 이벤트 리스터는 동작하게 되어 있음.
    # re : 즉 이벤트 리스터를 동작시켜라 라는 의미의 신호 같은 역할 + 시각화 플롯을 열어주는 역할
    with open(save_path, "w") as f :
        json.dump(coords, f)
    print(f"총 {len(coords)}개의 좌표가 저장되었습니다 -> {save_path}")

    return coords

if __name__ == "__main__" :
    click_coords("model_sketch/page_1.jpg")