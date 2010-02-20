import sys
from optparse import OptionParser, Option, SUPPRESS_HELP

class ArgsParser(OptionParser, object):
    """
    An OptionParser that also handles positional args conveniently
    Copied from
       http://code.activestate.com/recipes/574459/
    @todo: use argparser instead?
       http://code.google.com/p/argparse/
    """
    
    def __init__(self, *args, **kw):
        self.posargs = []
        super(self.__class__, self).__init__(*args, **kw)
    
    def add_posarg(self, *args, **kw):
        pa_help = kw.get("help", "")
        kw["help"] = SUPPRESS_HELP
        o = self.add_option("--%s" % args[0], *args[1:], **kw)
        self.posargs.append((args[0], pa_help))
    
    def get_usage(self, *args, **kwargs):
        self.usage = "%%prog %s [options]\n\nPositional Arguments:\n %s" % \
        (' '.join(["<%s>" % arg[0] for arg in self.posargs]), '\n '.join(["%s: %s" % (arg) for arg in self.posargs]))
        return super(self.__class__, self).get_usage(*args, **kwargs)

    def parse_args(self, *args, **kwargs):
        args = sys.argv[1:]
        args0 = []
        for p, v in zip(self.posargs, args):
            args0.append("--%s" % p[0])
            args0.append(v)
        args = args0 + args
        options, args = super(self.__class__, self).parse_args(args, **kwargs)
        if len(args) < len(self.posargs):
            msg = 'Missing value(s) for "%s"\n' % ", ".join([arg[0] for arg in self.posargs][len(args):])
            self.error(msg)
        return options, args

def create_automodels_parser():
    """
    Constructs command line parser for AutoModels project
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
                      dest="filename",
                      help="update an existing diagram or code file (coming soon)")
    parser.add_option("-c",
                      "--create",
                      help="create new diagram or code file",
                      action="store_true",
                      default=True)
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
    
    commands=("django_to_omni_graffle",
              "d2og",
              "omni_graffle_to_django",
              "og2d")
    parser.add_posarg("command",
                      help="""Type of conversion to perform:
    django_to_omni_graffle, d2om: -
    omni_graffle_to_django, og2d: - 
    
    Request more commands or vote for these on
        http://github.com/diN0bot/Auto-Models/issues
    # django_to_dot
    # dot_to_django
    # django_to_svg
    # svg_to_django""",
                      dest='command',
                      type="choice",
                      choices=commands,
                      default=commands[0])
    return parser
    
def main(args):
    parser = create_parser()
    (options, args) = parser.parse_args()                               
    print options
    print args
    
    parser.print_help()
    
    sys.exit()
    
    # default args
    include_prefixes = options.include_prefixes or []
    exclude_prefixes = options.exclude_prefixes or []
    include_django_contrib = False
    verbosity = 2
    
    # override defaults from command line
    for opt, arg in opts:      
        #if verbosity >= 2: print "opt", opt, "arg", arg          
        if opt in ("-h", "--help"):
            usage()                     
            sys.exit()
        elif opt in ("-v", "--verbosity"):
            verbosity = arg                  
        elif opt in ("-a", "--include_prefixes"):
            include_prefixes = [x.strip() for x in arg.split(',')]
        elif opt in ("-x", "--exclude_prefixes"):
            exclude_prefixes = [x.strip() for x in arg.split(',')]                   
        elif opt in ("-d", "--include_django_contrib"): 
            include_django_contrib = True
        else:
            # we expect this to get caught by getopt.getopt
            print "\nUnknown option %s\n" % opt
            usage()
            sys.exit(2)               

    if verbosity >= 2:
        if include_prefixes: print "include prefixes", include_prefixes
        if exclude_prefixes: print "exclude prefixes", exclude_prefixes
        print "include django contrib models", include_django_contrib
        print "verbosity", verbosity
    
    aobjects = DjangoModelInterface.load_aobjects(include_prefixes=include_prefixes,
                                                  exclude_prefixes=exclude_prefixes,
                                                  include_django_contrib=include_django_contrib)
    print "\nSuccessfully loaded Django models into internal format"
    #DjangoModelInterface.pretty_print(aobjects)
    
    ogi = OmniGraffleInterface()
    ogi.create_graffle(aobjects)
    print "\nSuccessfully created OmniGraffle diagram from internal format"
    
    #print '-'*20, "expected models", '-'*20
    #expected_code = DjangoModelInterface.create_classes(aobjects)
    #DjangoModelInterface.print_classes(aobjects)
    #print '-'*60
    
    aobjects2 = ogi.load_aobjects()
    print "\nSuccessfully loaded OmniGraffle back into internal format"
    print "\nWriting Django code from format:\n"
    DjangoModelInterface.print_classes(aobjects2)
    #print '-'*20, "actual models", '-'*20
    #actual_code = DjangoModelInterface.create_classes(aobjects2)
    
if __name__ == "__main__":
    """
    test script:
    1. loads Django models
    2. writes OmniGraffle file based on models
    3. reads back OmniGraffle file
    4. prints Django classes
    """
    if len(sys.argv) < 2:
        usage()
        sys.exit(2)
    
    main(sys.argv[1:])
    

