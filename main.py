#!/usr/bin/env python

"""
Reads Django models and creates new OmniGraffle file

Run this script:
    cd <somewhere in Django project>
    python <absolute path>/main.py
"""


from django_interface import DjangoModelInterface
from omni_interface import OmniGraffleInterface

if __name__ == "__main__":
    import settings
    dji = DjangoModelInterface(settings.APPS)
    #dji.pretty_print()
    
    omi = OmniGraffleInterface()
    omi.create_graffle(dji.AObjects.values())
    