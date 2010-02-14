
from data_structures import *

import sys

class DjangoModelInterface(object):
    """
    Abstracts Django specific parsing and editing.
    """
    
    def __init__(self):
        raise "Nothing worth instantiating"
    
    @classmethod
    def load_aobjects(klass, apps=None):
        """
        Loads models from apps into AObjects
        
        note: Must be run from within Django project.
        note: In order for all relation edges to be shown,
            all referenced apps should be included.
        
        @param apps: list of app names, eg ['foo', 'bar']
        @return: list of AObjects
        """
        apps = apps or []
        # All AObjects created from models in apps
        # model class object -> AObject
        obj_dict = {}
        setup_django_environment()
        """
        Load models into internal data structures
        1. First pass collects models as AObjects
        2. Second pass sets fields, including ForeignKeys to AObjects
        """
        klass._model_iterator(obj_dict, apps, klass._first_pass)
        klass._model_iterator(obj_dict, apps, klass._second_pass)
        
        return obj_dict.values()

    @classmethod
    def _first_pass(klass, obj_dict, model):
        """ First pass collects models as AObjects """
        # create AObject for model class
        o = AObject(model.__name__)
        obj_dict[model] = o
    
    @classmethod
    def _second_pass(klass, obj_dict, model):
        """ Second pass sets fields, including ForeignKeys to AObjects """
        # retrieve AObject for model class
        o = obj_dict[model]

        # iterate over model's fields to add AFields
        for field in model._meta.fields:
            f = AField(field.name, field.get_internal_type())
            if field.rel:
                if field.rel.to in obj_dict:
                    f.set_destination(obj_dict[field.rel.to])
            o.add_field(field=f)
            
    @classmethod
    def _model_iterator(klass, obj_dict, apps, fn):
        """
        @param fn: function that takes 2 parameters:
            klass (DjangoModelInterface instance)
            model (class object)
        """
        for app in apps:
            app = __import__(app)
            # PD_SPECIFIC: use of ALL_MODELS, list of class names
            for model in app.models.ALL_MODELS:
                # retrieve class object for class name
                #model = getattr(app.models, model)
                fn(obj_dict, model)
    
    @classmethod
    def create_classes(klass, aobjects, filename=None):
        lines = []
        for aobject in aobjects:
            lines.append("class %s(models.Model):" % aobject.name)
            for field in aobject.fields:
                p = []
                if field.dest:
                    p.append("'%s'" % field.dest.name)
                if field.type == 'CharField':
                    p.append("max_length=200")
                lines.append("    %s = models.%s(%s)" % (field.name,
                                                         field.type,
                                                         ", ".join(p)))
            lines.append("")
            
            # ToDo: print __unicode__ and Make methods, also class docs (OG notes?)
            # more default fields? what to express in omni graffle, visually v notes
        
        if filename:
            f = open(filename)
            f.write("\n".join(lines))
            f.close()
        else:
            print "\n".join(lines)

    @classmethod
    def pretty_print(klass, aobjects):
        for m in aobjects:
            print m.name
            for f in m.fields:
                print "  ", f.name, f.type
                if f.dest:
                    print "      ", f.dest.name


####### DJANGO UTILTIES #######

def setup_django_environment():
    """ Setup Django environment """
    # Nearest ancestor directory with a 'settings.py' file
    settings_dir = _find_file_in_ancestors("settings.py")
    sys.path.append(settings_dir)
    
    from django.core.management import setup_environ
    import settings
    setup_environ(settings)

def _find_file_in_ancestors(filename):
    """
    For each parent directory, check if 'filename' exists.  If found, return
    the path; otherwise raise RuntimeError.
    """
    import os
    path = os.path.realpath(os.path.curdir)
    while not filename in os.listdir(path):
        #if filename in os.listdir(path):
        #    return path
        newpath = os.path.split(path)[0]
        if path == newpath:
            raise RuntimeError("No file '%s' found in ancestor directories." % filename)
        path = newpath
    return path