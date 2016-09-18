Templo Server
=============

TemSer is a templating engine, containg also a built-in server.

The built-in server works like a plain normal web server, 
except that it interprets `*.tmd` files to serve dynamic content.
TMD is short for "Templated Markdown".

A typical template file is made of two parts. First, a header like:
```
<?
foo = path/to/local/file.json
bar = https://whatever.com/some/REST/api
?>
```
which is used to fetch some data as JSON, that can be used later in the template.
Then, the template itself, which is a combination of markdown and handlebars.

```
Example Title
=============

Listing the names in "foo":
{{/each foo}}
   - {{firstname}} {{lastname}}
{{/each}}
```

Would result in:

```
<h1>...</h1>
...
```

This piece is itself rendered in a customizable theme.




Install
-------

Requires python 3.5+

`pip install temser`

Usage
-----

```python
import temser

ts = temser.TemSer(root='directory/to/serve')
ts.run(debug=True, host='0.0.0.0', port=80)
```

> TODO: make also a command line like:
>
> `python temser.py -p 8080 -d directory/to/serve`

Instead of acting as a server, you can also use the template engine independently:

```
import temser

ts = temser.TemSer(root='directory/to/serve')
result = ts.render('file/path', foo='Arbitrary', bar='Args')
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

<b style="color:red">TODO: use relative imports!</b>

### Custom hooks


By default, `<? foo = url/to/some/json/data ?>` or `<? include ... ?>` will only
fetch content/data from local files or per HTTP from remote or local URLs.

If you want to fetch custom content/data directly, "hooks" can be used:
```
def countdown(path, parsed):
    n = int(path.strip('/'))
    res = list(range(n,0,-1))
    if parsed:
        return res
    else:
        return json.dumps(res)

ts = temser.TemSer()
ts.hooks['@countdown'] = countdown
```

Using a template `countdown.tml` like this:
```
<? nums = @countdown/$n ?>
<html>
	<body>
		{{#nums}} {{.}} {{/nums}}
	</body>
</html>
```

And calling `http://.../countdown.tml?n=5` would result in:

```
<html>
	<body>
		 5  4  3  2  1
	</body>
</html>
```

TODO
----
- $ escaping!