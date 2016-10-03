Title
=====

Section
-------

### Sub-section

Websites can be written in plain HTML or in "Markdown".
If you are not familiar with it yet, Markdown allows you to write using an easy-to-read, easy-to-write plain text format that will be automatically converted in plain HTML.

Find more details about markdown here:

https://daringfireball.net/projects/markdown/syntax

<table>
    <tr>
        <td style="bg-color:#aff">You</td>
		<td></td>
		<td style="bg-color:#faf">also</td>
		<td></td>
		<td style="bg-color:#ffa">HTML</td>
		<td></td>
    </tr>
	<tr>
		<td></td>
        <td style="bg-color:#ccf">can</td>
		<td></td>
		<td style="bg-color:#fcc">use</td>
		<td></td>
		<td style="bg-color:#cfc">too!</td>
    </tr>
</table>

### Including content

Sometimes, there is content that you want to include in several pages, like headers, footers, or other UI parts.
Instead of duplicating the markup code, you can simply `include` them, like this:

<? include /made_with_templo.tml ?>

### Handling data

You can also import data...

<? people = https://randomuser.me/api/?results=10&format=PrettyJSON&inc=name,picture ?>

...and use it in a template, like this:

<table>
	{{#each people.results}}
	<tr>
		<td><img src="{{picture.thumbnail}}" ></td>
		<td>{{name.first}} {{name.last}}</td>
	</tr>
	{{/each}}
</table>

