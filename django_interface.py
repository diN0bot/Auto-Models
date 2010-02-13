
from data_structures import *

import sys

class DjangoModelInterface(object):
    """
    Abstracts Django specific parsing and editing.
    """
    
    def __init__(self, apps=None):
        """
        Loads models from apps into AObjects
        
        note: Must be run from within Django project.
        note: In order for all relation edges to be shown,
            all referenced apps should be included.
        @param apps: list of app names, eg ['foo', 'bar']
        """
        # All AObjects created from models in apps
        # model class object -> AObject
        self.AObjects = {}
        DjangoModelInterface._setup_django_environment()
        if apps:
            self.load_models(apps)
    
    def load_models(self, apps):
        """
        Load models into internal data structures
        1. First pass collects models as AObjects
        2. Second pass sets fields, including ForeignKeys to AObjects
        """
        self._model_iterator(apps, self._first_pass)
        self._model_iterator(apps, self._second_pass)

    def _first_pass(self, model):
        """ First pass collects models as AObjects """
        # create AObject for model class
        o = AObject(model.__name__)
        self.AObjects[model] = o
    
    def _second_pass(self, model):
        """ Second pass sets fields, including ForeignKeys to AObjects """
        # retrieve AObject for model class
        o = self.AObjects[model]

        # iterate over model's fields to add AFields
        for field in model._meta.fields:
            f = AField(field.name, field.get_internal_type())
            if field.rel:
                if field.rel.to in self.AObjects:
                    f.set_destination(self.AObjects[field.rel.to])
            o.add_field(field=f)
            
    def _model_iterator(self, apps, fn):
        """
        @param fn: function that takes 2 parameters:
            self (DjangoModelInterface instance)
            model (class object)
        """
        for app in apps:
            app = __import__(app)
            # PD_SPECIFIC: use of ALL_MODELS, list of class names
            for model in app.models.ALL_MODELS:
                # retrieve class object for class name
                #model = getattr(app.models, model)
                fn(model)
    
    @classmethod
    def _setup_django_environment(klass):
        """ Setup Django environment """
        # Nearest ancestor directory with a 'settings.py' file
        settings_dir = klass._find_file_in_ancestors("settings.py")
        sys.path.append(settings_dir)
        
        from django.core.management import setup_environ
        import settings
        setup_environ(settings)
    
    @classmethod
    def _find_file_in_ancestors(klass, filename):
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

    def pretty_print(self):
        for m in self.AObjects.values():
            print m.name
            for f in m.fields:
                print "  ", f.name, f.type
                if f.dest:
                    print "      ", f.dest.name
        