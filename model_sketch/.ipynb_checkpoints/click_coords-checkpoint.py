import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def click_coords(image_path):
    coords = []  # 클릭된 좌표를 저장할 리스트

    def onclick(event):
        if event.xdata is not None and event.ydata is not None: # event는 matplotlib의 이벤트 객체, xdata와 ydata는 moustevent의 인스턴트 객체
            coords.append((event.xdata, event.ydata)) # xdata, ydata 데이터를 coords 리스트에 저장 (튜플 형태로)
            print(f"클릭된 좌표: ({event.xdata:.2f}, {event.ydata:.2f})") # # xdata, ydata 프린팅
            ax.plot(event.xdata, event.ydata, 'ro')  # 해당 좌표 빨간 점 찍기
            fig.canvas.draw() # 빨간 점을 시각화 업데이트 해주기
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

    return coords

if __name__ == "__main__" :
    click_coords("page_1.jpg")