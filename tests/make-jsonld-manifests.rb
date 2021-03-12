#!/usr/bin/env ruby
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
}.map {|p| File.expand_path(p)}.
  each do |dir|
  Dir.chdir(dir) do |path|
    RDF::Turtle::Reader.open('manifest.ttl', base_uri: "#{path}/manifest") do |ttl_reader|
      local_ctx['@context']['@base'] = "#{path}/manifest"
      JSON::LD::API.fromRdf(ttl_reader) do |expanded|
        framed = JSON::LD::API.frame(expanded, local_ctx, expanded: true)
        framed['@context']['@base'] = 'manifest' # no file-extension
        puts "Create #{path}/manifest.jsonld"
        File.open('manifest.jsonld', "w") do |file|
          file.write(framed.to_json(JSON::LD::JSON_STATE))
        end
      end
    end
  end
end

