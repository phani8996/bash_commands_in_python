import sys
from time import time

filename=sys.argv[1]
lines = int(sys.argv[2])

LINE_SIZE=200
temp=lines
data=''


def get_byte_range_file(fl, num_bytes):
    position = fl.tell()
    if position < num_bytes:
        num_bytes = position
    if position == 0:
        return None
    fl.seek(-num_bytes, 1)
    dt = fl.read(num_bytes)
    fl.seek(-num_bytes, 1)
    return dt

start_time1=time()
with open(filename) as fl:
    fl.seek(0,2)
    while True:
        num_bytes = temp*LINE_SIZE
        dt = get_byte_range_file(fl, num_bytes)
	if dt is not None:
            data = dt + data
        else:
            print('Reached starting of the file.Exiting')
            break
        if(data.count('\n') > lines):
	     data = data.split('\n')
             data = '\n'.join(line for line in data[-lines-1:])
             break
        else:
           temp = lines - data.count('\n') + 1

end_time1=time()
start_time2=time()
print data[:-1]
end_time2=time()
print end_time1-start_time1, end_time2-start_time2

