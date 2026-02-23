import cv2
import dlib
import numpy as np
import time
from collections import deque

class EyeTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(r"D:\webots project tests\controllers\videocaptest\shape_predictor_68_face_landmarks.dat")
        self.eye_movements_x = deque(maxlen=30)
        self.eye_movements_y = deque(maxlen=30)
        self.blink_threshold = None  
        
        print(" لطفاً برای ۳ ثانیه مستقیم به جلو نگاه کنید تا مقدار پایه تنظیم شود...")
        time.sleep(3)
        self._calibrate()
    
    def _calibrate(self):
        blink_distances = []
        for _ in range(30):
            ret, frame = self.cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray)
            for face in faces:
                landmarks = self.predictor(gray, face)
                left_eye, right_eye = self._get_eye_regions(frame, landmarks)
                x_ratio, y_ratio = self._get_pupil_position(left_eye, right_eye)
                self.eye_movements_x.append(x_ratio)
                self.eye_movements_y.append(y_ratio)
                
                blink_distances.append(self._get_blink_distance(landmarks))
        
        self.base_x = np.mean(self.eye_movements_x)
        self.base_y = np.mean(self.eye_movements_y)
        self.threshold_x = max(0.05, np.std(self.eye_movements_x) * 2.0)
        self.threshold_y = max(0.05, np.std(self.eye_movements_y) * 2.0)
        self.blink_threshold = np.mean(blink_distances) * 0.8  # مقدار آستانه برای تشخیص پلک زدن
    
    def _get_eye_regions(self, frame, landmarks):
        left_eye = frame[landmarks.part(37).y:landmarks.part(40).y, landmarks.part(36).x:landmarks.part(39).x]
        right_eye = frame[landmarks.part(43).y:landmarks.part(46).y, landmarks.part(42).x:landmarks.part(45).x]
        return left_eye, right_eye

    def _get_pupil_position(self, left_eye, right_eye):
        def process_eye(eye):
            gray_eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_eye, 30, 255, cv2.THRESH_BINARY_INV)
            moments = cv2.moments(thresh)
            if moments["m00"] != 0:
                cx = int(moments["m10"] / moments["m00"]) / eye.shape[1]
                cy = int(moments["m01"] / moments["m00"]) / eye.shape[0]
            else:
                cx, cy = 0.5, 0.5
            return cx, cy
        
        left_x, left_y = process_eye(left_eye)
        right_x, right_y = process_eye(right_eye)
        return (left_x + right_x) / 2, (left_y + right_y) / 2

    def _get_blink_distance(self, landmarks):
        left_eye_height = landmarks.part(41).y - landmarks.part(37).y
        right_eye_height = landmarks.part(47).y - landmarks.part(43).y
        return (left_eye_height + right_eye_height) / 2
    
    def detect_direction(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, frame
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        for face in faces:
            landmarks = self.predictor(gray, face)
            left_eye, right_eye = self._get_eye_regions(frame, landmarks)
            x_ratio, y_ratio = self._get_pupil_position(left_eye, right_eye)
            blink_distance = self._get_blink_distance(landmarks)
            
            direction = "Looking Center"
            if x_ratio > self.base_x + self.threshold_x:
                direction = "Looking Left"
            elif x_ratio < self.base_x - self.threshold_x:
                direction = "Looking Right"
            
            if blink_distance < self.blink_threshold:
                direction = "Looking Down"
            elif y_ratio < self.base_y - self.threshold_y:
                direction = "Looking Up"
            
            cv2.putText(frame, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return direction, frame
    
    def run(self):
        while True:
            direction, frame = self.detect_direction()
            cv2.imshow("Eye Tracking", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # کلید ESC برای خروج
                break
        self.release()
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = EyeTracker()
    tracker.run()
