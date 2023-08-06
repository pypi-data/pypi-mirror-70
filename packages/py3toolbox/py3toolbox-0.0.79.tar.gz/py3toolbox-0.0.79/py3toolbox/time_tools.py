import time
import datetime
import math

def get_timestamp(ts_format='%Y-%m-%d %H:%M:%S', epoch_time = None, iso_format=False, timezone=0) :
  time_stuct = time.localtime()
  
  if epoch_time is not None : 
    digits = int(math.log10(epoch_time))+1
    if digits > 10 :  epoch_time = int(str(epoch_time)[:10])
    time_stuct = time.localtime(epoch_time)
    
  dt = datetime.datetime.fromtimestamp(time.mktime(time_stuct))
  if iso_format == False: 
    return time.strftime(ts_format,  time_stuct)
  else:
    return dt.isoformat()   

def timer_start():
  start = time.time()
  return (start)  
  
def timer_check(start):
  return(time.time() - start)   

  
def get_epoch(time_string):
  datetime_object = datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')
  timestamp = datetime_object.timestamp()
  return  int(timestamp)


def cal_days_diff(dt_str1, dt_str2, ts_fmt = '%Y-%m-%d %H:%M:%S'):
  dt1 = datetime.datetime.strptime(dt_str1, ts_fmt)
  dt2 = datetime.datetime.strptime(dt_str2, ts_fmt)
  diff   = dt2 - dt1
  return diff.days




if __name__ == "__main__":
  print (get_timestamp(ts_format='%Y-%m-%d %H:%M:%S', epoch_time=1579046194))
  print (get_epoch(get_timestamp()))
  print (time.time())
  
  pass