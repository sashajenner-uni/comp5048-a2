#!/usr/bin/env Rscript
# What sorts of “trends” can you observe regarding some types of mobile devices
# becoming obsolete and being taken over by different/new types?
# trends data analysis of the data
USAGE = 'usage: ./trends.R DATA'

library(ggplot2)
library(readxl)
library(stringr)
library(plotly)
library(htmlwidgets)

# check args
args = commandArgs(TRUE)
if (length(args) != 1) {
	stop(USAGE)
}

# read file
path = args[1]
df = read_excel(path)

# change colnames
colnames(df) = c("model",
		 "release_date",
		 "release_year",
		 "model_id",
		 "ram",
		 "storage",
		 "cpu_clock",
		 "display_diagonal",
		 "display_width",
		 "display_length",
		 "width",
		 "length",
		 "depth",
		 "volume",
		 "mass",
		 "pixel_density",
		 "producer")

# grab producer
df$producer = word(df$model, 1)
df$release_year = as.integer(df$release_year)
df$aspect_ratio = df$length/df$width
df$display_aspect_ratio = df$display_length/df$display_width

# slight increase in mass of some but not a general trend
#ggplot(df) +
#	geom_point(aes(x=release_year, y=mass))

# increase in pixel density
ggplot(df) +
	geom_point(aes(x=release_year, y=pixel_density))

# more ram in the top phones
ggplot(df) +
	geom_point(aes(x=release_year, y=ram))

# more models being designed
ggplot(df) +
	geom_histogram(aes(x=release_year))

# more cpu clock
ggplot(df) +
	geom_point(aes(x=release_year, y=cpu_clock))

str(df)

# width height
#plot = df %>%
#	group_by(release_year) %>%
#	do(p=plot_ly(., x=~width, y=~length,
#		     #frame=~release_year,
#		     type='scatter', mode='markers',
#	       hovertext=~model, hoverinfo='text') %>%
#	layout(shapes = list(list(
#	    type = "line",
#	    x0 = 0,
#	    x1 = 1,
#	    xref = "x",
#	    y0 = 0,
#	    y1 = 1,
#	    yref = "y",
#	    line = list(color = "black")
#	  )),
#	       xaxis=list(title='Width'),
#	       yaxis=list(title='Length')
#	)
#	#%>%
#	#animation_opts(1000, easing='elastic', redraw = FALSE) %>%
#	#animation_slider(currentvalue = list(prefix = 'Release Year: '))
#	) %>%
#	subplot(nrows=5, shareX=TRUE, shareY=TRUE)
#saveWidget(plot, 'Rplots.html')

#plot = plot_ly(df, x=~width, y=~length,
#		     frame=~release_year,
#		     type='scatter', mode='markers',
#	       hovertext=~model, hoverinfo='text') %>%
#	layout(shapes = list(list(
#	    type = "line",
#	    x0 = 0,
#	    x1 = 1,
#	    xref = "x",
#	    y0 = 0,
#	    y1 = 1,
#	    yref = "y",
#	    line = list(color = "black")
#	  )),
#	       xaxis=list(title='Width'),
#	       yaxis=list(title='Length')
#	) %>%
#	animation_opts(1000, easing='elastic', redraw = FALSE) %>%
#	animation_slider(currentvalue = list(prefix = 'Release Year: '))
#saveWidget(plot, 'length-width-year.html')

#plot = plot_ly(df, x=~width, y=~length,
#		     type='scatter', mode='markers',
#	       hovertext=~model, hoverinfo='text',
#	       marker=list(color=~release_year,
#			   colorscale='Viridis',
#			   colorbar=list(title='Release Year'))
#	       ) %>%
#	layout(shapes = list(list(
#	    type = "line",
#	    x0 = 0,
#	    x1 = 1,
#	    xref = "x",
#	    y0 = 0,
#	    y1 = 1,
#	    yref = "y",
#	    line = list(color = "black")
#	  )),
#	       xaxis=list(title='Width'),
#	       yaxis=list(title='Length')
#	)
#saveWidget(plot, 'length-width-cyear.html')

#plot = plot_ly(df, x=~width, y=~length,
#		     type='scatter', mode='markers',
#	       hovertext=~model, hoverinfo='text'
#	       ) %>%
#	layout(shapes = list(list(
#	    type = "line",
#	    x0 = 0,
#	    x1 = 1,
#	    xref = "x",
#	    y0 = 0,
#	    y1 = 1,
#	    yref = "y",
#	    line = list(color = "black")
#	  )),
#	       xaxis=list(title='Width'),
#	       yaxis=list(title='Length')
#	)
#saveWidget(plot, 'length-width.html')

#plot = plot_ly(df[df$aspect_ratio > 1,],
#	       x=~sqrt(length^2+width^2),
#	       y=~sqrt(display_length^2+display_width^2),
#	       #y=~display_diagonal,
#		     type='scatter', mode='markers',
#	       hovertext=~model, hoverinfo='text',
#	       marker=list(color=~cpu_clock,
#			   #colorscale='Viridis',
#			   colorbar=list(title='CPU Clock'))
#	       ) %>%
#	layout(xaxis=list(title='Diagonal'),
#	       yaxis=list(title='Display Diagonal')
#	)
#saveWidget(plot, 'ddiag-diag-ccpu.html')

plot = plot_ly(df[df$aspect_ratio > 1,],
	       x=~aspect_ratio,
	       y=~display_aspect_ratio,
		     type='scatter', mode='markers',
	       hovertext=~model, hoverinfo='text',
	       marker=list(color=~cpu_clock,
			   #colorscale='Viridis',
			   colorbar=list(title='CPU Clock'))
	       ) %>%
	layout(shapes = list(list(
	    type = "line",
	    x0 = 0.3,
	    x1 = 4,
	    xref = "x",
	    y0 = 0,
	    y1 = 3.7,
	    yref = "y",
	    line = list(color = "black"))),
		xaxis=list(title='Aspect Ratio'),
	       yaxis=list(title='Display Aspect Ratio')
	)
saveWidget(plot, 'Rplots.html')
