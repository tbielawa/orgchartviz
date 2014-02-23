# OrgChartViz

Create GraphViz files of your org chart. Pulls data from LDAP.

## Library Requirements

* `argparse` or Python 2.6+
* `python-ldap`


# Usage

Note that these commands could take a while to run, depending on how
large your org structure is.

## Generate Dot File

Generate a dot file called `my_org_chart.dot`:

    $ ./gen_chart.py --uri=ldap://ldap.company.com --search-base=dc=company,dc=com --start-filter=uid=somebossid --manager-attr=manager --out my_org_chart.dot

You could instead print the dot file to your console directly by
setting `--out` to `-` (a single hyphen character)

## Generate an Image

Example of how to use the graphviz `circo` tool to generate a PNG file called `org_chart.png` from `my_org_chart.dot`.

    $ circo -Tpng -o org_chart.png my_org_chart.dot

You could also use the `dot` tool to generate a standard directed
graph. With larger orgs though this will generally give less readable
results than using `circo`.

## (Optional) Resize the Image

If you have a really large org `circo` or `dot` will generate very
tall and wide images (I'm talking up to or over 30,000 pixels
wide/tall). Some graphics editing tools can't handle images this
large! If you have the **ImageMagic** package installed you can use
the `convert` command to shrink your images.

For example, in my org (using `circo`) my image got pretty large:

    $ identify org_chart.png
    org_chart.png PNG 13805x12302 13805x12302+0+0 8-bit DirectClass 6.834MB 0.000u 0:00.000

That's **13805** by **12302** pixels!

### Resize the Image

Use the `convert` command. The general syntax is: `convert INPUT_IMAGE
-resize (NEWxDIMENSIONS|%) OUTPUT_IMAGE`.

I'm going to reduce this image to 10% of it's original
dimensions. We'll set `-resize 10%` to accomplish this:

    $ convert org_chart.png -resize 10% org_chart_resized.png
    $ identify org_chart_resized.png
    org_chart_resized.png PNG 1381x1230 1381x1230+0+0 8-bit PseudoClass 180c 149KB 0.000u 0:00.000

Now it's only **1381** by **1230** pixels. Much smaller.
