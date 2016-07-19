Mustache Template Server
========================

Two kind of file extensions:

- *.tml -> templated HTML
- *.tmd -> templated Markdown

Specify data sources:

```html
<? foo = url/to/some/json/data ?>
<!-- Now, the data identified by "foo" can be used in the template -->
<html>
<body>
	<ul>
		{{#foo}}
		<li>{{bar}}</li>
		{{/foo}}
	</ul>
</body>
</html>
```

Include other files:

```html
<? foo = url/to/some/json/data ?>
<!-- Now, the data identified by "foo" can be used in the template -->
<html>
<body>
	<? include header.tpl ?>
	
	<p>Listing:</p>
	{{#foo}}
		<? include item.tpl ?>
	{{/foo}}
	
	<? include footer.tpl ?>
</body>
</html>
```

### Flow of execution

1. fetch all includes (possibly caching the result)
2. replace $args with their argument values
3. fetch data sources
4. apply templating

***Remarks about included templates:***

- must be local
- must be of same type (.tml or .tmd)
- can be nested/recursive
- ~~can use {{mustache}} nor $arg as part of their name~~
- ~~can add data sources~~
- ~~cannot redefine data sources differently~~


Steps
=====

1. fetch all includes (possibly caching the result)
2. replace $args with their argument values
3. fetch data sources
4. apply templating
