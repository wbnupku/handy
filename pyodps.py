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


def show_pts(tbl_name):
    """Print table partition names."""
    for pt in o.get_table(tbl_name).iterate_partitions():
        print(pt.name)

        
def get_max_ds_pt(tbl_name, ignore_substr='.done'):
    tbl = o.get_table(tbl_name)
    def get_ds(pt_name):
        items = pt_name.split(',')
        for t in items:
            if 'ds=' in t and ignore_substr not in t:
                return t.split('=')[1].strip('\'')
        return None
    dslist = [get_ds(pt.name) for pt in tbl.iterate_partitions()]

    dslist = [ds for ds in dslist if ds is not None and len(ds) == 8]
    print(dslist)
    max_ds = max(dslist)
    return max_ds
