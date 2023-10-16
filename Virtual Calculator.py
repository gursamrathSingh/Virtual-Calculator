import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from time import sleep


class Button:
    def __init__(self, pos, w, h, val):
        self.pos = pos
        self.w = w
        self.h = h
        self.val = val

    def draw(self, frame):
        cv.rectangle(frame, self.pos, (self.pos[0] + self.w, self.pos[1]+self.h), (201, 220, 233), cv.FILLED)
        cv.rectangle(frame, self.pos, (self.pos[0] + self.w, self.pos[1]+self.h), (50, 50, 50), 2)
        cv.putText(frame, self.val, (self.pos[0] + 20, self.pos[1] + 60), cv.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 1)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.w and self.pos[1] < y < self.pos[1] + self.h :
            cv.rectangle(frame, self.pos, (self.pos[0] + self.w, self.pos[1] + self.h), (225 , 225, 225), cv.FILLED)
            cv.rectangle(frame, self.pos, (self.pos[0] + self.w, self.pos[1] + self.h), (50, 50, 50), 3)
            cv.putText(frame, self.val, (self.pos[0] + 20, self.pos[1] + 60), cv.FONT_HERSHEY_SIMPLEX, 2, (50, 50, 50), 2)
            return self.val
        return " "


# WebCam
capture = cv.VideoCapture(0)
detector = HandDetector(detectionCon=0.7, maxHands=1)

# Buttons
button1 = Button((300,100), 80, 80, "1")
button2 = Button((380,100), 80, 80, "2")
button3 = Button((460,100), 80, 80, "3")
button4 = Button((300,180), 80, 80, "4")
button5 = Button((380,180), 80, 80, "5")
button6 = Button((460,180), 80, 80, "6")
button7 = Button((300,260), 80, 80, "7")
button8 = Button((380,260), 80, 80, "8")
button9 = Button((460,260), 80, 80, "9")
button0 = Button((300,340), 80, 80, "0")

buttonA = Button((540,100), 80, 80, "+")
buttonB = Button((540,180), 80, 80, "-")
buttonC = Button((540,260), 80, 80, "*")
buttonD = Button((540,340), 80, 80, "=")
buttonE = Button((380,340), 80, 80, "/")
buttonF = Button((460,340), 80, 80, ".")

buttonList = [button1, button2, button3, button4, button5, button6, button7, button8, button9, button0, buttonA, buttonB, buttonC, buttonD, buttonE, buttonF]

#var
myEqn = ""
while True:
    # Capture frame-by-frame
    _, frame = capture.read()
    frame = cv.flip(frame, flipCode=1)

    # hand detection
    hands, img = detector.findHands(frame, flipType=False)

    # drawing buttons to the frame
    cv.rectangle(frame, (300, 20), (620, 100), (201 ,220 ,233), cv.FILLED)
    cv.rectangle(frame, (300, 20), (620, 100), (50, 50, 50), 3)

    for button in buttonList:
        button.draw(frame)

    # Processing
    if hands:
        lm_list = hands[0]['lmList']
        length, _, frame = detector.findDistance(lm_list[8][0:2], lm_list[12][0:2], frame)

        x, y = lm_list[8][0:2]
        if length < 20:
            for button in buttonList:
                var = button.checkClick(x,y)
                if var != " ":
                    if len(myEqn) > 0 and myEqn[len(myEqn)-1] == "=":
                        myEqn = ""
                    if var == "=":
                        myEqn = str(eval(myEqn))
                    myEqn += var
                    sleep(0.4)  # important line!

    # Displaying the eqn/result
    cv.putText(frame, myEqn, (310, 80), cv.FONT_HERSHEY_SIMPLEX, 2, (50, 50, 50), 2)

    # Window Configuring
    cv.namedWindow("Virtual Calculator", cv.WINDOW_NORMAL)
    cv.resizeWindow("Virtual Calculator", 1280, 720)
    cv.imshow("Virtual Calculator", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()