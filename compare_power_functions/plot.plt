set terminal png large size 1600,1200
set output "heatmap_square_multiply.png"
set title "Power using Square and multiply algorithm"
set colorbox user size .03, .6 noborder

set ticslevel 0
set samples 25, 25
set isosamples 50, 50
set label font "Arial,40"
set xlabel "x" offset 2, -2, 0  font "Arial,20"
set ylabel "n" offset 1, -2, 0 font "Arial,20"
set zlabel "time(ms)" offset -10, 0, 0 rotate by 90 font "Arial,20"
set pm3d implicit at s
splot 'data.csv' using 1:2:($3/1000000) with lines

set output "heatmap_loop.png"
set title "Power using loop"
splot 'data.csv' using 1:2:($4/1000000) with lines