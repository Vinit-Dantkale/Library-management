from datetime import datetime
t = datetime.strptime("2023-05-08 17:08:09.936106", '%Y-%m-%d %H:%M:%S.%f')-datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
print(t.days)


# 2023-05-08 17:08:09.936106