Template Examples
=================

Home page
---------
```html
<html>
	<head>
		<? include theme.tpl ?>
	</head>
	<body>
		<? include header.tpl ?>
		
		<p>bla bla bla</p>
		
		<? include footer.tpl ?>
	</body>
</html>
```

Movies search results
---------------------

```html
<? movies = @data/movies?search=$search&in=$category ?>
{{#movies}}
<div>
	<img src="{{image_url}}" style="float:left;"/>
	<h3>{{title}}</h3>
	<p>{{description}}</p>
</div>
{{/movies}}
```
