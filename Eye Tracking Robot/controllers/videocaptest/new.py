from eye_tracker import EyeTracker
import cv2

def handle_movement(direction):
    if direction == "Looking Up":
        print("Move Forward ")
    elif direction == "Looking Down":
        print("Move Backward ")
    elif direction == "Looking Left":
        print("Turn Left ")
    elif direction == "Looking Right":
        print("Turn Right ")
    elif direction == "Looking Center":
        print("Stop ")

if __name__ == "__main__":
    tracker = EyeTracker()
    
    while True:
        direction, frame = tracker.detect_direction()
        if direction:
            handle_movement(direction)

        cv2.imshow("Eye Tracking", frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

    tracker.release()
