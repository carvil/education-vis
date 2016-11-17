# Rendering apps for education content

## Setup

Install the python dependencies with:

```
pip install -r requirements.txt
```

There are no external ruby dependencies apart from the standard library.

## Preparing the data

In order to generate the data for this diagram, follow the steps below.

### Fetch content from GOV.UK's content store

With a file containing links to GOV.UK content like
[this](input/education_urls.csv), fetch the remaining content like this:

```
python fetch_govuk_data.py input/education_urls.csv output/education_data.csv
```

This will perform API calls to GOV.UK and download the required data. Then, run
the following in order to transform that data into something D3.js can use:

```
ruby generate_d3_input.rb output/education_data.csv > output/education_data.json
```

The index page will then pick up the latest version of that file and use it to
render, assuming the output file has the same name.
