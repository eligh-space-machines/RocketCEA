import sys

# try to solve spaces in Windows Path names by making 8.3, short path name.
_CAN_RUN_CTYPES = False
if sys.platform == 'win32':
    try:
        import ctypes
        from ctypes import wintypes
        _GetShortPathNameW = ctypes.windll.kernel32.GetShortPathNameW
        _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
        _GetShortPathNameW.restype = wintypes.DWORD
        _CAN_RUN_CTYPES = True
    except:
        print('ERROR getting _GetShortPathNameW')

def shortpath(x):
  # from: https://mail.python.org/archives/list/python-dev@python.org/thread/H6R3AHSYGNDDJKV2ZLI43DAGUKAG2Y3O/
  z=''
  for y in x.split('\\'):
    if len(y.split('.')[0])>8:
      if ('.' in y):
        z=z+'\\'+y.split('.')[0][:6].upper()+'~1'+'.'+y.split('.')[1]
      else:
        z=z+'\\'+y[:6].upper()+'~1'
    else:
      z=z+'\\'+y
  return z[1:]

def get_short_path_name(long_name):
    """
    Gets the short path name of a given long path.
    http://stackoverflow.com/a/23598461/200291
    
    GetShortPathName is used by first calling it without a destination buffer. 
    It will return the number of characters you need to make the destination buffer. 
    You then call it again with a buffer of that size. 
    If, due to a TOCTTOU problem, the return value is still larger, 
    keep trying until you've got it right.:
    """
    
    #if sys.platform != 'win32':
    if not _CAN_RUN_CTYPES:
        print( 'Failed to get short name in get_short_path_name' )
        print( '   for long_name:', long_name )
        return long_name
    
    output_buf_size = 0
    counter = 0
    COUNTER_LIMIT = 20 # prevent infinite loop
    while counter < COUNTER_LIMIT:
        counter += 1
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        needed = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        if output_buf_size >= needed:
            print( 'Using short form of Windows path:' )
            
            if len(output_buf.value) > 0 and output_buf.value.find(' ') < 0:
                print( '   "%s"'%output_buf.value )
                return output_buf.value
            else:
                sn = shortpath(long_name)
                print( '   "%s"'%sn )
                return sn
        else:
            output_buf_size = needed
            
    print( 'Failed to get short name in get_short_path_name' )
    print( '   for long_name:', long_name )
    return long_name
