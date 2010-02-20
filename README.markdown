
## OVERVIEW

### Turns the following code:
    
     class TestType(models.Model):
         OS_TYPES_LIST = ["Windows", "Mac", "Ubuntu"]
         os_types_max_len, OS_TYPES, OS_TYPES_CHOICES = model_utils.convert_to_choices(OS_TYPES_LIST)
         
         OS_VERSION_LIST = ["7", "XP", "Vista", "X.4", "X.5", "X.6", "8.04", "9.06"]
         os_version_max_len, OS_VERSION, OS_VERSION_CHOICES = model_utils.convert_to_choices(OS_VERSION_LIST)
         
         FF_VERSION_LIST = ["3.0", "3.5", "3.6"]
         ff_max_len, FF_VERSION, FF_VERSION_CHOICES = model_utils.convert_to_choices(FF_VERSION_LIST)
         
         slug = models.CharField(max_length=200)
         name = models.CharField(max_length=200)
         os_type = models.CharField(max_length=os_types_max_len, choices=OS_TYPES_CHOICES)
         os_version = models.CharField(max_length=os_version_max_len, choices=OS_VERSION_CHOICES)
         ff_version = models.CharField(max_length=ff_max_len, choices=FF_VERSION_CHOICES)
         
         ...
         
     class TestRun(models.Model):
         test_type = models.ForeignKey(TestType)
         dtime = models.DateTimeField(db_index=True)
         is_pass = models.BooleanField(default=False)
         number_fail = models.IntegerField(default=-1)
         total = models.IntegerField(default=-1)
         duration = models.IntegerField(default=-1)
         
         ...
        
### into an OmniGraffle diagram that looks like this:

<img src="http://github.com/diN0bot/Auto-Models/raw/master/screenshot.png" width="35%" />

### Turns the above OmniGraffle diagram into the following Django code:

     class TestType(models.Model):
         id = models.AutoField()
         slug = models.CharField(max_length=200)
         name = models.CharField(max_length=200)
         os_type = models.CharField(max_length=200)
         os_version = models.CharField(max_length=200)
         ff_version = models.CharField(max_length=200)

     class TestRun(models.Model):
         id = models.AutoField()
         test_type = models.ForeignKey('TestType')
         dtime = models.DateTimeField()
         is_pass = models.BooleanField()
         number_fail = models.IntegerField()
         total = models.IntegerField()
         duration = models.IntegerField()


### Coming soon: keep existing diagrams and code in synch.

## STATUS

[x] Create OmniGraffle diagram from Django models code

[ ] Update OmniGraffle diagram from Django models code

[X] Create Django models code from OmniGraffle diagram

[ ] Update Django models code from OmniGraffle diagram

[ ] Same as above but for SVG or GraphViz's dot format instead of OmniGraffle

## DEPENDENCIES

OmniGraffle

*   [http://www.omnigroup.com/applications/omnigraffle/](http://www.omnigroup.com/applications/omnigraffle/)
*   Mac-only software
*   requires OmniGraffle
*   requires appscript, python library for AppleScript
*   [http://appscript.sourceforge.net/py-appscript/doc/](http://appscript.sourceforge.net/py-appscript/doc/)

    sudo easy_install appscript

Django

*   [http://djangoproject.com](http://djangoproject.com)

## RUN

From command line:

    cd <Django project (or some directory inside project)>
    python main.py <django app name>,<django app2 name>,...
    
For example, to create a diagram for the models in apps foo
and bar, run like so:

    python main.py foo,bar
    
The script does a force-directed layout on the models. This will
likely need to be tweaked, both through the "Canvas: Diagram Layout"
inspector (apple-4) and by hand.

## TODO

[x] Add fields to diagram nodes

[x] First pass automatic layout

[ ] Be lenient in what is accepted when loading OmniGraffle files (to 
    permit users to alter, add notes)
    
[ ] More robust, clean errors all over

If requested:

[ ] Remove diN0-specific Django dependencies so people (without sweet
Django setups) can use this off the shelf

[ ] Nice GUI or command-line interface

[ ] other diagram formats

[ ] other code formats


docs

http://developer.apple.com/mac/library/documentation/Cocoa/Conceptual/ObjCTutorial/05View/05View.html#//apple_ref/doc/uid/TP40000863-CH7-SW1

http://developer.apple.com/mac/library/referencelibrary/GettingStarted/Learning_Objective-C_A_Primer/index.html#//apple_ref/doc/uid/TP40007594

http://en.wikipedia.org/wiki/Objective-C

http://developer.apple.com/cocoa/pyobjc.html

http://lethain.com/entry/2008/aug/22/an-epic-introduction-to-pyobjc-and-cocoa/


http://github.com/lethain/metawindow/blob/master/MWController.py

http://www.cs.usfca.edu/~jbovet/pyobjc/tutorial/tutorial.html


http://scottr.org/blog/2008/jun/11/build-cocoa-guis-python-pyobjc-part-one/

http://scottr.org/blog/2008/jun/11/build-cocoa-guis-python-pyobjc-part-two/


http://scottr.org/blog/2008/jun/23/building-cocoa-guis-python-pyobjc-part-three/

