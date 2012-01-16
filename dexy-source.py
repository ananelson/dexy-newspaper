from idiopidae.runtime import Composer
from pygments import highlight
from pygments.formatters.latex import LatexFormatter
from pygments.lexers.agile import PythonLexer
import dexy
import idiopidae.parser
import inspect
import json
import pkgutil
import sys

lexer = PythonLexer()
formatter = LatexFormatter()
composer = Composer()

def fetch_item_content(cm):
    is_method = inspect.ismethod(cm)
    is_function = inspect.isfunction(cm)

    if is_method or is_function:
        try:
            source = inspect.getsource(cm)
        except IOError:
            source = ""

        builder = idiopidae.parser.parse('Document', source + "\n\0")
        sections = {}

        for i, s in enumerate(builder.sections):
            lines = builder.statements[i]['lines']
            sections[s] = composer.format(lines, lexer, formatter)

        if len(sections) == 1:
            return sections.values()[0]
        else:
            return sections
    else:
        try:
            # If this can be JSON-serialized, leave it alone...
            json.dumps(cm)
            return cm
        except TypeError:
            # ... if it can't, convert it to a string to avoid problems.
            return str(cm)

package = dexy
method_source_code = {}
class_info = {}
prefix = package.__name__ + "."

for module_loader, name, ispkg in pkgutil.walk_packages(package.__path__, prefix=prefix):
    try:
        __import__(name)
        mod = sys.modules[name]

        for k, m in inspect.getmembers(mod):

            if not inspect.isclass(m) and hasattr(m, '__module__') and m.__module__.startswith('dexy'):
                # TODO figure out how to get module constants
                key = "%s.%s" % (m.__module__, k)
                item_content = fetch_item_content(m)
                method_source_code[key] = item_content

            elif inspect.isclass(m) and m.__module__.startswith('dexy'):
                class_key = "%s.%s" % (name, k)
                class_info[class_key] = {}
                try:
                    class_info[class_key]['source'] = highlight(inspect.getsource(m), lexer, formatter)
                except IOError:
                    print "can't get source for", class_key
                    class_info[class_key]['source'] = ""


                for ck, cm in inspect.getmembers(m):
                    key = "%s.%s.%s" % (name, k, ck)
                    item_content = fetch_item_content(cm)
                    method_source_code[key] = item_content
                    class_info[class_key][ck] = item_content

    except ImportError:
        pass

with open("dexy--source.json", "w") as f:
    json.dump(method_source_code, f, sort_keys=True, indent=4)

with open("dexy--classes.json", "w") as f:
    json.dump(class_info, f, sort_keys=True, indent=4)
