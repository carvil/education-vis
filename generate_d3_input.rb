#!/usr/bin/env ruby

require 'csv'
require 'json'

raw_data = CSV.read(ARGV[0], headers: true)

rendering_apps = raw_data.map { |row| row['rendering_app'] }.uniq
document_types = raw_data.map { |row| row['document_type'] }.uniq
links = []

rendering_apps.each_with_index do |app_name, i|
  rows = raw_data.select {|row| row['rendering_app'] == app_name}
  doc_types_present = rows.map{|row| row['document_type']}.uniq

  doc_types_present.each do |document_type|
    filtered_rows = rows.select {|row| row['document_type'] == document_type}
    j = document_types.find_index(document_type)
    links << [app_name, document_type, filtered_rows.count]
  end
end

puts JSON.pretty_generate(links)
