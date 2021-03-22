#!/usr/bin/env ruby
require "bundler/setup"
require 'json/ld'
require 'rdf/turtle'
require 'rdf/isomorphic'
require 'rdf/ordered_repo'
require 'rdf/normalize'

man_dir = File.expand_path("")
local_ctx = JSON.parse(File.read("#{man_dir}/manifest-context.jsonld"))
%w{
  nt/syntax
  semantics
  sparql/syntax
  sparql/eval
  turtle/syntax
  turtle/eval
}.each do |path|
  dir = File.expand_path(path)
  base = "https://w3c.github.io/rdf-star/tests/#{path}/"
  ttl_graph = RDF::OrderedRepo.load("#{dir}/manifest.ttl", base_uri: base)
  local_ctx['@context']['@base'] = base
  local_ctx['@context']['trs'] = "https://w3c.github.io/rdf-star/tests/#{path}#"
  JSON::LD::Writer.open("#{dir}/manifest.jsonld",
    format: :jsonld, 
    frame: local_ctx,
    context: local_ctx,
    base_uri: base) {|writer| writer << ttl_graph}

  # Validate that the two graphs say the same thing.
  jsonld_graph = RDF::OrderedRepo.load("#{dir}/manifest.jsonld", base_uri: base)
  if !jsonld_graph.isomorphic?(ttl_graph)
    STDERR.puts "expected #{dir}/manifest.jsonld to be isomorphic with expected #{dir}/manifest.ttl"
    STDERR.puts "\nFrom Turtle:\n#{ttl_graph.dump(:normalize)}"
    STDERR.puts "\nFrom JSON-LD:\n#{jsonld_graph.dump(:normalize)}"
    exit(1)
  end
end

