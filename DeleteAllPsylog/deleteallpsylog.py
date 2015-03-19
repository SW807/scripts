import os
import sys
import subprocess

def main():
    root_directory = "C:\Users\Stefan Micheelsen\Google Drev\Dokumenter\Uni\8. Semester\SW8\code"
    app_directories = ["PsyLog",
                       "module-accelerometer",
                       "module-gyroscope",
                       "module-light",
                       "module-location",
                       "module-proximity",
                       "module-screen",
                       "module-sound",
                       "module-testanalyse"]
apps = subprocess.Popen("adb shell pm list packages | grep dk.aau.cs.psylog", stdout = subprocess.PIPE).communicate()[0].split("\n")
apps = [x.strip().replace("package:","") for x in apps]
apps = [x for x in apps if len(x) > 0]

print apps
for app in apps:
	subprocess.Popen("adb shell pm uninstall -k " + app).wait()
    
if __name__ == '__main__':
    main()