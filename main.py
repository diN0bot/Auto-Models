#!/usr/bin/env python

"""
Reads Django models and creates new OmniGraffle file

Run this script:
    cd <somewhere in Django project>
    python <absolute path>/main.py
"""


from django_interface import DjangoModelInterface, _find_file_in_ancestors
from omni_interface import OmniGraffleInterface

import sys

if __name__ == "__main__":
    """
    test script:
    1. loads Django models
    2. writes OmniGraffle file based on models
    3. reads back OmniGraffle file
    4. prints Django classes
    """
    
    if len(sys.argv) > 1:
        apps = sys.argv[1].split(',')
    else:
        try:
            # settings.APPS is a neat Django trick:
            # http://proudly.procrasdonate.com/django-tricks-part-5-automatic-app-settings/
            settings_dir = _find_file_in_ancestors("settings.py")
            sys.path.append(settings_dir)
            
            from django.core.management import setup_environ
            import settings
            setup_environ(settings)
            apps = settings.APPS
        except:
            print """
Please provide comma-separated list of Django apps:
    python <path>/main.py foo,bar,baz
    
"""
            exit(1)
    
    aobjects = DjangoModelInterface.load_aobjects(apps)
    #DjangoModelInterface.pretty_print(aobjects)
    
    ogi = OmniGraffleInterface()
    ogi.create_graffle(aobjects)
    
    # not yet written
    aobjects2 = ogi.load_aobjects()
    
    DjangoModelInterface.create_classes(aobjects)
    