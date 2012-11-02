'''
Methods for reading data from the ugly-ass data file.
'''

def translate_line(line, columns):
    '''
    Given a line and a list of column specifications, generate a dictionary
    with the contents of the line, keyed by the column name as specified in the
    data dictionary.
    '''
    ret = {}
    for col in columns:
        ret[col.name] = line[col.start:col.end]
    return ret

from data_dictionary import extract_columns

def ProgressReporter(generator, iterations, name='entries'):
    class ProgressReporterClass:
        def __init__(self):
            self.progress = 0
        def next(self):
            self.progress += 1
            if self.progress % iterations == 0 and self.progress != 0:
                print 'processed', self.progress, name
            return generator.next()
        def __iter__(self):
            return self
    return ProgressReporterClass()

if __name__ == '__main__':
    with open('asec2012early_pubuse.dd.txt', 'r') as f:
        cols = extract_columns(f) 
    total = 0
    num = 0
    with open('asec2012early_pubuse.dat', 'r') as f:
        try:
            for line in ProgressReporter(f.xreadlines(), 1000):
                translated = translate_line(line, cols)
                income = int(translated['HTOTVAL'])
                if income != 0:
                    total += income
                    num += 1
        except KeyboardInterrupt:
            pass
    print 'processed', num, 'lines in total'
    print float(total) / num
