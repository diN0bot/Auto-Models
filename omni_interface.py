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
                    print afield.dest
                    if afield.dest in nodes:
                        print "in nodes"
                        self._write_edge(nodes[aobject], nodes[afield.dest])
                    else:
                        print "not in nodes"
                else:
                    print "no afield dest for", afield.name, afield.type
                    
    def _write_node(self, document, aobject):
        properties = {#appscript.k.url: link,
                      appscript.k.text: aobject.name,
                      appscript.k.autosizing: appscript.k.full,
                      appscript.k.draws_shadow: True,}
        
        return document.make(new=appscript.k.shape, 
                             #at=document.graphics.first, 
                             with_properties=properties)   
    
    def _write_edge(self, aobject_src, aobject_dest):
        properties = {appscript.k.line_type: appscript.k.curved}
        
        self.og.connect(aobject_src,
                        to=aobject_dest, 
                        with_properties=properties)

#    og.layout(doc.document.pages.first)
 
