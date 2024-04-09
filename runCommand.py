from subprocess import Popen, PIPE, STDOUT, run

def run_command(cmd, timeout=2):
  process = run(cmd, capture_output=True, text=True, check=False, encoding='utf-8', shell=True, timeout=timeout)

  # change to json
  terminal_markers = '\x1b'
  lines = [
    line.strip(terminal_markers)
    for line in (process.stdout + "\n" + process.stderr).split("\n")
    if line.strip()
    ]

  return lines, process.returncode