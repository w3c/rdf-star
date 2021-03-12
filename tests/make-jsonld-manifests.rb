#!/usr/bin/env ruby
require 'json/ld'
require 'rdf/turtle'

man_dir = File.expand_path("")
%w{
  nt/syntax
  semantics
  sparql/syntax
  sparql/eval
  turtle/syntax
  turtle/eval
}.map {|p| File.expand_path(p)}.
  each do |dir|
  Dir.chdir(dir) do |path|
    RDF::Turtle::Reader.open('manifest.ttl', base_uri: path) do |ttl_reader|
      JSON::LD::Writer.open('manifest.jsonld',
                            frame: "#{man_dir}/manifest-context.jsonld",
                            context: "#{man_dir}/manifest-context.jsonld",
                            base_uri: path
      ) do |jsonld_writer|
        puts "Create #{path}/manifest.jsonld"
        jsonld_writer << ttl_reader
      end
    end
  end
end

