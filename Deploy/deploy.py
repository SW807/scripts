import os
import sys
import subprocess

def main():
    root_directory = "C:\Users\Mathias\Desktop\P8\Programmer"
    app_directories = ["PsyLog",
                       "module-accelerometer",
                       "module-gyroscope",
                       "module-light",
                       "module-location",
                       "module-proximity",
                       "module-screen",
                       "module-sound",
                       "module-testanalyse"]
    # To build:     gradlew.bat build el. gradlew.bat clean build -> outputter apk'er som kan installeres.
    # To install:   adb -d install apk-path
    original_dir = os.getcwd()
    for app in [os.path.join(root_directory, x) for x in app_directories]:
        print("Building application %s" % app)
        os.chdir(app)
        gradlew_path = os.path.join(app, "gradlew.bat")
        subprocess.Popen([gradlew_path, "assembleDebug"]).wait()
        
        apk_path = os.path.join(app, "app\\build\\outputs\\apk\\app-debug.apk")
        if(os.path.isfile(apk_path)):
            print("Installing application %s" % app)
            subprocess.Popen(["adb", "install", "-r", apk_path]).wait()
        os.chdir(original_dir)
        
        
    
                 
    
if __name__ == '__main__':
    main()