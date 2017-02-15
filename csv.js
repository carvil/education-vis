#! /usr/bin/env node

// run this on the command line to output a CSV of content per taxon to populate
// this spreadsheet: https://docs.google.com/spreadsheets/d/1LmeshaUZIda_K9Lz5c_TNs4MIIC-0GYdX-CwvlgNjvY/edit#gid=1003528232
//
// node csv.js > ./output/taxonomy.csv

var treeData = require("./output/taxonomy.json");

function traverseTree(taxon) {
    console.log("\""+taxon.name+"\", "+taxon.number_of_tagged_content+", "+taxon.number_of_tagged_guidance_content);
    for (var i in taxon.children) {
      traverseTree(taxon.children[i]);
    }
}

function parentDepth(parent) {
  var count = 0;
  console.log(parent.name);
  for (i in parent.parents) {
    var this_parent = parent.parents[i];
    console.dir(this_parent);
    count++;
    parentDepth(this_parent);
  }

  // return count;
}

console.log("Name, Tagged Content, Tagged Guidance Content");
traverseTree(treeData);
