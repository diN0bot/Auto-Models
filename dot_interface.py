import subprocess

class DotInterface(object):
    """
    Abstracts dot specific parsing and editing.
    """

    '''
    digraph graphname {

    a [label="Foo"];
    b [shape=box];
    c [label="XXX", shape=circle];

    a -> b -> c [color=blue];
    b -> d [style=dotted];
    a -> c [color=green, style=dotted];

    }
    '''

    def __init__(self, name):
        self.name = name

    def create_dotfile(self, AObjects):
        """
        Writes AObjects to dot file
        1. First pass writes object shapes
        2. Second pass writes arrows
        3. Does layout
        """
        f = open(self.name, 'w')
        f.write("digraph %s {\n\n" % self.name)
        f.write("rankdir=LR;\n\n")

        """ write dot file """
        visited = {}
        for aobject in AObjects:
            self._write_node(f, aobject)
            visited[aobject] = 1

        for aobject in AObjects:
            for afield in aobject.fields:
                if afield.dest:
                    if afield.dest in visited:
                        self._write_edge(f, aobject, afield.dest, afield.dest.color)

        f.write("\n}\n")
        f.close()

    def create_pdf(self):
        command = ["dot", "-O", "-Tpdf", self.name]
        subprocess.Popen(command)

    def _retrieve_color(self, color):
        s = "#"
        for c in color:
            cstr = "%x" % (c * 255)
            if len(cstr) < 2:
                cstr = "0%s" % cstr
            if len(cstr) > 2:
                print cstr
                cstr = "00"
            s += cstr
        return s

    def _write_node(self, f, aobject):
        """
        creates two nodes, one for name, one for list of fields,
        and assembles them into a single node group
        @return: group
        """
        shape = "box"
        if aobject.shape == "Rectangle":
            shape = "rectangle"
        elif aobject.shape == "Circle":
            shape = "oval"

        if aobject.color == (1, 1, 1):
            color = (0, 0, 0)
        else:
            color = aobject.color
        color = self._retrieve_color(color)

        properties = {'label': aobject.name,
                      'shape': shape,
                      'fillcolor': color}
        if color != "#000000":
            properties['style'] = "filled"

        properties_str = ", ".join(['%s="%s"' % (k, v) for k, v in properties.items()])
        f.write('"%s" [%s];\n' % (aobject.name, properties_str))

    def _write_edge(self, f, src, dest, color):
        if color == (1, 1, 1):
            color = (0, 0, 0)
        color = self._retrieve_color(color)

        f.write('"%s" -> "%s" [color="%s", penwidth=3];\n' % (src.name,
                                                              dest.name,
                                                              color))
