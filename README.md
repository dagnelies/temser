Mustache Template Server
========================

It works like a plain normal web server, except that it interprets `*.tml` files to serve dynamic content.
TML is short for "Templated Markup Language" and is an extension of mustache templates.

Install
-------

Requires python 3

`pip install temser`



Usage
-----


### ...as a standalone server

TODO

`python temser.py -p 8080 -d directory/to/serve`

### ...only the templating library

```
import barmaid
maid = barmaid.Barmaid(root='some/dir')
rendered = barmaid.mix('file/path', foo='Arbitrary', bar='Args')
```


Templates
---------

### Data

```html
<!-- Let's import some data to be used in the template -->
<? foo = url/to/some/json/data ?>

<html>
	<body>
		<ul>
			<!-- Usual mustache stuff -->
			{{#foo}}
			<li>{{bar}}</li>
			{{/foo}}
		</ul>
	</body>
</html>
```

### URL parameters


```html
<!-- The $... come directly from the URL's query parameters (and post params) -->
<? foo = data/$some/$arg?param=$foobar ?>

<html>
	<body>
		<ul>
			<!-- Usual mustache stuff -->
			{{#foo}}
			<li>{{bar}}</li>
			{{/foo}}
		</ul>
	</body>
</html>
```

### Content

It is possible to include other files in a template:

```html
<html>
	<body>
		<? include /fragments/header.tpl ?>
		
		<p>Listing:</p>
		{{#foo}}
			<? include /fragments/item.tpl ?>
		{{/foo}}
		
		<? include /fragments/footer.tpl ?>
	</body>
</html>
```

***Remarks about included templates:***

1. Includes are the first thing to be resolved, a bit like pre-processing.
As such, they cannot contain `{{mustache}}` nor `$arg` as part of their URL.

2. Although included fragments can include their own data sources, they cannot redefine
existing ones with a different URL.


### Custom hooks


By default, `<? foo = url/to/some/json/data ?>` or `<? include ... ?>` will only
fetch content/data from local files or per HTTP from remote or local URLs.

If you want to fetch custom content/data directly, "hooks" can be used:
```

```

---------

Standalone server
-----------------

### Config

Same as canister + json.config

```
{
	"theme": {
		"url": "http://whatever/theme",
		"params": {
			"title": "Fancy",
			"menu": [{
				"label": "Home",
				"url": "/index.tml"
			}]
		}
}

```

### Themes