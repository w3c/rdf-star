# Preliminary implementations of RDF-star #

| Implementation | [SA] | [PG] | Notes | Documentation |
|:---------------|:----:|:----:|:------|:-------------:
| AllegroGraph   |      |  +   | in the works | https://lists.w3.org/Archives/Public/public-rdf-star/2020Aug/0021.html
| AnzoGraph      |      |  x   | | https://docs.cambridgesemantics.com/anzograph/v2.2/userdoc/lpgs.htm?Highlight=rdf
| BlazeGraph     |      |  x   | | https://github.com/blazegraph/database/wiki/Reification_Done_Right
| Corese         |      |  x   | | http://ns.inria.fr/sparql-extension/rdfstar.html
| GraphDB        |  x   |      | | http://graphdb.ontotext.com/documentation/9.2/free/devhub/rdf-sparql-star.html
| Jena           |  x   |      | | https://jena.apache.org/documentation/rdfstar/
| EYE            |  x   |  x   | SA is the default. PG can be emulated by adding rules | https://github.com/josd/eye/
| rdf4j          |  x   |      | | https://rdf4j.org/documentation/programming/rdfstar/
| rdfjs/N3.js    |  x   |  +   | PG may become configurable soon | https://github.com/rdfjs/data-model-spec/pull/165
| RubyRDF        |  x   |      | | https://github.com/ruby-rdf/rdf#rdf-rdfstar
| Stardog        |      |  x   | | https://www.stardog.com/docs/#_edge_properties

### key ###
| symbol | meaning |
|:-:|:-:|
| x | supported |
| + | partially supported or planned |
      
Source: https://lists.w3.org/Archives/Public/public-rdf-star/2020Aug/0026.html

[SA]: https://w3c.github.io/rdf-star/rdf-star-cg-spec.html#sa-mode-and-pg-mode
[PG]: https://w3c.github.io/rdf-star/rdf-star-cg-spec.html#sa-mode-and-pg-mode
