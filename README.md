# eye-tracking-webots-robot
Webots robot simulation controlled by eye tracking (left, right, up, down), keyboard and sensors.

<img width="1127" height="600" alt="Screenshot (46)" src="https://github.com/user-attachments/assets/cb847d93-8903-4c12-9907-d002fcd0da6f" />

## Featuers 
1- Real-time **eye tracking**
2- Dual control **keyboard + eye-based movment**
3- **distance sensors**, **temperture**(based on area), **light detection**(Implemented in version R2021a with different assumptions)
4- **Camera recording** It is saved in the "videocaptest" folder with avi format.
5- Modular structure

## Requirements
- Python 3.9
- Webots R2021a
- shape_predictor_68_face_landmarks.dat (which you can find in "videocaptest" folder)
- opencv
- numpy
- dlib

<img width="1107" height="750" alt="Screenshot (45)" src="https://github.com/user-attachments/assets/8a6d66b4-2076-4929-99dc-2bf8f1f3a8c2" />
<img width="1920" height="903" alt="Screenshot (48)" src="https://github.com/user-attachments/assets/65bf1c56-3c8a-4e44-9a13-5c2fc9d5211a" />

## How to Use
- open "myworld.wbt" (or your custom design).
- From file menu, click **Import 3D Models** and open "Robot7.wrl".
- Run the simulation.

## Keyboard Control
you can control the robot using:
- W (Forward)
- S (Backward)
- A (Left)
- D (Right)

## Eye Tracking Mode
Press **E** to activate eye tracking mode and wait a few seconds.

For best performance:
- Position your device so the camera can clearly see your eyes.
- Make sure the camera is at eye level.
- Sit in a well-lit place.
- Avoid strong light reflections on your eyes.

## Acknowledments
- The base eye-tracking implementation (left/right detection) was adapted from:
Gaze Tracking by antoinelame
https://github.com/antoinelame/GazeTracking

I expanded the implementation to support up/down detection and integrated it into the robot controller.

- The robot body design was inspired by:
Digital-Twin-Webots-Tutorial-Video by ennuikat
https://github.com/ennuikat/Digital-Twin-Webots-Tutorial-Video

The model was modified and customized to fit this simulation.

## Author
Melika shahbazi zade
Electrical Engineer | Control Systems
contact: melikashahbazizade@gmail.com
