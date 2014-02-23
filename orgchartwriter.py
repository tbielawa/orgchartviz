"""
Simple module for writing output to a specified location
"""
import sys

class OrgChartWriter(object):
    OUTPUT="org_chart.dot"
    WRITER=None
    APPEND="\n"

    def __init__(self):
        if not OrgChartWriter.WRITER:
            if OrgChartWriter.OUTPUT == '-':
                OrgChartWriter.OUTPUT = sys.stdout
                OrgChartWriter.WRITER = sys.stdout
            else:
                OrgChartWriter.WRITER = open(self.OUTPUT, 'w')

        self.WRITER = OrgChartWriter.WRITER

    def write(self, msg):
        try:
            self.WRITER.write(msg + self.APPEND)
        except Exception, e:
            print "Error in write():"
            print str(e)
        else:
            self.flush()

    def flush(self):
        self.WRITER.flush()

    def begin_output(self):
        out = "digraph org_chart {"
        self.write(out)

    def dot(self, out):
        self.write("    " + out)

    def end_output(self):
        out = "}"
        self.write(out)
