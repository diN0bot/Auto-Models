#!/usr/bin/env python

"""
Reads Django models and creates new OmniGraffle file

Run this script for usage instructions:
    cd <somewhere in Django project>
    python <absolute path>/main.py --help
"""

from django_interface import DjangoModelInterface, _find_file_in_ancestors
from omni_interface import OmniGraffleInterface
from ext.ArgsParser import ArgsParser

def create_parser():
    """
    Constructs command line parser
    """
    parser = ArgsParser()
    parser.add_option("-d",
                      "--include_django_contrib",
                      #dest="include_django_contrib",
                      help="include models from Django.contrib apps. \
                      django.contrib models are excluded by default",
                      action="store_true",
                      default=False)
    parser.add_option("-u",
                      "--update",
                      help="update an existing diagram or code file rather than creating one (coming soon)",
                      action="store_true",
                      default=False)
    '''
    parser.add_option("-c",
                      "--create",
                      help="create new diagram or code file",
                      action="store_true",
                      default=True)
    '''
    parser.add_option("-v",
                      "--verbosity",
                      dest="verbosity",
                      help="Verbosity level; 0=minimal output, 1=normal output, 2=all output",
                      default=0)
    parser.add_option("-a",
                      "--include_prefixes",
                      dest="include_prefixes",
                      help="comma-separated, NO WHITESPACE, list of model module prefixes \
                        Models that start with an includes item are included. \
                        eg, --include_prefixes=myapp,django.contribue.auth")
    parser.add_option("-x",
                      "--exclude_prefixes",
                      dest="exclude_prefixes",
                      help="comma-separated, NO WHITESPACE, list of model module prefixes \
                        Models that start with an excludes item are excluded. \
                        eg, --exclude_prefixes=myapp.uninterestingmodels,south")
    
    commands=("help","-h","--help",
              "django_to_omni_graffle",
              "d2og",
              "omni_graffle_to_django",
              "og2d")
    parser.add_posarg("command",
                      help="""Type of conversion to perform.
 Should be one of the following:
    help: prints command line interface usage instructions
    django_to_omni_graffle or d2om: create omni graffle diagram from django models
    omni_graffle_to_django or og2d: write django models from omni graffle diagram
    
    Request more commands or vote for these on
        http://github.com/diN0bot/Auto-Models/issues
    # django_to_dot
    # dot_to_django
    # django_to_svg
    # svg_to_django""",
                      dest='command',
                      type="choice",
                      choices=commands)
    return parser
    
def main():
    parser = create_parser()
    (options, args) = parser.parse_args()                               
    
    # default args
    command = options.command
    is_update = options.update
    verbosity = options.verbosity
    # if django to ...
    include_prefixes = options.include_prefixes and options.include_prefixes.split(',') or []
    exclude_prefixes = options.exclude_prefixes and options.exclude_prefixes.split(',') or []
    
    include_django_contrib = options.include_django_contrib
    # if update
    #filename = options.filename
    
    if verbosity >= 2:
        print options
        print args
        print include_prefixes
        print exclude_prefixes

    if command in ("help", "-h", "--help"):
        parser.print_help()
    elif command in ("django_to_omni_graffle", "d2og"):
        if verbosity >= 1: print "starting %s..." % command
        aobjects = DjangoModelInterface.load_aobjects(include_prefixes=include_prefixes,
                                                      exclude_prefixes=exclude_prefixes,
                                                      include_django_contrib=include_django_contrib)
        if verbosity >= 0:
            print "\nSuccessfully loaded Django models into internal format"
        if verbosity >= 3:
            DjangoModelInterface.pretty_print(aobjects)
        
        ogi = OmniGraffleInterface()
        ogi.create_graffle(aobjects)
        if verbosity >= 1:
            print "\nSuccessfully created OmniGraffle diagram from internal format"
        
    elif command in ("omni_graffle_to_django", "og2d"):
        ogi = OmniGraffleInterface()
        aobjects2 = ogi.load_aobjects()
        if verbosity >= 1:
            "\nSuccessfully loaded OmniGraffle back into internal format"
        if verbosity >= 1:
            "\nWriting Django code from format:\n"
        DjangoModelInterface.print_classes(aobjects2)

if __name__ == "__main__":
    """
    test script:
    1. loads Django models
    2. writes OmniGraffle file based on models
    3. reads back OmniGraffle file
    4. prints Django classes
    """
    main()
