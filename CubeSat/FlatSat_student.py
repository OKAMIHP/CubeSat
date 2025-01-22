#AUTHOR: Your Name
#DATE: 01/01/2025

#import libraries
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2

#VARIABLES
THRESHOLD = 10          # Example threshold value; adjust to your needs
REPO_PATH = "/home/pi/FlatSatChallenge"  # Example path
FOLDER_PATH = "Images"  # Example folder name in your repo

#imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()

def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        print('added remote')
        origin.pull()
        print('pulled changes')
        repo.git.add(REPO_PATH + "/" + FOLDER_PATH)
        repo.index.commit('New Photo')
        print('made the commit')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')

def img_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = f'{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg'
    return imgname

def take_photo():
    """
    This function is completed to:
      - Continuously read acceleration data.
      - When it exceeds THRESHOLD, pause, take a photo, 
        then optionally push to GitHub.
    """
    while True:
        accelx, accely, accelz = accel_gyro.acceleration

        # Calculate total magnitude of acceleration
        magnitude = (accelx**2 + accely**2 + accelz**2)**0.5
        
        # Check if magnitude is above threshold
        if magnitude > THRESHOLD:
            # Pause briefly
            time.sleep(1)
            
            # Set image name (e.g. first name + last initial)
            name = "YourName"
            
            # Start camera, warm up, capture, stop
            picam2.start()
            time.sleep(2)
            filename = img_gen(name)
            picam2.capture_file(filename)
            picam2.stop()
            
            # Optionally push to GitHub
            git_push()
            
            # Pause again before continuing loop
            time.sleep(2)

        # Small pause to avoid constant polling
        time.sleep(0.2)

def main():
    take_photo()

if __name__ == '__main__':
    main()