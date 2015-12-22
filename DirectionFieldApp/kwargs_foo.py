__author__ = 'benjamin'


def foo(**kwargs):
    if 'value' in kwargs:
        str = kwargs.pop('value')
    else:
        str = 'no input!'
    print str

foo()
foo(value=1)
foo(**{'value':2})

kwargs={'value':3}
foo(**kwargs)

try:
    v = kwargs.pop('value')
    print 'success!'
except:
    print 'fail!'