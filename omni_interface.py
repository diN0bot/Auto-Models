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
    
    def _write_node(self, document, aobject):
        """
        creates two nodes, one for name, one for list of fields,
        and assembles them into a single node group
        @return: group
        """
        properties = {#appscript.k.url: link,
                      appscript.k.text: aobject.name,
                      appscript.k.autosizing: appscript.k.full,
                      appscript.k.draws_shadow: True}
        
        n_name = document.make(new=appscript.k.shape, 
                               #at=document.graphics.first, 
                               with_properties=properties)
        
        properties = {#appscript.k.url: link,
                      appscript.k.text: '\n'.join([f.name for f in aobject.fields]),
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
        properties = {appscript.k.line_type: appscript.k.curved}
        
        self.og.connect(aobject_src,
                        to=aobject_dest, 
                        with_properties=properties)

#    og.layout(doc.document.pages.first)
 
