import appscript

from data_structures import *

class OmniGraffleInterface(object):
    """
        Abstracts OmniGraffle specific parsing and editing.
    """
    
    # OmniGraffle appscript instance
    og = None
    
    def __init__(self, name=None):
        try:
            if name:
                self.og = appscript.app(name)
            else:
                try:
                    self.og = appscript.app('OmniGraffle.app')
                except:
                    self.og = appscript.app('OmniGraffle Professional 5.app')
        except:
            raise "Could not find OmniGraffle application"
    
    def create_graffle(self, AObjects):
        """
        Writes AObjects to OmniGraffle file via appscript
        1. First pass writes object shapes
        2. Second pass writes arrows
        3. Does layout
        """
        self.og.make(new=appscript.k.document)
        main_doc = self.og.windows.first.get()
        
        # AObject -> omni node
        nodes = {}
        
        """ write OmniGraffle file """
        for aobject in AObjects:
            n = self._write_node(main_doc, aobject)
            nodes[aobject] = n
        
        for aobject in AObjects:
            for afield in aobject.fields:
                if afield.dest:
                    if afield.dest in nodes:
                        self._write_edge(nodes[aobject], nodes[afield.dest])
        
        # adjust pages automatically based on node layout
        main_doc.adjusts_pages.set(True)
        
        # set automatic layout
        main_doc.layout_info.get().type.set(appscript.k.force_directed)
        #main_doc.layout_info.get().automatic_layout.set(True)
        self.og.layout(main_doc.graphics)
        
    def update_graffle(self, AObjects, filename):
        """
        Updates OmniGraffle file based on AObjects
        
        First Pass:
        1. Iterate through existing OG nodes
            -> If there is a matching AObject
                remove existing fields, relations
        2. Create nodes for AObjects without matches
        
        Second Pass:
        1. Iterate through OG node/AObject pairs from first pass
            -> add fields and relations
        """
        self.og.open(filename)
        main_doc = self.og.windows.first.get()
        
        #todo
    
    def load_aobjects(self, filename=None):
        """
        Loads OmniGraffle file into AObjects
        1. Iterate over groups to construct AObjects with dest-less fields
        2. Iterate over AObjects, reconstruct field types and dest links as appropriate
        
        @return: list of AObjects
        """
        if filename:
            self.og.open(filename)
        main_doc = self.og.windows.first.get()
        
        # group -> AObject
        group_aobj_dict = {}
        
        #### 1. Construct AObject for each graphic
        for group in main_doc.groups.get():
            n0 = group.graphics.get()[0]
            n1 = group.graphics.get()[1]
            if ':' in n0.text.get():
                fields = n0
                name = n1
            else:
                fields = n1
                name = n0
            
            # retrieve AObject name
            ao = AObject(name.text.get())
            # retrieve AObject fields
            for fullfield in fields.text.get().split('\n'):
                name = fullfield.split(':')[0].strip()
                type = fullfield.split(':')[1].strip()
        
                if type[:-1] == 'F':       # CharF, IntegerF
                    type = "%sield" % type # CharField, IntegerField
                # do this in second pass
                #elif type[:2] == '->':
                #    type = "ForeignKey"
                #    dest = AObject with name == type[2:]
                ao.add_field(name=name, type=type)
                group_aobj_dict[group] = ao
        
        #### 2. Recreate AField destination links
        for group, ao in group_aobj_dict.items():
            for field in ao.fields:
                if field.type[:2] == '->':
                    dest_name = field.type[2:]
                    # find destination AObject
                    for line in group.outgoing_lines.get():
                        dest_ao = group_aobj_dict[line.destination.get()]
                        # check if this is the right line for the field type
                        if dest_ao.name == dest_name:
                            field.dest = dest_ao
                    field.type = 'ForeignKey'
                
        return group_aobj_dict.values()
    
    def _write_node(self, document, aobject):
        """
        creates two nodes, one for name, one for list of fields,
        and assembles them into a single node group
        @return: group
        """
        properties = {appscript.k.text: aobject.name,
                      appscript.k.autosizing: appscript.k.full,
                      appscript.k.draws_shadow: True}
        
        n_name = document.make(new=appscript.k.shape, 
                               #at=document.graphics.first, 
                               with_properties=properties)
        
        field_names = []
        for f in aobject.fields:
            # this needs to be reversible
            if f.type[:-5] == 'Field': # CharField, IntegerField
                type = f.type[:-4]     # CharF, IntegerF
            elif f.type == 'ForeignKey' and f.dest: # ForeignKey (to AObject named User)
                type = "->%s" % f.dest.name         # eg ->User, ->Post
            else:
                type = f.type
            field_names.append("%s: %s" % (f.name, type))
        #field_names = ["%s: %s" % (f.name, type) for f in aobject.fields]
        properties = {appscript.k.text: '\n'.join(field_names),
                      appscript.k.autosizing: appscript.k.full,
                      appscript.k.draws_shadow: True}
        
        n_fields = document.make(new=appscript.k.shape, 
                               #at=document.graphics.first, 
                               with_properties=properties)
        
        # set widths to be the same
        max_width = max(n_fields.size.get()[0], n_name.size.get()[0])
        n_name.size.set([max_width, n_name.size.get()[1]])
        n_fields.size.set([max_width, n_fields.size.get()[1]])
        
        # position field node beneath name node
        #  same x as name, add height to y
        n_fields.origin.set([n_name.origin.get()[0],
                             n_name.origin.get()[1]+n_name.size.get()[1]])
        
        # assemble
        return document.assemble([n_name, n_fields])
    
    def _write_edge(self, aobject_src, aobject_dest):
        properties = {appscript.k.line_type: appscript.k.curved,
                      appscript.k.tail_type:"FilledArrow"}
        
        self.og.connect(aobject_src,
                        to=aobject_dest, 
                        with_properties=properties)

#    og.layout(doc.document.pages.first)
 
