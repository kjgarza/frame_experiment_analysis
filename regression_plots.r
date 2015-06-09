library(ggplot2)


plot_odds<-function(x, title=NULL){
tmp<-data.frame(exp(cbind(OR =coef(x), confint(x))))
odds<-tmp[-1,]
names(odds)<-c('OR', 'lower', 'upper')
odds$vars<-row.names(odds)
ticks<-c(seq(0.1,1,by=0.1),seq(0,10,by=1),seq(10,100,by=10))

ggplot(odds, aes(y= OR, x = reorder(vars, OR))) +
geom_point() +
geom_errorbar(aes(ymin=lower, ymax=upper), width=.2) +
scale_y_log10() +
geom_hline(yintercept = 1, linetype=2) +
coord_flip() +
labs(title = title, x = 'Variables', y = 'OR') 
}