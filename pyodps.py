# milisecond转化为age
def milisecond2age(t, ds):
    if t is None:
        return None
    dt = datetime.strptime(ds, '%Y%m%d')
    dt0 = datetime.fromtimestamp(int(t) / 1000)
    age = (dt - dt0).days + 1
    if age <= 0:
        return None
    else:
        return age
      
 
# milisecond转化为datatime
def milisecond2ds(t, format='%Y%m%d'):
    if t is None:
        return None
    dt = datetime.fromtimestamp(int(t) / 1000)
    return dt.strftime(format)

      
