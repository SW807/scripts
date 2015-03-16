import os
import zlib
import tarfile
import subprocess
import io
import datetime
import sys

def main():
    if(not os.path.isdir("databases")):
        os.mkdir("databases")
    # Check that device is connected.
    cmd_check_device = ["adb", "devices"]
    result = subprocess.Popen(cmd_check_device, stdout=subprocess.PIPE).communicate()[0].strip()
    if(len(result.split("\n")) == 1):
        sys.exit("Device is not connected, please connect it and try again.")
    # Check that package is installed
    cmd_check_package = ["adb", "shell", "pm", "path", "dk.aau.cs.psylog.psylog"]
    is_installed = subprocess.Popen(cmd_check_package, stdout=subprocess.PIPE).communicate()[0].strip()
    if(len(is_installed) < 2):
        sys.exit("Package is not installed, please install it and try again.")

    # Make backup and extract database file.
    cmd_backup = ["adb", "backup", "-f", os.path.join(os.getcwd(), "data.ab"), "-noapk", "dk.aau.cs.psylog.psylog"]
    subprocess.Popen(cmd_backup).wait()
    with open('data.ab', 'rb') as f:
        f.seek(24)  # skip 24 bytes
        data = f.read()  # read the rest
    tarstream = zlib.decompress(data)
    tf = tarfile.open(fileobj=io.BytesIO(tarstream))
    for entry in tf:
        if(entry.path == "apps/dk.aau.cs.psylog.psylog/db/database.db"):
            fileobj = tf.extractfile(entry)
            with open("databases/database-%s.db" % (datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')), "wb") as w:
                w.write(fileobj.read())
    os.remove('data.ab')  
    
    
if __name__ == '__main__':
    main()