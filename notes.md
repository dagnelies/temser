### would it be nice to include local/remote *content*?

By *content*, the rendered result of a template is meant.
It turns out that both are not so interesting for different reasons.

The issue with remote content is latency.
If the server calls remote content and waits before responding, 
it would cause large delays and workload.

Local content isn't very interesting either since the same can be achieved by rendering the fragment directly.

**Therefore, no, **content** cannot be included, only template fragments**

### Would it be nice to have parametrized includes?

Like `<? include vehicle/$type.tml ?>`

Yes, that would be cool! ...but what if the included fragment also have a $var?
Then it couldn't be replaced ...which is sucky again. It's not very consistent
that first level fragments can be parametrized but others not.

Or we need a replace/fetch/replace/fetch mechanism ...also an option.

What about `<? include items/{{type}}.tml ?>`?

Well, then you would need to fetch the data, then render it, then fetch the fragments,
then render it, then fetch the fragments... Sounds complicated. Not good.

**Both options rejected. Raw files include.**

### Would it be nice if args could have default values?

Yes, that would be cool!

Like:
```
<? default $arg value ?>
```
or
```
$foo ?= default-value
```
?

...but it would add extra syntax

**Let's do it in a later stage to avoid complexity**

### Would people expect order to play a role?

Like:
```html
<?
$foo foo-default-value
$bar bar-default-value
foo = @data/items/$foo
bar = @data/items?search=$bar
include stuff.tml
?>
<html>
...
```

**Redefines forbidden!**

### What happens if...

- include contains `http://`, `{{mustache}}`, `$arg`, `?arg=...` => ERROR!
- fragment contains data imports... just collect them normally, plain cut'n'paste
- $arg is missing? => ERROR!

### Force standalone tags?

It's quite difficult to parse/render, because it can't simply be done on the fly.

Should we enforce that:
```html
<?
foo = /@data/items/$foo
bar = /@data/items?search=$bar
include stuff.tml
?>
<html>
...
```
Is written as:
```html
<? foo = /@data/items/$foo ?>
<? bar = /@data/items?search=$bar ?>
<? include stuff.tml ?>
<html>
...
```

Yeah, let's do that!


### What about caching?

For usual HTTP request, the timestamp of the file has to be compared.

For the templates, it's a bit more tricky since the cached result depends on:

- all included template fragments
- the arguments (not only the file)
- the data, and its last modification date
 
**Current way:** do not cache ...heck, that's how php does it.
