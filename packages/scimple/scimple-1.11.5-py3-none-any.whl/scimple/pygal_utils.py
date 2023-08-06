# #####
# PYGAL
# #####

from IPython.display import display, HTML
html_pygal="""
<!DOCTYPE html>
<html>
  <head>
  <script type="text/javascript" src="http://kozea.github.com/pygal.js/latest/pygal-tooltips.min.js"></script>
    <!-- ... -->
  </head>
  <body>
    <figure>
      <!-- Pygal render() result: -->
      {a}
      <!-- End of Pygal render() result: -->
    </figure>
  </body>
</html>
"""
fig_pygal="""
<figure>
  <!-- Pygal render() result: -->
  {a}
  <!-- End of Pygal render() result: -->
</figure>
"""
def show(chart):
    plot_html = html_pygal.format(a=chart.render(is_unicode=True))
    display(HTML(plot_html))
def to_html(chart):
    plot_html = html_pygal.format(a=chart.render(is_unicode=True))
    return plot_html
def to_html_fig(chart):
    plot_html_fig = fig_pygal.format(a=chart.render(is_unicode=True))
    return plot_html_fig
def to_svg(chart):
    return chart.render(is_unicode=True)
