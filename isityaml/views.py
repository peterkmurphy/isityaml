# PKM2017 - using a simpler, yet more modern way of rendering content.

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render

# The following code updates the scanner so that it can deal with Unicode
# anchors and aliases.

# PKM2017 - hopefully this will be removed in future versions of the code
# as the YAML parser will be updated to sort out this bug.

from yaml import compose_all, serialize_all
from yaml.scanner import Scanner, ScannerError;
from yaml.reader import Reader
from yaml.parser import Parser
from yaml.composer import Composer
from yaml.constructor import Constructor, SafeConstructor
from yaml.resolver import Resolver
from yaml.error import YAMLError;

class Scanner12(Scanner):
    ''' This is an updated version of the YAML scanner that handles Unicode
        anchors.
    '''

    def __init__(self):
        super(Scanner12, self ).__init__();

    def scan_anchor(self, TokenClass):
        ''' After 1.2, it is clear which characters can be part of an anchor -
            and '[ *alias, value ]' should always report an error because
            commas are forbidden to be part of an anchor or alias name.

            So this code removes the restriction that anchor/alias values be
            numbers and ASCII letters.
        '''
        start_mark = self.get_mark()
        indicator = self.peek()
        if indicator == u'*':
            name = 'alias'
        else:
            name = 'anchor'
        self.forward()
        length = 0
        ch = self.peek(length)
        while ch not in u'\0 \t\r\n\x85\u2028\u2029,[]{}':
            length += 1
            ch = self.peek(length)
        if not length:
            raise ScannerError("while scanning an %s" % name, start_mark,
                    "expected alphabetic or numeric character, but found %r"
                    % ch.encode('utf-8'), self.get_mark())
        value = self.prefix(length)
        self.forward(length)
        ch = self.peek()
        if ch not in u'\0 \t\r\n\x85\u2028\u2029?:,]}%@`':
            raise ScannerError("while scanning an %s" % name, start_mark,
                    "expected alphabetic or numeric character, but found %r"
                    % ch.encode('utf-8'), self.get_mark())
        end_mark = self.get_mark()
        return TokenClass(value, start_mark, end_mark)

class Loader12(Reader, Scanner12, Parser, Composer, Constructor, Resolver):
    ''' This is a version of the loader that uses Scanner12. '''
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner12.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)

# PKM2014 - uses SafeConstructor instead of Constructor. This should make no
# difference, because "Is it YAML?" only gets as far as the composition stage,
# but - well: it reduces the risk of something bad happening.

#        Constructor.__init__(self)
        SafeConstructor.__init__(self)
        Resolver.__init__(self)

# Here ends the YAML update.

STATE_GET = 0; # Used only for get requests.
STATE_POST_YES = 1; # Used for successful post (when YAML is parsed).
STATE_POST_NO = 2; # Used for failed posts
COMMENTSTR = \
  "# This is a comment. Your YAML stream is good, but contains no documents. "

@csrf_protect
def index(request):
    yamlcanon = u""; # YAML in canonical form.
    yamlerror = u"" # YAML error messages.
    yamloriginal = u"" # The original text. Shown only for error messages.
    yamlstate = STATE_GET # The state of the page.
    ourmap = {"yamlstate": yamlstate, "yamlcanon": yamlcanon,
        "yamlerror": yamlerror, "yamloriginal": yamloriginal};
    if request.method == 'GET':
        pass; # Everything we need is in ourmap already.
    else: # POST request.
        try:
            ourtarget = request.POST.get("yamlarea");
            composition = compose_all(ourtarget, Loader12);
            yamlcanon = serialize_all(composition,
                canonical=True, allow_unicode=True);
            ourmap["yamlstate"] = STATE_POST_YES;
            if len(yamlcanon) == 0:
                ourmap["yamlcanon"] = COMMENTSTR
            else:
                ourmap["yamlcanon"] = yamlcanon;

# PKM2014 - AttributeErrors are now caught.

        except (YAMLError, AttributeError) as e:
            ourmap["yamlstate"] = STATE_POST_NO;
            ourmap["yamlerror"] = e.__str__();
            ourmap["yamloriginal"] = ourtarget;
    return render(request, 'isityaml/isityaml.html', ourmap)
