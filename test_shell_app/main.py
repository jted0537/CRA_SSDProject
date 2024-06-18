import os

with open("../result.txt") as file_data:
    print(file_data.readline(), end="")

os.popen(f"ssd R 3").read().encode("UTF-8")
# p = subprocess.Popen("ssd R 3", stdout=subprocess.PIPE)
# result = p.communicate()
# text = result[0].decode("utf-8")
