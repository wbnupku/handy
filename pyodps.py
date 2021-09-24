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
    """
    Get max ds of odps table.
    Parameters:
        tbl_name: str
            name of odps table.
        ignore_substr: str, default: '.done'
            omit the partition if the name contains 'ignore_substr'
    Return:
        max_ds: str
            ds value of the partition with max ds. 
    """
    tbl = o.get_table(tbl_name)
    def get_ds(pt_name):
        items = pt_name.split(',')
        for t in items:
            if 'ds=' in t and ignore_substr not in t:
                return t.split('=')[1].strip('\'')
        return None
    dslist = [get_ds(pt.name) for pt in tbl.iterate_partitions()]

    dslist = [ds for ds in dslist if ds is not None and len(ds) == 8]
    max_ds = max(dslist)
    return max_ds

def ds_plus_n(ds, n):
    """获取ds + n days."""
    from datetime import timedelta
    dt = datetime.strptime(ds, '%Y%m%d') + timedelta(days=n)
    return dt.strftime('%Y%m%d')

def create_table_example():
    from odps.models import Schema, Column, Partition
    columns = [Column(name='num', type='bigint', comment='the column'),
               Column(name='num2', type='double', comment='the column2')]
    partitions = [Partition(name='pt', type='string', comment='the partition')]
    schema = Schema(columns=columns, partitions=partitions)
    table = o.create_table('my_new_table', schema, if_not_exists=True, lifecycle=7)

def distinct_by_cols(df, on, keep='first', keep_on=None):
    names = df.schema.names
    types = df.schema.types

    if keep_on is None:
        keep_on = on

    def dedup_and_leave_last(keys):

        def h(row, done):
            if done:
                yield row
        return h
    
    def dedup_and_leave_first(keys):
        rows = [[]]
        def h(row, done):
            if not rows:
                rows[0].append(row)
            if done:
                yield row
                rows[0] = []
        return h
    
    def dedup_and_leave_max(keys):
        buf = [None]

        def h(row, done):
            if buf[0] is None:
                buf[0] = row
            elif getattr(row, keep_on) > getattr(buf[0], keep_on):
                buf[0] = row
            if done:
                if buf[0] is not None:
                    yield buf[0]
                buf[0] = None
        return h
    def dedup_and_leave_min(keys):
        buf = [None]

        def h(row, done):
            if buf[0] is None:
                buf[0] = row
            elif getattr(row, keep_on) < getattr(buf[0], keep_on):
                buf[0] = row
            if done:
                if buf[0] is not None:
                    yield buf[0]
                buf[0] = None
        return h
    
    if keep == 'max':
        return df.map_reduce(group=on,
                             reducer=dedup_and_leave_max,
                             reducer_output_names=names,
                             reducer_output_types=types)
    elif keep == 'min':
        return df.map_reduce(group=on,
                             reducer=dedup_and_leave_min,
                             reducer_output_names=names,
                             reducer_output_types=types)
    elif keep == 'first':
        return df.map_reduce(group=on,
                         reducer=dedup_and_leave_first,
                         reducer_output_names=names,
                         reducer_output_types=types)
    else:
        return df.map_reduce(group=on,
                             reducer=dedup_and_leave_last,
                             reducer_output_names=names,
                             reducer_output_types=types)

def keep_unique(df, on):
    """ONLY keep unique rows."""
    gdf = df.groupby(on).agg(c=df.count())
    return df.join(gdf[gdf.c == 1].exclude('c'), on=on)
        
    
def df_diff(df1, df2, on):
    if isinstance(on, (list, tuple)):
        select_cols = on
    else:
        select_cols = [on]
    df = df1.left_join(df2[df2[select_cols], Scalar(1, 'int').rename('_df_diff_flag_')].distinct(), on=on, merge_columns=True)
    return df[df._df_diff_flag_.isnull()].exclude('_df_diff_flag_')


def exec_sql(sql):
    """#调用 pyodps 执行odps sql 参考 pyodps 文档 https://pyodps.readthedocs.io/zh_CN/latest/"""
    print('====> execute_sql: ' + sql)
    instance = o.run_sql(sql)
    print('====> logview: ' + instance.get_logview_address())
    instance.wait_for_success()
    
def spid_decoder(sp_id, tag, is_show):
    """Convert from sp_id to show_id or vdo_id.
    
    Parameters:
    -----------
    sp_id: int, unified id for all data.
    tag: int, 1 for show_id, 2 for vdo_id.
    is_show: int, 1 for show and other value for vdo not show.
    
    Return:
    -----------
    docoded_id: show_id or vdo_id.
    """
    if sp_id is None:
        return 0
    # tag=1 to decode show_id from ID_Encoder(1,show_id,0) (type<<60 | sl_id << 32 | vid)
    if tag==1 and is_show == 1:
        return (sp_id - (1<<60)) >> 32
    elif tag==1 and is_show !=1:
        # for vdo , product 0
        return 0
    # tag=2 to decode vdo_id from ID_Encoder(3,0,vdo_id) or ID_Encoder(4,plylst_id,vdo_id)
    # (type<<60 | sl_id << 32 | vid)
    elif tag != 1 and is_show == 1:
        return 0
    elif tag != 1 and is_show != 1:
        return sp_id & 0xFFFFFFFF
    else:
        return 0
    
    
""""
resource manipulation
"""
def get_file_from_resource(resource_path, local_file, o=None):
    if o is None:
        o = odps.from_global()
    if not o.exist_resource(resource_path):
        print('resource not exist')
        return None
    res = o.get_resource(resource_path)
    
    data = res.open('rb').read()

    with open(local_file, 'wb') as fout:
        fout.write(data)
    print('get_resource {} done'.format(resource_path))
    
def copy_file_to_resource(local_file, resource_path, resource_type, overwritten, o=None):
    """Copy local file as odps resource."""
    from odps import ODPS
    if o is None:
        o = ODPS.from_global()
    if overwritten and o.exist_resource(resource_path):
        o.delete_resource(resource_path)
    if isinstance(local_file, str) or isinstance(local_file, Text):
        fobj = open(local_file, 'rb')
    else:
        fobj = local_file
    return o.create_resource(resource_path, resource_type, file_obj=fobj)

