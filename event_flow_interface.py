from data_structures import AObject, AField
import subprocess
import re
import random

class EventFlowInterface(object):
    """
    Abstracts Event Framework parsing.
    """
    TOPIC_RE = re.compile("dispatcher.(publish|publish_with_header|register).Topics.([A-Z_]+)")

    def _generate_random_color(self, mixr, mixg, mixb):
        """
        mix in colors to random color
        """
        r = random.random()
        g = random.random()
        b = random.random()

        r = (r + mixr) / 2
        g = (g + mixg) / 2
        b = (b + mixb) / 2

        return (r, g, b)

    def __init__(self):
        pass

    def load_aobjects(self, directory, source_re, dest_re):
        """
        Loads event dispatch and registration into AObjects
        """
        # maps filenames/topic to aobjects
        aobjects = {}
        # maps filenames/topic to map of destination filename/topic
        visited = {}

        command_list = ["|",
                        "grep -v Binary",
                        "|",
                        "grep -v site_media",
                        "|",
                        "grep -v tests.py",
                        ">"]
        publish_output_filename = "publish.out"
        publish_command = " ".join(["grep -r dispatcher.publish(_with_header)?.Topics %s" % directory] + command_list + [publish_output_filename])
        self._do_command(publish_command)
        self._extract_objects_and_arrows(publish_output_filename,
                                         aobjects,
                                         visited,
                                         is_publishing=True)

        register_output_filename = "register.out"
        register_command = " ".join(["grep -r dispatcher.register.Topics %s" % directory] + command_list + [register_output_filename])
        self._do_command(register_command)
        self._extract_objects_and_arrows(register_output_filename,
                                         aobjects,
                                         visited,
                                         is_publishing=False)

        return aobjects.values()

    def _extract_objects_and_arrows(self,
                                    output_filename,
                                    aobjects,
                                    visited,
                                    is_publishing=True):
        # example line
        #/Users/lucy/sandbox/ck/cloudkick/helen/agent_cull_service.py:        dispatcher.publish(Topics.HELEN_NODE_LOOKUP, event, service=SERVICE)

        f = open(output_filename)
        for line in f.readlines():
            parts = line.split()
            # remove .py:
            filename_parts = parts[0].split("/")
            filename = filename_parts[-2] + "/" + filename_parts[-1][:-4]
            topic = None
            for part in parts:
                search = EventFlowInterface.TOPIC_RE.search(part)
                if search:
                    topic = search.groups()[1]
            if not topic:
                print "ERR: NO TOPIC FOUND for", line
                continue

            if filename in aobjects:
                faobject = aobjects[filename]
            else:
                faobject = AObject(name=filename,
                                   color=self._generate_random_color(1, 1, 1),
                                   shape="Circle")
                aobjects[filename] = faobject
                visited[filename] = {}

            if topic in aobjects:
                taobject = aobjects[topic]
            else:
                taobject = AObject(name=topic)
                aobjects[topic] = taobject
                visited[topic] = {}

            if is_publishing:
                source = faobject
                dest = taobject
            else:
                source = taobject
                dest = faobject

            if dest.name in visited[source.name]:
                # we've seen this combo before
                continue
            else:
                visited[source.name][dest.name] = 1
                afield = AField(name="fieldname",
                                type="bam",
                                dest=dest)
                source.add_field(field=afield)

    def _do_command(self, command):
        print
        print "THE COMMAND:"
        print command
        print
        process = subprocess.Popen(command,
                                   shell=True,
                                   stdout=subprocess.PIPE)
        stdoutdata, stderrdata = process.communicate()

        if stderrdata:
            print "STDERRDATA:"
            print stderrdata
            #except subprocess.CalledProcessError:
        if stdoutdata:
            print "STDOUTDATA:"
            print stdoutdata


    def pretty_print(self, aobjects):
        for m in aobjects:
            print m.name
            for f in m.fields:
                print "  ", f.name, f.type
                if f.dest:
                    print "      ", f.dest.name
