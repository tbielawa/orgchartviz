import ldap
import orgchartwriter

class Person(object):
    managerattr = None

    def __init__(self, res, l):
        # res = ldap search result tuple
        self.dn = res[0]
        self.uid = res[1]['uid'][0]
        self.manager = None
        self.res = res
        # No children by default
        self.children = []
        self.l = l
        self.filterchildren = "(%s=%s)" % (self.managerattr, self.dn)
        self._print_node()
        self.ex_contract = self.res[1]['rhatPersonType'][0] == 'Ex-contingent Worker'

    def log(self, msg):
        o = orgchartwriter.OrgChartWriter()
        o.dot(msg)

    def _print_node(self):
        pass

    def find_children(self):
        pass

    def has_children(self):
        # Do a search for potential children, return that
        return self.l.search(filterstr=self.filterchildren)

class Employee(Person):
    def _print_node(self):
        shape="ellipse"
        self.log("node [shape=%s]; \"%s\";" % (shape, self.uid))

class Manager(Person):
    def _print_node(self):
        shape="triangle"
        self.log("node [shape=%s]; \"%s\";" % (shape, self.uid))

    def find_children(self):
        # self.log("finding children")
        children = self.has_children()
        if children:
            # self.log("I have children")
            # Any results returned?
            for child in children:
                child_name = child[1]['uid'][0]
                # self.log("Inspecting child: %s" % child_name)
                # Check if they have children themselves
                c = Person(child, self.l)

                if c.ex_contract:
                    # This is an ex-contractor account, don't show it
                    continue

                if c.has_children():
                    # self.log("%s has children" % c.uid)
                    # OK, they do, so they're a manager
                    m = Manager(child, self.l)
                    self.children.append(m)
                    # self.log("Calling %s's find_children() method" % child_name)
                    m.find_children()
                else:
                    # Nope, they're just a leaf-node
                    self.children.append(Employee(child, self.l))

            self.print_dot()

    def print_dot(self):
        children_names = [ c.uid for c in self.children]
        self.log("\"%s\" -> {%s};" % (self.uid, '"{0}"'.format('" "'.join(children_names))))
