from flask import Flask, render_template, request

import csv, os, sys, math
from datetime import datetime, timezone, timedelta

from runCommand import run_command

app = Flask(__name__, root_path="flask", static_folder="static")

dirName = "hw1"

def getStudents():
   with open(dirName+".csv", encoding='utf-8-sig') as csvfile:
      lines = list(csv.reader(csvfile))
      dirs = os.listdir(dirName)
      return lines, dirs

@app.route("/")
def index():
  
  lines, dirs = getStudents()
  return render_template("main.html", students=lines, dirs=dirs)

@app.route("/student/<name>")
def getStudent(name):
  student_lines, dirs = getStudents()
  # for file in glob.glob("*"):
  #     print(file)
  folderDir = f"./{dirName}/{name}"
  filesList = []

  tc_filename = set()
  for root, dirs, files in os.walk(f"./{dirName}_testcase"):
     for file in files:
      tc_filename.add(file)
        
  # Get parameter
  parameter_dict = request.args.to_dict()
  filecontent = ""; selfile=""; tc_output_st = ""; timestamp="0"; due_timestamp = "0"
  if len(parameter_dict) > 0:
     if "timestamp" in parameter_dict.keys(): timestamp = parameter_dict['timestamp']

     filecontent = 'printf("Hello World!");'
     selfile = parameter_dict['file'].replace("\ ", " ")
     filedir = f"{folderDir}/{selfile}"
     try:
      with open(filedir) as file:
          lines = file.readlines()
          filecontent = "".join(lines)
     except:
        with open(filedir, encoding="euckr") as file:
          lines = file.readlines()
          filecontent = "".join(lines)

     # Run Code
     if "tc" in parameter_dict.keys():
        tc = parameter_dict["tc"]
        filedir_nsp = filedir.replace(' ', '\ ')
        runcmd = f"gcc -o a {filedir_nsp} && tail --lines +2 ./{dirName}_testcase/{tc} | ./a && rm ./a"
        tc_output = run_command(runcmd)
        tc_output_st = "\n".join(tc_output[0])

        with open(f"./{dirName}_testcase/{tc}") as file:
          lines = file.readlines()
          due_timestamp = lines[0].split(" ")[1].strip()
          print(due_timestamp)
          due_timestamp = datetime.strptime(due_timestamp, "%Y/%m/%d").timestamp() #+ 86400

  for root, dirs, files in os.walk(folderDir):
    for file in files:
        if file.endswith(".c"):
             rootc = root.replace(" ", "\ ")
             filec = file.replace(" ", "\ ")
             filename = os.path.join(rootc, filec)
            #  print(filename, file)
             filesList.append({
                "filename": filename.replace(folderDir + "/", ""),
                "git_timestamp":  "".join(run_command(f"git -C {rootc} log -1 --pretty='format:%ct' '{filec}'")[0]),
                "git_time":  "".join(run_command(f"git -C {rootc} log -1 --pretty='format:%ci' '{filec}'")[0]),
                "git_message":  "".join(run_command(f"git -C {rootc} log -1 --pretty='format:%s' '{filec}'")[0])
             })
  filesList.sort(key=lambda x: (x["git_timestamp"], x["filename"]), reverse=True)
  print(timestamp, due_timestamp)

  # Next student
  nextidx = 0
  try:
    nextidx = list(map(lambda x: x[0], student_lines)).index(str(name.split("_")[0]))
    pass
  except:
     pass
  next_student = student_lines[(nextidx + 1) % len(student_lines)]
  next_student = f"{next_student[0]}_{next_student[1]}"
  return render_template("student.html", name=name, filesList=filesList, filecontent=filecontent, tc_filename=tc_filename, selfile=selfile, tc_output_st=tc_output_st, timestamp=datetime.fromtimestamp(int(float(timestamp)), timezone(timedelta(hours=9))), due_timestamp=datetime.fromtimestamp(int(float(due_timestamp)), timezone(timedelta(hours=9))), late_days = math.ceil((int(float(timestamp)) - int(float(due_timestamp))) / 86400), next_student=next_student)

# app.run(host="0.0.0.0", port="4000")
if __name__ == "__main__":
  app.run(port="4000", debug=True)