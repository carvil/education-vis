# NOTE: to be run in a console in content tagger

hierarchy = {}
content_id = 'c58fdadd-7743-46d6-9629-90bb3ccc4ef0'

def guidance_document_types
  [
    'answer',
    'business_support',
    'business_support_finder',
    'calculator',
    'calendar',
    'completed_transaction',
    'contact',
    'detailed_guidance',
    'detailed_guide',
    'form',
    'guidance',
    'guide',
    'hmrc_manual',
    'hmrc_manual_section',
    'html_publication',
    'local_transaction',
    'manual',
    'manual_section',
    'place',
    'programme',
    'service_manual_guide',
    'service_manual_homepage',
    'service_manual_service_standard',
    'service_manual_service_toolkit',
    'service_manual_topic',
    'simple_smart_answer',
    'smart_answer',
    'statutory_guidance',
    'transaction',
    'travel_advice',
    'travel_advice_index',
  ]
end

def make_it(hierarchy, content_id)
  taxon = Taxonomy::BuildTaxon.call(content_id: content_id)
  tagged_content = Services.publishing_api.get_linked_items(
    content_id,
    link_type: "taxons",
    fields: %w(base_path document_type)
  )
  tagged_guidance_content = tagged_content.select do |content|
    guidance_document_types.include?(content['document_type'])
  end
  hierarchy[:name] = taxon.title
  puts taxon.title
  parents = taxon.parent_taxons.map do |parent|
    Taxonomy::BuildTaxon.call(content_id: parent)
  end
  hierarchy[:parents] = parents.map(&:title)
  taxonomy = Taxonomy::ExpandedTaxonomy.new(content_id)
  taxonomy.build_child_expansion
  hierarchy[:children] = []
  hierarchy[:number_of_tagged_content] = tagged_content.count
  hierarchy[:number_of_tagged_guidance_content] = tagged_guidance_content.count

  taxonomy.child_expansion.children.each do |child|
    hierarchy[:children] << make_it({}, child.content_id)
  end

  hierarchy
end

tree = make_it(hierarchy, content_id)
puts tree.to_json
