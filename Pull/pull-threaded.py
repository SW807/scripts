import os
import sys
import subprocess
from multiprocessing import Pool
FNULL = open(os.devnull, 'w')

update_submodules = False
errs = {}

def update_repository(x):
    repository_dir = x[0]
    clone_url = x[1]
    repository_exists = os.path.exists(repository_dir)
    if(repository_exists):
        os.chdir(repository_dir)
        result = subprocess.Popen("git pull".split(" "), stderr=subprocess.PIPE, stdout=FNULL).communicate()[1]
        if(result != None):
            errs[repository_dir] = result
        if(repository_dir not in ["module-lib", "log-lib"]):
            subprocess.Popen("git submodule update --init --recursive".split(" "), stderr=FNULL, stdout=FNULL).wait()
            if(update_submodules):
                subprocess.Popen("git submodule foreach --recursive git pull origin master".split(" "), stderr=FNULL, stdout=FNULL).wait() # Get tip of submodule and update references for that repository. vvv
                subprocess.Popen("git add app/src/main/java/dk/aau/cs/psylog/module_lib".split(" "), stderr=FNULL, stdout=FNULL).wait()
                subprocess.Popen(['git', 'commit', '-m', 'Update submodule reference'], stderr=FNULL, stdout=FNULL).wait()
                subprocess.Popen("git push".split(" "), stderr=FNULL, stdout=FNULL).wait()
        os.chdir("..")
    else:
        subprocess.Popen(("git clone --recursive " + clone_url).split(" "), stderr=FNULL, stdout=FNULL).wait()
    
def main():
    repos = ["https://github.com/SW807/module-sound.git",
             "https://github.com/SW807/module-screen.git",
             "https://github.com/SW807/module-proximity.git",
             "https://github.com/SW807/module-location.git",
             "https://github.com/SW807/module-light.git",
             "https://github.com/SW807/module-gyroscope.git",
             "https://github.com/SW807/module-accelerometer.git",
             "https://github.com/SW807/module-lib.git",
             "https://github.com/SW807/log-lib.git",
             "https://github.com/SW807/PsyLog.git",
             "https://github.com/SW807/module-testAnalyse.git",
             "https://github.com/SW807/scripts.git"]

    repos = [x.strip() for x in repos]
    repos = {os.path.splitext(os.path.basename(x))[0]: x for x in repos}

    pool = Pool(maxtasksperchild=1)
    pool.map(update_repository, list(repos.items()))

    print "Printing errors.."
    for key, value in errs.items():
        print "%s: %s" % (key, value)

if __name__ == '__main__':
    main()
