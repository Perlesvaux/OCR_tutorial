from re import findall
from sys import argv


# def format_code(file_string, rgx_matches, color_markup="", css_color=""): #string = format_code(document, rgx_findall, "JS***", "pnk")
#     for element in rgx_matches:
#         if element != "":
#             file_string=file_string.replace(element, f"""<code style="color:{css_color};">{element.strip(color_markup).replace("<", "&lt;").replace(">", "&gt;")}</code>""")
#     return file_string

#color{"matches": findall(rgx, document), "markup": "PNK***", "css":"pink"}
def format_code(dump, color, template=""):
    for item in color.get("matches"):
        element=item.strip(color.get("markup")).replace("<", "&lt;").replace(">", "&gt;")
        dump=dump.replace(item, template.format(element=element, css=color.get("css")))
    return dump


if len(argv) == 2:

    with open(argv[1], 'r') as fp:

        document= fp.read()

        commentary           = "##.*"
        tutorial             = ".+(?=##)"    #.+(?= \/\/)
        link                 = "\bhttps?://\S+\b"
        # pnk, pnk_mu, pnk_css = "PNK\*\*\*.*\n", "PNK***", "pink"
        # blu, blu_mu, blu_css = "BLU\*\*\*.*\n", "BLU***", "lightskyblue"
        code_tag_template    = """<code style="color:{css};">{element}</code>"""
        # code_tag_template    = """<code style="color:{css};">{element.strip(markup).replace("<", "&lt;").replace(">", "&gt;")}</code>"""

        commentaries = findall(commentary, document)
        tutorials    = findall(tutorial, document)
        links        = findall(link, document)
        # pnks         = findall(pnk, document)
        # blus         = findall(blu, document)

        pink = {"matches":findall("PNK\*\*\*.*\n", document), "markup":"PNK***", "css":"pink"}
        blue = {"matches":findall("BLU\*\*\*.*\n", document), "markup":"BLU***", "css":"lightskyblue"}
        comm = {"matches":findall("##.*"         , document), "markup":""      , "css":""}

        if len(commentaries) != len(tutorials):
            print("Error: commentaries and tutorials aren't the same length!")
            exit(1)

        #adding hyperlinks!
        for l in links:
            if l != "":
                document=document.replace(l, f"""<a href="{l}">{l}</a>""")

        document = format_code(document, pink, code_tag_template)
        document = format_code(document, blue, code_tag_template)
        document = format_code(document, comm)


        # document = format_code(document, pnks, pnk_mu, pnk_css)

        # document = format_code(document, blus, blu_mu, blu_css)


        #Now that commentaries can be retrieved from a list, let's remove them from the document's body
        # for x in commentaries:
        #     if x != "":
        #         document=document.replace(x, "")


        for i, tuto in enumerate(tutorials):
            if tuto != "" and commentaries[i] != "":
                document=document.replace(tuto, f"""<span class="commented" data-toggle="popover"    data-content="{commentaries[i].replace('##', '')}">{tuto.strip()}</span>""")


        bootstrap = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
"""

        css = """<style>
body{
    background-color: #405d27;
}
  span{
    color:#82b74b;
  }

  pre{
    margin: 0 auto;
    width: fit-content;
    color:#fff;
    background:#3e4444;
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
        <body><pre><code>
{document}
            </code></pre>
            {JS}
        </body>
        </html>
        """

        print(template)
        # print(len(tutorials), len(commentaries))
        # print(pnks)
