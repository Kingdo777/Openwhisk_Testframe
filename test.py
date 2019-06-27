import json
import os
import subprocess


def run_cmd(cmd):
    return os.popen(cmd).read().strip("\n")


run_cmd("cp ./iperf3 /tmp/iperf3")
run_cmd("chmod +x /tmp/iperf3")
run_cmd("/tmp/iperf3 -s")
sp = subprocess.Popen(["/tmp/iperf3",
                       "-c",
                       "127.0.0.1",
                       "-p",
                       str(5201),
                       "-l",
                       "-t",
                       "1",
                       "-Z",
                       "-J"],
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE)
out, err = sp.communicate()
_d = json.loads(out)["end"]
sender = _d["streams"][0]["sender"]
bps = str(sender["bits_per_second"])
