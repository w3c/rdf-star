This is a collection of individual
[EARL reports](https://www.w3.org/TR/EARL10-Schema/) for
test subjects claiming JSON-LD processor conformance.

The consolidated report is saved to `index.html` generated
using the
[earl-report Ruby gem](https://rubygems.org/gems/earl-report).
Run it as follows:

```sh
$ gem install earl-report rdf-turtle json-ld rdf-ordered-repo
$ rm -f manifests.nt && (cd ..; rake reports/manifests.nt)
$ earl-report --format json -o earl.jsonld *.ttl
$ earl-report --json --format html --template template.haml -o index.html earl.jsonld
```
