# {{ title }}

_{{ subtitle }}_

[Cover Image]({{ image.source }})

&nbsp;

{% for item in content %}
{{ item.text }}
{% if not loop.last %}
&nbsp;
{% endif %}
{% endfor %}

&nbsp;

---
^(Posted on {{ postdate }})

^(Archived on {{ getdate }})

^(Original copy) ^[here]({{ url }})