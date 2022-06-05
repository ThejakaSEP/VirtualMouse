# https://github.com/autopilot-rs/autopy/issues/72

import cv2
import numpy as np
import HandTrackingModule as htm
import time
# import autopy
import pyautogui


wCam, hCam = 640 , 480
cTime = 0
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()
frameR = 100 #Frame Reduction

#To smoothen the values
smooth = 5
pLocX,pLoxY = 0,0
clocX,clocY = 0,0

while True:
    # 1. Find the hand Landmarks
    success,img = cap.read()
    img = detector.findHands(img)
    lmList,bbox = detector.findPosition(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList)!=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
        # print(x1,y1,x2,y2)

    # 3. Check which fingers are up
    fingers = detector.fingersUp()
    # print(fingers)

    # 4. Only Index finger -> Moving Mode

    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 255, 0), 2)

    if fingers[1] == 1 and fingers[2] ==0:

        # 5. Convert Coordinates to ratio of Screen

        x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
        y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

        # 6. Smoothen Values
        clocX = pLocX+(x3-pLocX)/smooth
        clocY = pLoxY+(y3-pLoxY)/smooth

        # 7. Move mouse
        pyautogui.moveTo(wScr-clocX,clocY)
        cv2.circle(img,(x1,y1),15,(255,0,255),thickness=-1)
        pLocX,pLoxY = clocX,clocY
    # 8. Both Index and Middle fingers -> Clicking Mode
    if fingers[1] == 1 and fingers[2] == 1:
        length,img,lineInfo = detector.findDistance(8,12,img)
        if length < 40:
            # cv2.circle(img, (lineInfo[4], lineInfo[5]),
            #            15, (255, 0, 0), thickness=-1)
            pyautogui.click()


    if fingers[1] == 1 and fingers[2] == 1 and fingers[3]==1:
        length1,img,lineInfo = detector.findDistance(8,16,img)
        if length1 < 60:
            # print("Hello")
            # cv2.circle(img, (lineInfo[4], lineInfo[5]),
            #            15, (0, 0, 255), thickness=-1)
            # pyautogui.click()
            pyautogui.click(button='right')
            # pyautogui.click(button = 'left', clicks = 2, interval=0.5)
            # pyautogui.doubleClick()


    # 11. Frame Rate
    cTime = time.time()
    fps = 1/ (cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    # 12. Display
    cv2.imshow("Image",img)
    cv2.waitKey(1)