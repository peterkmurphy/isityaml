from django.template import Context, RequestContext, loader
from django.http import HttpResponse, Http404, HttpResponseRedirect;
from django.shortcuts import render_to_response;
from django.core.context_processors import csrf

# The following code updates the scanner so that it can deal with Unicode
# anchors and aliases.

from yaml.scanner import Scanner, ScannerError;
from yaml.tokens import *;
from yaml.reader import *
from yaml.parser import *
from yaml.composer import *
from yaml.constructor import *
from yaml.resolver import *
from yaml.error import YAMLError;
import yaml;

class Scanner12(Scanner):
    ''' This is an updated version of the YAML scanner, so that it handles 1.2
    adequately.
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
#        while u'0' <= ch <= u'9' or u'A' <= ch <= u'Z' or u'a' <= ch <= u'z'    \
#                or ch in u'-_':
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
        Constructor.__init__(self)
        Resolver.__init__(self)

# Here ends the YAML update.

STATE_GET = 0; # Used only for get requests.
STATE_POST_YES = 1; # Used for successful post (when YAML is parsed).
STATE_POST_NO = 2; # Used for failed pos


def index(request):
    canon = u""; # YAML in canonical form.
    error = u"" # YAML error messages.
    original = u"" # The original text. Shown only for error messages.
    state = STATE_GET # The state of the page.
    ourmap = {"state": state, "canon": canon, "error": error, "original": original};
    t = loader.get_template('isityaml/index.html')
    if request.method == 'GET':
        ourmap.update(csrf(request));
        c = Context(ourmap);
    else: # POST request.
        try:
            ourtarget = request.POST.get("yamlarea");
            composition = yaml.compose_all(ourtarget, Loader12);
            canon = yaml.serialize_all(composition, 
                canonical=True, allow_unicode=True);
            ourmap["state"] = STATE_POST_YES;
            if len(canon) == 0:
                ourmap["canon"] = "# This is a comment. Your YAML stream is good, but it contains no documents. "
            else:
                ourmap["canon"] = canon;
        except YAMLError, e:
            ourmap["state"] = STATE_POST_NO;
            ourmap["error"] = e.__str__();
            ourmap["original"] = ourtarget;
        ourmap.update(csrf(request));
        c = RequestContext(request, ourmap);
    
    return HttpResponse(t.render(c))    



