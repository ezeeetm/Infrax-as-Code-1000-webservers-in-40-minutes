http://matplotlib.org/examples/mplot3d/bars3d_demo.html


from bokeh.plotting import figure, output_file, show

# prepare some data
x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
y0 = [0.1, 0, 1.0, 0, 2.0, 0, 3.0]
y1 = [10**i for i in x]
y2 = [10**(i**2) for i in x]

# output to static HTML file
output_file("log_lines.html")

# create a new plot
p = figure(
   tools="pan,box_zoom,reset,save",
   y_axis_type="log", y_range=[0.001, 10**11], title="log axis example",
   x_axis_label='sections', y_axis_label='particles'
)

# add some renderers
p.circle(x, y0, legend="fdsa", color="red", alpha=0.5, line_color=None, size=6)
p.circle(x, y1, legend="jhg", color="firebrick", alpha=0.5, line_color=None, size=6)
p.circle(x, y2, legend="uyhg", color="olive", alpha=0.5, line_color=None, size=6)

# show the results
show(p)
