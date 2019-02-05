import slideshow
import markdown

style = """<style>

body,td {font-family: Arial;
    font-size:1.2em;
}
    
div.page{
    padding: 4em;
}

#cours {
    position: relative;
    margin-left:10%;
    margin-right:10%;
    width:80%;
    margin-top:20px;
    padding-top:5px;
    padding-left:40px;
    padding-right:40px;
    font-size:1em;
    background-color:#FFF;
}

#cours h1 {
    background-color:#4479D4;
    padding-top:10px;
    padding-left:20px;
    padding-right:20px;
    padding-bottom:10px;
    color:#FFFFFF;
    border-radius: 10px 10px;
}
#cours h1 code {
    color: #FFF;
}

#cours pre.marked{
    background-color:#222;
    color: #fff;
    font-size: 1em;
    margin-left:40px;
    margin-right:40px;
    padding: 7px;
    border-style: solid;
    border-color: #888;
    border-width: 1px;
    width: 50em;
}

.python-console{
    background-color:#000;
    font-family: "Consolas", "Courier New", "Monospace";
    color: #fff;
    margin-left:40px;
    margin-right:40px;
    padding: 7px;
    border-style: solid;
    border-color: #888;
    border-width: 1px;
    width: 50em;
}
.python-console span.python-prompt{
    color: #ff6;
}
.python-console span.python-string{
    color: #aaf;
}
.python-console span.python-comment{
    color: #0f0;
}
.python-console span.python-keyword{
    color: #f66;
}
.python-console span.python-builtin{
    color: #f69;
}

.python{
    background-color:#eee;
    font-family: "Consolas", "Courier New", "Monospace";
    font-size: 1em;
    margin-left: 40px;
    margin-right: 40px;
    padding: 7px;
    border-style: solid;
    border-color: #000;
    border-width: 1px;
    border-radius: 5px;
    width: auto;
}

.python span.python-string{
    color: blue;
}
.python span.python-comment{
    color: green;
}
.python span.python-keyword{
    color: purple;
}
.python span.python-builtin{
    color: #963;
}

.console{
    background-color:#000;
    font-family: "Consolas", "Courier New", "Monospace";
    color: #fff;
    margin-left:40px;
    margin-right:40px;
    padding: 7px;
    border-style: solid;
    border-color: #888;
    border-width: 1px;
    width: 50em;
}
.raw{
    font-size: 0.9em;
    font-weight:bold;
    margin-left:40px;
    margin-right:40px;
    padding: 7px;
    width: auto;
}

code {
    color: #339;
    font-size:1.2em;
    font-weight:bold;
}
em{
    color: #339;
    font-family:courier;
}
strong{
    color: #339;
    font-family:courier;
}

#footer {
    text-align: center;
    position:absolute;
    bottom:25px;
    width:90%;
    font-weight:bold;
    color:#7AA2E4;
    padding:5px;
}
#timeline {
    text-align: center;
    position: absolute;
    bottom: 5px;
    width: 90%;
    font-weight: bold;
    color: #FFB740;
    background-color: #7AA2E4;
    height: 10px;
    padding-left: 5px;
    padding-right: 5px;
}
#tl_pos{
    text-align: center;
    position:absolute;
    bottom:0px;
    width:4px;
    font-weight:bold;
    background-color:#FFF;
    height:10px;
    left:0px;
}

</style>
"""

class Slideshow:
    
    def __init__(self, path):
        with open(path, encoding="utf-8") as fobj:
            self.src = src = fobj.read()
        self.title = ''
        self.show_page_num = False
        
        # table of contents : matches matter with page number
        self.contents = []
        
        # directives for the document
        while src.startswith('@'):
            line_end = src.find('\n')
            key,value = src[:line_end].split(' ', 1)
            if key=='@title':
                self.title = value
            elif key=='@pagenum':
                self.show_page_num = True
            elif key=="@index":
                self.contents.append([value, 0])
            src = src[line_end + 1:]

        self.pages = []
        lines = []
        for line in src.split('\n'):
            if line.startswith('../..'):
                self.pages.append('\n'.join(lines))
                lines = []
            elif line.startswith('@pause'):
                continue
            elif line.startswith('@index'):
                self.contents.append([line.split(' ', 1)[1], len(self.pages)])
            else:
                lines.append(line)

        if lines:
            self.pages.append('\n'.join(lines))

    def make_html(self):
        res = ('<!doctype html>\n<html>\n<head>\n<meta charset="utf-8">\n'
            + style + '</head>\n<body>')

        for num, page in enumerate(self.pages):
            html = '<div class="page">\n' + markdown.mark(page)[0] + "\n</div>"
            
            html += '\n<p style="page-break-after:always;"></p>'
            
            res += html
            
            """
            for elt in zone.get(selector='.python'):
                src = elt.text.strip()
                width = max(len(line) for line in src.split('\n'))
                width = max(width, 30)
                # replace element content by highlighted code
                elt.html = highlight.highlight(src).html
                elt.style.width = '%sem' %int(0.7*width)
                elt.bind('click', run_code)
        
            for elt in zone.get(selector='.python-console'):
                src = elt.text.strip()
                lines = src.split('\n')
                result = ''
                py = ''
                py_starts = []
                for line in lines:
                    if line.startswith('>>>') or line.startswith('...'):
                        py += line[4:]+'\n'
                        py_starts.append('<span class="python-prompt">{}</span>'.format(line[:3]))
                    else:
                        if py:
                            colored = highlight.highlight(py).html
                            colored_lines = colored.split('\n')
                            if result:
                                result += '\n'
                            result += '\n'.join(start+' '+line
                                for (start, line) in zip(py_starts, colored_lines))
                            py = ''
                            py_starts = []
                        result += '\n' + line
                if py:
                    colored = highlight.highlight(py).html
                    colored_lines = colored.split('\n')
                    if result:
                        result += '\n'
                    result += '\n'.join(start+' '+line
                        for (start, line) in zip(py_starts, colored_lines))
                    py = ''
                    py_starts = []
        
                elt.html = result
            """
        return res + '</body>\n</html>'

path = "cours_python.pss"
slides = Slideshow(path)

with open("printable.html", "w", encoding="utf-8") as out:
    out.write(slides.make_html())

