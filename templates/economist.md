# {{ title }}

_{{ subtitle }}_

![{{ image.alt }}]({{ image.source }})
{% for item in content %}
{{ item.rich }}
{% endfor %}
&nbsp;

```
Posted on {{ postdate }}
Archived on {{ getdate }}

Original copy at {{ url }}
```
