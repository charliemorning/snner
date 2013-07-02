__author__ = 'charlie'


from email.utils import parsedate_tz
import datetime


set_value = lambda nm,v_set,dft: v_set[nm] if nm in v_set else dft


def parse_datestr(datestr):

    time_tuple = parsedate_tz(datestr)

    y,m,d,h,min,s = time_tuple[:6]

    return datetime.datetime(y,m,d,h,min,s)

