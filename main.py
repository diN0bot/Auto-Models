#!/usr/bin/env python

"""
Reads Django models and creates new OmniGraffle file

Run this script for usage instructions:
    cd <somewhere in Django project>
    python <absolute path>/main.py --help
"""

import sys

try:
    from omni_interface import OmniGraffleInterface
except ImportError:
    OmniGraffleInterface = None

from event_flow_interface import EventFlowInterface
from dot_interface import DotInterface
from ext.ArgsParser import ArgsParser


def pretty_print(klass, aobjects):
    for m in aobjects:
        print m.name
        for f in m.fields:
            print "  ", f.name, f.type
            if f.dest:
                print "      ", f.dest.name


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

    commands = ("help", " - h", " - -help",
                "django_to_omni_graffle",
                "d2og",
                "omni_graffle_to_django",
                "og2d",
                "event_flow_to_omni_graffle",
                "ef2og",
                "event_flow_to_dot",
                "ef2dot")
    parser.add_posarg("command",
                      help="""Type of conversion to perform.
 Should be one of the following:
    help: prints command line interface usage instructions
    django_to_omni_graffle or d2om: create omni graffle diagram from django models
    omni_graffle_to_django or og2d: write django models from omni graffle diagram
    event_flow_to_omni_graffle or ef2og: create omni graffle diagram from event flow
    event_flow_to_dot or ef2dot: create dot diagram from event flow

    Request more commands or vote for these on
        http: // github.com / diN0bot / Auto - Models / issues
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
        return

    if (command.startswith("og2") or command.startswith("omgni_graffle_to_") or \
       command.endswith("2og") or command.endswith("_to_omni_graffle")) \
       and not OmniGraffleInterface:
       print 'Could not import OmniGraffleInterface, probably ' + \
             'missing "appscript" package.'
       print 'You can install it using pip: pip install appscript'
       sys.exit(1)

    # do loading portion of command
    if command.startswith("d2") or command.startswith("django_to_"):
        # we don't want to load django settings if we don't have to
        from django_interface import DjangoModelInterface

        if verbosity >= 1: print "starting %s..." % command
        aobjects = DjangoModelInterface.load_aobjects(include_prefixes=include_prefixes,
                                                      exclude_prefixes=exclude_prefixes,
                                                      include_django_contrib=include_django_contrib)
        successfully_loaded = "Django models"
        write_fields_in_object = True

    elif command.startswith("og2") or command.startswith("omgni_graffle_to_"):
        ogi = OmniGraffleInterface()
        aobjects2 = ogi.load_aobjects()
        successfully_loaded = "OmniGraffle"

    elif command.startswith("ef2") or command.startswith("event_flow_to_"):
        import config
        efi = EventFlowInterface()
        aobjects = efi.load_aobjects(config.EVENT_FLOW_DIRECTORY,
                                     config.EVENT_SOURCE_REGEX,
                                     config.EVENT_DEST_REGEX)
        successfully_loaded = "Event Flow"
        write_fields_in_object = False

    # tell the user what happened
    if verbosity >= 0:
        print "\nSuccessfully loaded %s into internal format" % successfully_loaded
    if verbosity >= 3:
        pretty_print(aobjects)

    # do loading portion of command
    if command.endswith("2og") or command.endswith("_to_omni_graffle"):
        ogi = OmniGraffleInterface()
        ogi.create_graffle(aobjects,
                           write_fields_in_object=write_fields_in_object)
        created = "OmniGraffle diagram"

    elif command.endswith("2d") or command.endswith("_to_django"):
        DjangoModelInterface.print_classes(aobjects)
        created = "Django models"

    elif command.endswith("2dot") or command.endswith("_to_dot"):
        import config
        config.GENERATED_FILE_DIRECTORY
        doti = DotInterface("event_flow")
        doti.create_dotfile(aobjects)
        doti.create_pdf()
        created = "Dot diagram"

    if verbosity >= 1:
        print "\nSuccessfully created %s from internal format" % created


if __name__ == "__main__":
    """
    test script:
    1. loads Django models
    2. writes OmniGraffle file based on models
    3. reads back OmniGraffle file
    4. prints Django classes
    """
    main()
