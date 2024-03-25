import cv2
import time
import mediapipe as mp
import serial 
import serial.tools.list_ports


class handDetector():
    def __init__(self, mode=False, maxHands=2,modelC=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelC, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        self.result = self.hands.process(imgRGB)
        # print(result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:
            for handLand in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLand, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        PosList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                PosList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)

        return PosList
    
    def getNumber(self,ar):
        s=""
        for i in ar:
            s+=str(ar[i])
        
        if(s=="00000"):
            return (0)
        elif(s=="01000"):
            return(1)
        elif(s=="01100"):
            return(2) 
        elif(s=="01110"):
            return(3)
        elif(s=="01111"):
            return(4)
        elif(s=="11111"):
            return(5) 

class DeviceManager():

    def list_the_port(self):
        serialList = list(serial.tools.list_ports.comports())
        portList = []
        print ()
        for n,port in enumerate(serialList):
            k = n + 1
            portList.append(port.device)
            print ("%d). %s"%(k,port.device))
        print ()
        return portList

    def select_port_from_list(self,ports):
        
        selectedValue = input()
        selectedPort = 0
        try:
            selectedPort = eval(selectedValue)
            if selectedPort > len(ports) or selectedPort <= 0:
                print ("Error in inputs. Give correct Value....")
                return 0
            return (ports[selectedPort - 1])
        except Exception as e:
            print ("Error in inputs. Enter Numbers only")
            return 0
        
    def connect_device(self,deviceToConnect):
        connectedDevice = serial.Serial(port=deviceToConnect, baudrate=9600, timeout=.1) 
        return connectedDevice

    def send_data(self,connectedDevice, dataToSend):
        connectedDevice.write(bytes(dataToSend, 'utf-8')) 

    def send_finger_data(self,device,data):
        s=""
        for i in data:
            s+=str(data[i])
        if s == None:
            s="00000"
        s = s + "\n"
        self.send_data(device,s)

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    comDevice = DeviceManager()
    fingers=[]

    listedPort = comDevice.list_the_port()
    print ("Select Port Number from the list:",)
    device = comDevice.select_port_from_list(listedPort)
    
    if(device != 0):
        connectedDevice = comDevice.connect_device(device)

        while connectedDevice.is_open:
            success, img = cap.read()
            img = detector.findHands(img,draw=True)
            lmList = detector.findPosition(img,draw=True)

            # if len(PosList) != 0:
            #     print(PosList[4])

            tipId=[4,8,12,16,20]
            if(len(lmList)!=0):
                fingers=[]
                #thumb
                if(lmList[tipId[0]][1]>lmList[tipId[0]-1][1]):
                        fingers.append(1)
                else :
                        fingers.append(0)
                #4 fingers
                for id in range(1,len(tipId)):
                    
                    if(lmList[tipId[id]][2]<lmList[tipId[id]-2][2]):
                        fingers.append(1)
                    
                    else :
                        fingers.append(0)

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime

            comDevice.send_finger_data(connectedDevice,fingers)
            flipimg = cv2.flip(img,1)
            cv2.putText(flipimg, str(detector.getNumber(fingers)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 0), 3)
            cv2.imshow("Webcam", flipimg)
            cv2.waitKey(1)


if __name__ == "__main__":
    main()