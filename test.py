from subprocess import Popen, PIPE

process = Popen(["python", "discord_message.py"], stdout=PIPE)
(output, err) = process.communicate()
# print(output.decode("utf-8"))
exit_code = process.wait()
