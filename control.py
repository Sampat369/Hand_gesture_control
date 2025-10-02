import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Finger indices and their corresponding landmarks
FINGERS = {
    "Thumb": (mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_IP, mp_hands.HandLandmark.THUMB_CMC),
    "Index": (mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP, mp_hands.HandLandmark.INDEX_FINGER_MCP),
    "Middle": (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP, mp_hands.HandLandmark.MIDDLE_FINGER_MCP),
    "Ring": (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP, mp_hands.HandLandmark.RING_FINGER_MCP),
    "Pinky": (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP, mp_hands.HandLandmark.PINKY_MCP)
}
cap = cv2.VideoCapture(0)
finger_states = [] 
mid_pos=[[],[]] 
xp=yp=0
status=""
turn=[1,1,1,1,1]
while cap.isOpened():
    
    ret, frame = cap.read()
    if not ret:
        break
    frame=cv2.resize(frame,(1000,700))
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Determine finger states
            finger_states = []
            mid_pos=[[],[]]
            status=""
            for finger, (tip,pip, mcp) in FINGERS.items():
                if finger =="Thumb":
                    #Thumb in x-axis
                    tip_x=hand_landmarks.landmark[tip].x
                    ip_x=hand_landmarks.landmark[pip].x
                    cmc_x=hand_landmarks.landmark[mcp].x
                    state=1 if tip_x<ip_x  else 0
                elif finger=="Middle":
                    tip_y = hand_landmarks.landmark[tip].y
                    pip_y = hand_landmarks.landmark[pip].y
                    mcp_y = hand_landmarks.landmark[mcp].y
                    tip_x=hand_landmarks.landmark[tip].x
                    pip_x=hand_landmarks.landmark[pip].x
                    mcp_x=hand_landmarks.landmark[mcp].x
                   
                    mid_pos[0].append(tip_x*1000)
                    mid_pos[0].append(pip_x*1000)
                    mid_pos[0].append(mcp_x*1000)
                    mid_pos[1].append(tip_y*700)
                    mid_pos[1].append(pip_y*700)
                    mid_pos[1].append(mcp_y*700)
                    state = 1 if tip_y < pip_y and tip_y<mcp_y  else 0
                    xp=mid_pos[0][0]-mid_pos[0][1]
                    yp=mid_pos[1][0]-mid_pos[1][1]
                else:    
                    tip_y = hand_landmarks.landmark[tip].y
                    pip_y = hand_landmarks.landmark[pip].y
                    mcp_y = hand_landmarks.landmark[mcp].y
                    if finger=="Index":
                       
                        tip_x=hand_landmarks.landmark[tip].x
                        posx=tip_x*1000-500
                        posy=tip_y*700
                    state = 1 if tip_y < pip_y and tip_y<mcp_y  else 0
                finger_states.append(state)

                #data annalysis for gesture
                if 65>xp>-65 and 56>yp>-75 and finger_states!=[0,0,0,0,0] :
                    turn=[1,1,1,1,1]
                    status="no action"
                elif xp>56 and 20>yp>-60 and turn[2]==1:
                      pyautogui.press('right')
                      status="right"
                      turn=[1,1,0,1,1]
                elif finger_states==[0,1,1,1,0]and turn[4]==1:                         
                    pyautogui.press('space')  
                    status="space"
                    turn=[1,1,1,1,0]
                elif -65<xp<70 and  yp<-65 and turn[0]==1:
                   pyautogui.press('up')
                   status="up"
                   turn=[0,1,1,1,1]
                elif yp>65 and -65<xp<30 and turn[1]==1:
                    pyautogui.press('down')
                    status="down"
                    turn=[1,0,1,1,1]
                elif xp<-75 and 30>yp>-45 and turn[3]==1:
                    pyautogui.press('left')
                    status="left"
                    turn=[1,1,1,0,1]
                
                
            
            
    cv2.imshow('Finger State Detection', frame) 
    
    #finger gesture actions

    print(xp,"oo",yp,"oo",status)
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()
# python control.py            