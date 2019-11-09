import cv2
import numpy as np
import math
import time

'''
This program is for comparing color, especially RGB, HSV, and YCbCr.
It will read example cube photo, and select some pixels' color.
Finally, Comparing these colors to sort specific type of color.
'''
cameras = []
screens = []

w, h = 320, 240

RENDER_BASE_X = -1920
RENDER_BASE_Y = 0
RENDER_TITLEBAR_HEIGHT = 33

AVERAGE_COLOR_OFFSET = 3
COLOR_DISTANCE_OFFSET = 100

CUBE = [
    {
        'face': 'B',
        'pixel': [
            [116, 32], [155, 39], [186, 44],
            [126, 53], [166, 59], [201, 64],
            [139, 82], [180, 85], [218, 89]
        ],
        'center': None,
        'faceString': [str(i) for i in range(0, 9)],
        'color': [None] * 9
    },
    {
        'face': 'R',
        'pixel': [
            [73, 109], [81, 81], [91, 47],
            [79, 130], [88, 102], [98, 69],
            [88, 162], [97, 133], [110, 99],
        ],
        'center': None,
        'faceString': [str(i) for i in range(0, 9)],
        'color': [None] * 9
    },
    {
        'face': 'D',
        'pixel': [
            [186, 179], [153, 179], [112, 180],
            [200, 153], [165, 151], [123, 150],
            [218, 121], [180, 118], [137, 113],
        ],
        'center': None,
        'faceString': [str(i) for i in range(0, 9)],
        'color': [None] * 9
    },
    {
        'face': 'U',
        'pixel': [
            [115, 34], [153, 41], [184, 48],
            [128, 56], [167, 61], [200, 67],
            [142, 80], [182, 85], [219, 90]
        ],
        'center': None,
        'faceString': [str(i) for i in range(0, 9)],
        'color': [None] * 9
    },
    {
        'face': 'L',
        'pixel': [
            [89, 47], [99, 70], [111, 99],
            [77, 85], [87, 108], [97, 135],
            [67, 115], [75, 139], [85, 169]
        ],
        'center': None,
        'faceString': [str(i) for i in range(0, 9)],
        'color': [None] * 9
    },
    {
        'face': 'F',
        'pixel': [
            [142, 116], [183, 119], [219, 122],
            [126, 153], [167, 154], [202, 155],
            [112, 186], [153, 184], [188, 183]
        ],
        'center': None,
        'faceString': [str(i) for i in range(0, 9)],
        'color': [None] * 9
    }
]

# Render camera screen to window
def renderWindow(title, screen, x, y):
    cv2.imshow(title, screen)
    cv2.moveWindow(title, x, y)

# Draw green circle on selected points
def drawPos(cubeObj, screen):
    for obj in cubeObj:
        for i, pixel in enumerate(obj['pixel']):
            x = pixel[0]; y = pixel[1]
            cv2.circle(screen, (x, y), 2, (0, 255, 0), -1)
            cv2.putText(screen, '{}{}'.format(obj['face'], i), #[{}, {}]'.format(obj['face'], i, x, y),
                (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 0))

# Calculate average color in range of -offset/2 ~ offset/2
def calAvgColor(a, b, c, x, y, offset):
    fromX = math.ceil(x - offset / 2); toX = math.ceil(x + offset / 2)
    fromY = math.ceil(y - offset / 2); toY = math.ceil(y + offset / 2)

    if fromX < 0: fromX = 0
    if toX >= w: toX = w - 1
    if fromY < 0: fromY = 0
    if toY >= h: toY = h - 1

    avgA = 0; avgB = 0; avgC = 0
    for aY in range(fromY, toY):
        for aX in range(fromX, toX):
            avgA += a[y, x]
            avgB += b[y, x]
            avgC += c[y, x]

    powOffset = offset * offset
    avgA = math.floor(avgA / powOffset)
    avgB = math.floor(avgB / powOffset)
    avgC = math.floor(avgC / powOffset)

    return avgA, avgB, avgC

# Save average color, and set center color
def saveColor(cubeObj, a, b, c):
    for obj in cubeObj:
        for i, pixel in enumerate(obj['pixel']):
            x = pixel[0]; y = pixel[1]
            avgA, avgB, avgC = calAvgColor(a, b, c, x, y, AVERAGE_COLOR_OFFSET)
            obj['color'][i] = (avgA, avgB, avgC)
            if i == 4: obj['center'] = (avgA, avgB, avgC)

