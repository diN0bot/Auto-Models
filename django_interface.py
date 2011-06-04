from django.db.models import get_models

from data_structures import *

import sys

class DjangoModelInterface(object):
    """
    Abstracts Django specific parsing and editing.
    """

    def __init__(self):
        raise "Nothing worth instantiating"

    @classmethod
    def load_aobjects(klass, include_prefixes=None, exclude_prefixes=None, include_django_contrib=False):
        """
        Loads selected models into AObjects

        note: Must be run from within Django project.
        note: In order for all relation edges to be shown,
            all referenced models should be included.

        @param include_prefixes: list of module prefixes from which to include models; eg, ['foo', 'bar']
            if specified, other parameters are ignored
        @param exclude_prefixes: list of module prefixes from which to exclude models; eg, ['foo', 'bar']
        @param include_django_contrib: if True, includes models from django.contrib apps
        @return: list of AObjects
        """
        print include_prefixes
        print exclude_prefixes
        setup_django_environment()
        models = klass._get_models(include_prefixes, exclude_prefixes, include_django_contrib)
        """
        Load models into internal data structures
        1. First pass collects models as AObjects
        2. Second pass sets fields, including ForeignKeys to AObjects
        """
        # All AObjects created from models
        # model class object -> AObject
        obj_dict = {}
        klass._model_iterator(obj_dict, models, klass._first_pass)
        klass._model_iterator(obj_dict, models, klass._second_pass)

        return obj_dict.values()

    @classmethod
    def _get_models(klass, include_prefixes=None, exclude_prefixes=None, include_django_contrib=False):
        """
        Retrieves models based on the following rules:
        1. All models from modules matching included prefixes are included.
            Excluded and django contrib rules are ignored
        2. All models from modules matching excluded prefixes are excluded.
        3. Django contrib models are excluded unless include_django_contrib is True
        """
        DEBUG = False
        include_prefixes = include_prefixes or []
        exclude_prefixes = exclude_prefixes or []
        models = []
        for model in get_models():
            if DEBUG: print "model", model.__module__, model.__name__
            if include_prefixes:
                for app in include_prefixes:
                    if DEBUG: print "include prefix: ", app
                    if model.__module__.startswith(app):
                        models.append(model)
                        continue
                continue
            model_is_excluded = False
            for app in exclude_prefixes:
                if DEBUG: print "exclude prefix: ", app
                if model.__module__.startswith(app):
                    model_is_excluded = True
                    continue
            if DEBUG: print "model is excluded = ", model_is_excluded
            if model_is_excluded:
                continue
            if include_django_contrib or not model.__module__.startswith('django.contrib'):
                models.append(model)
        return models

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
    def _model_iterator(klass, obj_dict, models, fn):
        """
        @param fn: function that takes 2 parameters:
            klass (DjangoModelInterface instance)
            model (class object)
        """
        '''
        for app in apps:
            app = __import__(app)
            # PD_SPECIFIC: use of ALL_MODELS, list of class names
            for model in app.models.ALL_MODELS:
                # retrieve class object for class name
                #model = getattr(app.models, model)
                fn(obj_dict, model)
        '''
        for model in models:
            fn(obj_dict, model)

    @classmethod
    def print_classes(klass, aobjects, filename=None):
        """
        Convenience function for printing create_classes

        todo see python tokenizer and parser for manipulating code
        http://docs.python.org/library/tokenize.html
        http://docs.python.org/library/parser.html
        """
        lines = klass.create_classes(aobjects, filename)
        if filename:
            f = open(filename)
            f.write("\n".join(lines))
            f.close()
        else:
            print "\n".join(lines)

    @classmethod
    def create_classes(klass, aobjects, filename=None):
        """
        @return: list of strings representing lines of code
        """
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
        return lines

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
