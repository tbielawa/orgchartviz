#!/usr/bin/env python
import argparse
from pprint import pprint as p
import ldap
import people
import orgchartwriter

class org_chart_ldap(object):
    def __init__(self, uri=None, search_base=None, cacert_file=None):
        self.search_base = search_base
        self.uri = uri
        if cacert_file:
            ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, cacert_file)
        self._initialize()

    def _initialize(self):
        self.l = ldap.initialize(self.uri)
        self._bind()

    def _bind(self):
        self.l.simple_bind_s("", "")

    def search(self, filterstr=None):
        return self.l.search_s(self.search_base, ldap.SCOPE_SUBTREE, filterstr=filterstr)


parser = argparse.ArgumentParser(description="Generate a dot language digraph of an org chart from LDAP")
parser.add_argument("--uri", "-u", required=True,
                    help="ldap:// URI to your ldap server")
parser.add_argument("--search-base", "-b", required=True,
                    help="Search base for limiting queries (ex: dc=company,dc=com)")
parser.add_argument("--start-filter", "-s", required=True,
                    help="LDAP filterstring which matches the person you want to build an org chart from (ex: uid=pointyhairboss)")
parser.add_argument("--manager-attr", "-m",
                    default="manager",
                    help="Attribute to associate employees to managers. Default 'manager'")
parser.add_argument("--out", "-o",
                    default="org_chart.dot",
                    help="File name for dot output file. Use '-' for stdout. Default org_chart.dot")
parser.add_argument("--cacert", "-c",
                    help="Path to the CA file for secure connections")
args = parser.parse_args()

people.Person.managerattr = args.manager_attr
orgchartwriter.OrgChartWriter.OUTPUT = args.out

try:
    logger = orgchartwriter.OrgChartWriter()
    logger.begin_output()
    l = org_chart_ldap(uri=args.uri, search_base=args.search_base, cacert_file=args.cacert)
    first_result = l.search(filterstr=args.start_filter)[0]
    first_result_obj = people.Manager(first_result, l)
    first_result_obj.find_children()
except KeyboardInterrupt:
    pass
else:
    logger.end_output()
