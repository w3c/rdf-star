#!/usr/bin/env python
from pathlib import Path
import json

def main():
    dir = Path(__file__).parent
    for i in [
        ["semantics", "manifest.jsonld"],
        #["sparql", "manifest.jsonld"],
    ]:
        make_html(dir.joinpath(*i))

def make_html(jsonld: Path):
    dir = jsonld.parent
    html = dir.joinpath(jsonld.stem + '.html')
    print(html)
    with jsonld.open() as f:
        manifest = json.load(f)
    with html.open('w') as out:
        out.write("<!DOCTYPE html>\n")
        out.write('<meta charset="UTF-8">')
        out.write(STYLE)
        out.write(f"<title>{jsonld.stem}</title>\n")
        out.write(f"<h1>{jsonld.stem}</h1>\n")
        out.write(f'<p>Generated from <a href="{jsonld.name}">{jsonld.name}</a></p>')
        if 'comment' in manifest:
            out.write(f"<p>{manifest['comment']}</p>\n")

        include = manifest.get('include')
        if include:
            out.write('<p><strong>Includes:</strong></p>\n<ul class="inclueded">\n')
            for url in include:
                make_html(dir.joinpath(*url.split('/')))
                name = url.replace('.jsonld', '')
                url = url.replace('.jsonld', '.html')
                out.write(f'<li><a href="{url}">{name}</a>\n')
            out.write("</ul>\n")

        entries = manifest['entries']
        if not entries:
            return
        out.write('<p><strong>Entries:</strong></p>\n<ul class="entries">\n')
        for (i, entry) in enumerate(entries):
            eid = entry.get('@id', f"#{jsonld.name}_entry{i}")
            name = entry.get('name', eid[1:])
            approval = entry['approval'].lower()
            out.write(f'<li class="{approval}"><a href="{eid}">{name}</a>\n')
            # store computed values for the next loop
            entry['@id'] = eid
            entry['name'] = name
            # 
        out.write("</ul>\n")

        for entry in entries:
            eid = entry['@id']
            name = entry['name']
            if eid[1:] != name:
                print(f"{eid}'s name does not match id")
            approval = entry['approval'].lower()
            out.write(f'<section id="{eid[1:]}" class="entry {approval}">\n')
            out.write(f'<h2>{name} <a href="{eid}">🔗</a></h2>\n')
            out.write('<table class="properties">\n')
            out.write(f'<tr class="status"><th>status:</th><td>{approval}</td>\n')
            out.write(f'<tr class="type"><th>type:</th><td>{readable_type(entry)}</td>\n')
            if 'entailmentRegime' in entry:
                out.write(f'<tr class="regime"><th>regime:</th><td>{entry["entailmentRegime"]}</td>\n')
            recognized = entry.get('recognizedDatatypes')
            if recognized:
                out.write(f'<tr class="recognized"><th>recognizing:</th><td>{" ".join(recognized)}</td>\n')
            unrecognized = entry.get('unrecognizedDatatypes')
            if unrecognized:
                out.write(f'<tr class="unrecognized"><th>ignoring:</th><td>{" ".join(unrecognized)}</td>\n')
            out.write("</table>\n")

            write_file(out, entry['action'], dir)
            out.write(f"<div>{result_message(entry)}</div>\n")
            if entry['result'] is False:
                out.write("<div>a contradiction</div>")
            else:
                write_file(out, entry['result'], dir)
            if 'comment' in entry:
                out.write(f"<p>{entry['comment']}</p>\n")
            out.write("</section>")


def readable_type(entry: dict) -> str:
    typ = entry['@type']
    return {
        'PositiveEntailmentTest': 'positive entailment test',
        'NegativeEntailmentTest': 'negative entailment test',
    }.get(typ, typ)

def write_file(out, relative_url, current_dir):
    out.write(f'<div><code><a href="{relative_url}">{relative_url}</a></code></div>\n')
    try:
        with current_dir.joinpath(*relative_url.split('/')).open() as f:
            out.write("<pre>\n")
            quoted = f.read().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            out.write(quoted)
    except Exception as e:
        msg = "(problem rendering file) %s\n" % e
        out.write(msg)
        print(f"{relative_url}:", msg)
    finally:
        out.write("</pre>\n")

def result_message(entry: dict) -> str:
    typ = entry['@type']
    msg = {
        'PositiveEntailmentTest': 'MUST entail',
        'NegativeEntailmentTest': 'MUST NOT entail',
    }.get(typ)
    if msg is None:
        if typ.startswith('Netagitve'):
            msg = 'MUST NOT result into'
        else:
            msg = 'MUST result into'
    return msg

STYLE = '''
<style>
    .included a, .entries a {
        text-decoration: none;
    }

    .included a:hover, .entries a:hover {
        text-decoration: underline;
    }

    .entries .rejected {
        text-decoration: line-through red;
    }

    .entries .approved::after {
        content: "✓";
    }

    .entry h2 a {
        text-decoration: none;
    }

    .approved tr.status td {
        color: darkGreen;
    }

    .proposed tr.status td {
        color: orange;
    }

    .rejected tr.status td {
        color: red;
    }

    tr.recognized td, tr.unrecognized td {
        font-family: monospace;
    }

    pre {
        border: thin solid black;
        background-color: lightYellow;
        padding: .6em 1em;
    }
</style>
''' 

main()
