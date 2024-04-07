import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ["GIT_SSH_COMMAND"] = f"ssh -i {dir_path}/key/han220 -o IdentitiesOnly=yes"

import csv
import multiprocessing

from runCommand import run_command


def gitGetItem(line):
  sid = line[0]
  name = line[1]
  giturl = line[2]

  giturl = giturl[:-4] if giturl[-4:] == ".git" else giturl 
  giturl_sp = giturl.split("/")[-2:]
  if len(giturl_sp) <= 1:
    return
  pmy, pcode = run_command(f"git clone --depth 1 git@github.com:{giturl_sp[0]}/{giturl_sp[1]}.git {dirName}/{sid}_{name}")
  msg = pmy[0]
  if "Cloning into" in msg and pcode == 0:
    print("\033[92m[cloned]", sid, name, pcode, "\033[0m")
  elif "already exists and is" in msg:
    pmy1, pcode1 = run_command(f"git -C {dirName}/{sid}_{name} pull")
    print("[exist]", sid, name, pcode, pmy1[-2:])
  else:
    print("\033[91m[error]", sid, name, pcode, pmy[-2:], "\033[0m")

# Main Code

dirName = "hw1"
with open(dirName+".csv", encoding='utf-8-sig') as csvfile:
  lines = csv.reader(csvfile)
  i = 0

  pool = multiprocessing.Pool(processes=4)
  pool.map(gitGetItem, lines)
  pool.close()
  pool.join()
  # for line in lines:
  #   i += 1
  #   gitGetItem(line)

print("Finished!")

