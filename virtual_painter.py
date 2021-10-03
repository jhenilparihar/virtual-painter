import cv2
import numpy as np
import os
import HandTracking as ht
# import ctypes

# Get the window size and calculate the center
# user32 = ctypes.windll.user32
# win_x, win_y = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
# win_cnt_x, win_cnt_y = [user32.GetSystemMetrics(0)/2, user32.GetSystemMetrics(1)/2]
#

cam_width, cam_height = 1280, 680

file_list = os.listdir("navbar")
navbar_list = []
for image_path in file_list:
    image = cv2.imread(f"navbar/{image_path}")
    navbar_list.append(image)
navbar = navbar_list[1]

file_list = os.listdir("colors")
color_bar_list = []
for i, image_path in enumerate(file_list):
    image = cv2.imread(f"colors/{i+1}.png")
    color_bar_list.append(image)
color_bar = color_bar_list[1]

clear = cv2.imread("CLEAR ALL.png")

##############################################
previous_time = 0
xp, yp = 0, 0
brush_thickness = 7
draw_color = (255, 0, 0)
erase = False
draw_color_list = [(240, 240, 240), (255, 0, 0), (92, 225, 230), (255, 54, 0), (43, 255, 0), (7, 84, 40),
                   (255, 0, 199), (156, 0, 200), (255, 255, 0), (255, 145, 77)]
##############################################

color_list = []
for color in draw_color_list:
    color_list.append((color[2], color[1], color[0]))

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

detector = ht.HandDetector(max_hands=1, detection_confidence=0.85)

img_canvas = np.zeros((720, 1280, 3), np.uint8)

while True:

    # import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # find hand landmark

    img = detector.find_hands(img)
    landmark_list, bounding_box = detector.find_position(img, draw_bounding_box=False, draw=False)

    if len(landmark_list) != 0:
        x1, y1 = landmark_list[8][1:]
        x2, y2 = landmark_list[12][1:]

        # check which finger is up
        fingers = detector.fingers_up()

        # if selection mode - two fingers are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0

            cv2.rectangle(img, (x1, y1-15), (x2, y2+15), (255, 0, 255), cv2.FILLED)

            if y1 < 125 and x1 < 880:
                if 225 < x1 < 300:
                    navbar = navbar_list[1]
                    brush_thickness = 7
                    erase = False
                elif 350 < x1 < 450:
                    navbar = navbar_list[2]
                    brush_thickness = 3
                    erase = False
                elif 500 < x1 < 650:
                    navbar = navbar_list[3]
                    erase = True
                    brush_thickness = 35
                elif 700 < x1 < 950:
                    navbar = navbar_list[4]
                    erase = False
                    brush_thickness = 5

            elif x1 > 880 and y1 < 63:
                if 978 < x1 < 1028:
                    color_bar = color_bar_list[0]
                    draw_color = color_list[0]
                elif 1038 < x1 < 1088:
                    color_bar = color_bar_list[2]
                    draw_color = color_list[2]
                elif 1098 < x1 < 1148:
                    color_bar = color_bar_list[4]
                    draw_color = color_list[4]
                elif 1158 < x1 < 1208:
                    color_bar = color_bar_list[6]
                    draw_color = color_list[6]
                elif 1218 < x1 < 1268:
                    color_bar = color_bar_list[8]
                    draw_color = color_list[8]

            elif x1 > 880 and 63 < y1 < 126:
                if 978 < x1 < 1028:
                    color_bar = color_bar_list[1]
                    draw_color = color_list[1]
                elif 1038 < x1 < 1088:
                    color_bar = color_bar_list[3]
                    draw_color = color_list[3]
                elif 1098 < x1 < 1148:
                    color_bar = color_bar_list[5]
                    draw_color = color_list[5]
                elif 1158 < x1 < 1208:
                    color_bar = color_bar_list[7]
                    draw_color = color_list[7]
                elif 1218 < x1 < 1268:
                    color_bar = color_bar_list[9]
                    draw_color = color_list[9]

            if x1 < 60 and 225 < y1 < 425:
                img_canvas = np.zeros((720, 1280, 3), np.uint8)

        # if drawing mode if index finger is up
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, draw_color, cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if erase:
                cv2.line(img, (xp, yp), (x1, y1), (0, 0, 0), brush_thickness)
                cv2.line(img_canvas, (xp, yp), (x1, y1), (0, 0, 0), brush_thickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), draw_color, brush_thickness)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, brush_thickness)

            xp, yp = x1, y1

    img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, img_inv)
    img = cv2.bitwise_or(img, img_canvas)

    # Setting the navbar image

    img[0:126, 0:880] = navbar
    img[0:126, 880:1280] = color_bar
    img[250:450, 0:60] = clear

    # Display
    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", img_canvas)
    cv2.waitKey(1)
