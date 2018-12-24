import sys
from time import time
import boto3
s3 = boto3.client('s3')

bucket=sys.argv[1]
filepath=sys.argv[2]
lines = int(sys.argv[3])

LINE_SIZE=200
temp=lines
data=''

def get_byte_range_s3(bucket, path, start, end):
    if start > end:
        start, end = end, start
    if start < 0:
       start = 0
    if end < 0:
       end = 0
    resp = s3.get_object(Bucket=bucket, Range='bytes={}-{}'.format(start, end), Key=path)
    content = resp['Body']
    return content.read().decode("utf-8") 

def get_file_size(bucket, path):
    try:
        resp = s3.head_object(Bucket=bucket, Key=path)
        return resp['ContentLength']
    except Exception as ex:
        print('Exception occured while getting file metadata', ex)
        return None

start_time1=time()
file_size = get_file_size(bucket, filepath)
end_time1=time()
start = file_size - temp*LINE_SIZE
end = file_size
start_time2=time()
loop=1
while True:
    #print('loop:', loop)
    loop += 1
    dt = get_byte_range_s3(bucket, filepath, start, end)
    if dt is not None:
        #print(type(data), type(dt), dt)
        #break
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
        end = start
        start = start - temp*LINE_SIZE
    if end < 0:
       break

end_time2=time()
start_time3=time()
print(data[:-1])
end_time3=time()
print(end_time1-start_time1, end_time2-start_time2, end_time3-start_time3)
