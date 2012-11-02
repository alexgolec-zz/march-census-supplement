'''
Methods for reading and parsing the data dictionary specification file.
'''

from sys import stderr

class DataSpec:
    def __init__(self, name, start, end, value_min=None, value_max=None,
                 auxiliaries=None):
        self.name = name

        if start > end:
            raise ValueError('invalid position')

        self.start = start
        self.end = end

        if (value_min is not None and value_max is None or
            value_max is not None and value_min is None):
            raise ValueError('either none or both of value_min and value_max must be set')
        if (value_min is not None and value_max is not None
            and value_min > value_max):
            raise ValueError('invalid range')
            
        self.value_min = value_min
        self.value_max = value_max
        self.auxiliaries = auxiliaries

def extract_range(line):
    '''
    Extract the first singly-parenthesized item from the string. Nested
    parentheses are not supported because they are unnecessary for this
    application, and will throw. Return values are:
     - the contents of the first parenthesized block, without parentheses
     - the original string without the parenthesized block
    '''
    inside = False
    ret = []
    start = None
    end = None
    for i in xrange(0, len(line)):
        char = line[i]
        if inside is False:
            if char == '(':
                start = i
                inside = True
        elif inside is True:
            # we assume there is only one layer of nesting
            assert char != '('
            if char != ')':
                # this will be at least one, since we can only enter the
                # inside state after seeing at least one character
                ret.append(char)
            else:
                end = i
                break
    if start is not None and end is not None:
        # start is exclusive, so dont' add to it, but end is inclusive, so add
        return (''.join(ret), line[0:start]+line[end + 1:len(line)])
    else:
        return ('', line)

def data_spec_line(line):
    '''
    Turn a line into a data spec object.
    '''
    line_before = line
    # extract the value range before splitting the line
    value_range, line = extract_range(line)
    line = line.strip()

    # a little sanity checking
    if value_range != '':
        assert line+' ('+value_range+')' == line_before, line_before
    else:
        assert line == line_before

    kind, name, length, start = line.split(' ')
    length = int(length)
    start = int(start) - 1
    value_min = None
    value_max = None
    auxiliary = None

    if value_range != '':
        split = [i.strip() for i in value_range.split(',')]
        assert len(split) == 1 or len(split) == 2
        if len(split) == 2:
            val_range, aux = split
            auxiliary = [int(aux)]
        else:
            val_range = split[0]
            auxiliary = None

        value_min, value_max = val_range.split(':')
        value_min = int(value_min)
        value_max = int(value_max)

    return DataSpec(name, start, start+length,
                    value_min, value_max, auxiliary)

import re

def extract_columns(f):
    linenum = 0
    spec = []
    for line in f.xreadlines():
        linenum += 1
        line = re.sub(r' +', ' ', line.strip())
        if len(line) < 2:
            print >> stderr, linenum, 'length of line too short:', line
            continue
        elif line[0] == 'D' and line[1] == ' ':
            spec.append(data_spec_line(line))

if __name__ == '__main__':
    with open('asec2012early_pubuse.dd.txt', 'r') as f:
        extract_columns(f)
