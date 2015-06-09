library('plyr')
source('css_stats.R')


exp <- read.csv('dummy', stringsAsFactors=F)


exp_filtered <- exp[exp$honest == 'on',]

y <- exp_filtered[exp_filtered$treatment == 'TREATMENT',]

y <- y[c("baseline", "measure_1")]


t.test(y$baseline, y$measure_1, paired=TRUE)

#
#y$c_sum <- rowSums(y)
#y$d_dif <-
#
#yc_mean <- mean(y$c_sum)
#yd_mean <- mean(y$d_dif)





x <- exp_filtered[exp_filtered$treatment == 'CONTROL',]

x <- x[c("baseline", "measure_1")]


x$c_sum <- rowSums(x)



