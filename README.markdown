
## OVERVIEW

1. Turns the following code:
    
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
        
into an OmniGraffle diagram that looks like this:

<img src="http://github.com/diN0bot/Auto-Models/raw/master/screenshot.png" width="50%" />

2. Coming soon: turn the above OmniGraffle diagram into Django code:

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

3. Coming eventually: keep existing diagrams and code in synch.

## STATUS

[x] Create OmniGraffle diagram from Django models code
[ ] Update OmniGraffle diagram from Django models code
[-] Create Django models code from OmniGraffle diagram
[ ] Update Django models code from OmbniGraffle diagram

## DEPENDENCIES

OmniGraffle
http://www.omnigroup.com/applications/omnigraffle/
 -> Mac-only software
 -> requires OmniGraffle
 -> requires appscript, python library for AppleScript
http://appscript.sourceforge.net/py-appscript/doc/
    sudo easy_install appscript

Django
http://djangoproject.com

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

If requested:

[ ] Remove diN0-specific Django dependencies so people (without sweet
Django setups) can use this off the shelf....once someone not me
wants to use this, that is :-)

[ ] GUI interface

[ ] other diagram formats

[ ] other code formats?
