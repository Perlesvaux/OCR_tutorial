from re import findall
from sys import argv

# @java([\s\S]*?)@javaend
def format_code(dump, lang):
    template = """<pre><code class="language-{language}">{txt}</code></pre>"""
    for item in lang.matches:
        txt=item.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        dump=dump.replace(item, template.format(txt=txt, language=lang.language))
    return dump.replace(f"@{lang.language}end", "").replace(f"@{lang.language}", "")


class lang:
    def __init__(self, doc, language):
        self.language = language
        self.rgx = """@{language}([\s\S]*?)@{language}end""".format(language=language)
        # self.eachrow = findall(self.rgx, doc)[0].split("\n")[1:-1]
        self.matches = findall(self.rgx, doc)
        # self.matches = ["\n".join(x.split("\n")[1:-1]) for x in self.all]

"""@{language}([\s\S]*?)@{language}end"""

if len(argv) == 2:

    with open(argv[1], 'r') as fp:

        document= fp.read()

        javacode   = lang(document, "java")
        bashcode   = lang(document, "bash")
        markupcode = lang(document, "markup")

        document = format_code(document, javacode)
        document = format_code(document, bashcode)
        document = format_code(document, markupcode)



        bootstrap = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
<link href="prism.css" rel="stylesheet" />
"""

        css = """<style>
body{
    background-color: #313636;
}
  span{
    color:#82b74b;
  }

  h2{
    color:olive;
  }

  pre{
    margin: 0 auto;
    width: fit-content;
    color:#fff;
    background:#252828;
    white-space: pre-wrap;
    border-style: none;
  }

  .commented{
    width:fit-content;
    text-shadow: .1px .1px black;
  }

  .commented:hover{
    background-color:#82b74b;
    color:black;
    cursor: help;
  }

  /* Popover */
  .popover {
    border: 2px inset white;
    border-radius: 25px;
  }
  /* Popover Header */
  .popover-title {
    background-color: #73AD21;
    color: #FFFFFF;
    font-size: 28px;
    text-align:center;
    border-radius: 25px;
  }
  /* Popover Body */
  .popover-content {
    color:#fff;
    background:#405d27;
    padding: 25px;
    width:fit-content;
    border-radius: 25px;
  }
  /* Popover Arrow */
  .arrow {
    border-right-color: white !important;
  }
  </style>"""

        JS = """<script>
$(document).ready(function(){
  $('[data-toggle="popover"]').popover();
});
</script>
  """
        template = f"""<!DOCTYPE html>
        <head>
           {bootstrap}
           {css}
           <title>{argv[1]}</title>
        </head>
        <body>
        <pre>
{document}
        </pre>
            {JS}
  	    <script src="prism.js"></script>
        </body>
        </html>
        """

        print(template)
        print(javacode.rgx)
        print(javacode.matches)
        # print(link.matches)
        # print(href.matches)
        # print(len(tutorials), len(commentaries))
        # print(pnks)
