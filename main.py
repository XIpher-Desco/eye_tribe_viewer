import tkinter
from PIL import ImageTk
from peyetribe.peyetribe import EyeTribe
import numpy


# peyetribe の初期化
tracker = EyeTribe()
tracker.connect()
n = tracker.next()

tracker.pushmode()

# frame の root の作成
eye_tribe_root = tkinter.Tk()
eye_tribe_root.configure(bg="green", bd=10)
# eye_tribe_root.wm_attributes("-transparentcolor", "snow")

eye_tribe_root.geometry(
    "640x360"
    )
eye_tribe_root.title(
    "アイトラッカー表示トラッカーアプリ"
    )

# info_text = tkinter.StringVar()
# info_text.set("aaaaaaaaaaaaaaaaaaaaaa")
# raw_data_label  = tkinter.Label(eye_tribe_root, textvariable=info_text)
# raw_data_label.grid()

canvas = tkinter.Canvas(
    eye_tribe_root,
    width = 640,
    height = 360,
    relief = "flat",
    bd = 0,
    bg = "green",
    highlightthickness=0
    )

canvas.grid()

# ターゲット画像を開く
target_image = ImageTk.PhotoImage(file = "2_32.png")

gaze_history_num = 5

gaze_history_x = [1 for i in range(gaze_history_num)]
gaze_history_y = [1 for i in range(gaze_history_num)]
gaze_point_x = 1
gaze_point_y = 1

def repeat():
    global target_image
    #ここに定期的に実行する処理を記述する
    # canvas.create_oval(i-5, i-5, i+5, i+5, fill="blue")
    global gaze_point_x
    global gaze_point_y
    n = tracker.next()
    # info_text.set(str(n.raw)+";"+str(n.avg) +";"+str(n.timestamp))
    if not(n.avg.x == 0 and n.avg.y == 0):
        gaze_point_x=n.avg.x/4
        gaze_point_y=n.avg.y/4

    # avg
    gaze_history_x.append(gaze_point_x)
    if len(gaze_history_x) > gaze_history_num:
        gaze_history_x.pop(0)

    render_x_pos = numpy.average(gaze_history_x)
    
    gaze_history_y.append(gaze_point_y)
    if len(gaze_history_y) > gaze_history_num:
        gaze_history_y.pop(0)

    render_y_pos = numpy.average(gaze_history_y)


    # print(n)
    canvas.delete('gaze_point')
    # canvas.create_oval(render_x_pos-10, render_y_pos-10, render_x_pos+10, render_y_pos+10, fill="green", outline="white", width=5, tag='gaze_point')
    canvas.create_image(
        render_x_pos,
        render_y_pos,
        image = target_image,
        tag='gaze_point'
        )

    eye_tribe_root.after(10, repeat)

eye_tribe_root.after(100, repeat)

eye_tribe_root.mainloop()

tracker.pullmode()

tracker.close()
