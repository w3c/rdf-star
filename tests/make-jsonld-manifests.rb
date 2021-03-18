#!/usr/bin/env ruby
require "bundler/setup"
require 'json/ld'
require 'rdf/turtle'

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
  base = "https://w3c.github.io/rdf-star/tests/#{path}/manifest"
  RDF::Turtle::Reader.open("#{dir}/manifest.ttl") do |ttl_reader|
    local_ctx['@context']['@base'] = base
    JSON::LD::Writer.open("#{dir}/manifest.jsonld",
                          frame: local_ctx,
                          context: local_ctx,
                          base_uri: base
    ) do |jsonld_writer|
      puts "#{dir}/manifest.jsonld"
      jsonld_writer << ttl_reader
    end
  end
end