def calDist(fromX, fromY, fromZ, toX, toY, toZ):
    return math.sqrt(
        abs(fromX * fromX - toX * toX)
        + abs(fromY * fromY - toY * toY)
        + abs(fromZ * fromZ - toZ * toZ))

def sortColor():
    for fromObj in CUBE:
        for toObj in CUBE:
            i = 0; fromX, fromY, fromZ = fromObj['center']
            for toX, toY, toZ in toObj['color']:
                distance = calDist(0, fromY, fromZ, 0, toY, toZ)
                #print(i, distance)
                if distance < COLOR_DISTANCE_OFFSET:
                    toObj['faceString'][i] = fromObj['face']

                i += 1

def clearCube():
    for obj in CUBE:
        obj['faceString'] = [str(i) for i in range(0, 9)]

for i in range(0, 2):
    cameras.append(cv2.VideoCapture(i))

for cam in cameras:
    cam.set(3, w)  # cv2.CAP_PROP_FRAME_HEIGHT
    cam.set(4, h)  # cv2.CAP_PROP_FRAME_WIDTH

while True:
    #clearCube()

    for i, cam in enumerate(cameras):
        ret, frame = cam.read()

        YCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
        y, cr, cb = cv2.split(YCrCb)
        ny = cv2.normalize(y, None, 0, 255, cv2.NORM_MINMAX)
        ncr = cv2.normalize(cr, None, 0, 255, cv2.NORM_MINMAX)
        ncb = cv2.normalize(cb, None, 0, 255, cv2.NORM_MINMAX)

        HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        H, S, V = cv2.split(HSV)
        nH = cv2.normalize(H, None, 0, 255, cv2.NORM_MINMAX)
        nS = cv2.normalize(S, None, 0, 255, cv2.NORM_MINMAX)
        nV = cv2.normalize(V, None, 0, 255, cv2.NORM_MINMAX)

        cubeObj = []
        if i == 0:
            cubeObj.append(CUBE[0])
            cubeObj.append(CUBE[1])
            cubeObj.append(CUBE[2])
        else:
            cubeObj.append(CUBE[3])
            cubeObj.append(CUBE[4])
            cubeObj.append(CUBE[5])

        drawPos(cubeObj, frame)
        saveColor(cubeObj, nH, nS, nV)

        screens = [
            [
                'Camera{} - Y'.format(i),
                y,
                RENDER_BASE_X + 0 * w,
                RENDER_BASE_Y + 2 * i * (h + RENDER_TITLEBAR_HEIGHT)
            ],
            [
                'Camera{} - nY'.format(i), 
                ny, 
                RENDER_BASE_X + 0 * w, 
                RENDER_BASE_Y + (2 * i + 1) * (h + RENDER_TITLEBAR_HEIGHT)
            ],
            [
                'Camera{} - Cr'.format(i), 
                cr, 
                RENDER_BASE_X + 1 * w, 
                RENDER_BASE_Y + 2 * i * (h + RENDER_TITLEBAR_HEIGHT)
            ],
            [
                'Camera{} - nCr'.format(i), 
                ncr, 
                RENDER_BASE_X + 1 * w, 
                RENDER_BASE_Y + (2 * i + 1) * (h + RENDER_TITLEBAR_HEIGHT)
            ],
            [
                'Camera{} - Cb'.format(i), 
                cb, 
                RENDER_BASE_X + 2 * w, 
                RENDER_BASE_Y + 2 * i * (h + RENDER_TITLEBAR_HEIGHT)
            ],
            [
                'Camera{} - nCb'.format(i), 
                ncb, 
                RENDER_BASE_X + 2 * w, 
                RENDER_BASE_Y + (2 * i + 1) * (h + RENDER_TITLEBAR_HEIGHT)
            ],
            [
                'Camera{} - Pixel'.format(i), 
                frame, 
                RENDER_BASE_X + 3 * w, 
                RENDER_BASE_Y + 2 * i * (h + RENDER_TITLEBAR_HEIGHT)
            ],
        ]

        for screen in screens:
            renderWindow(screen[0], screen[1], screen[2], screen[3])

        #cv.imwrite('test{}-gray.png'.format(i), gray)
        #cv.imwrite('test{}-ycrcb.png'.format(i), YCrCb)

        # 참고: 0x1B (ESC)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.release()
    
    sortColor()

    for obj in CUBE:
        print(obj['face'] + '-' + ''.join(obj['faceString']))

    time.sleep(1)


cv2.destroyAllWindows()
