require(likert)
require(reshape)
library(RColorBrewer)
library(plyr)
library(ggplot2)


graph_with_who <- function(DFdataUnderCite, DFdataUnderShare, title=NULL) {
    ## setup
    ##cc <-brewer.pal(4, "PuBu")
    cc <-colorRampPalette(brewer.pal(11, 'PuBu'))(30)
    cc <- cc[c(27,19,13,9)]
    likertLabels<- c("private", "collaborators", "stakeholders", "public")
    ##format data
    dAlcite <- data.frame(DFdataUnderCite)
    dAshare <- data.frame(DFdataUnderShare)
    myList5 <- list(dAshare, dAlcite)
    junto <-do.call(rbind.fill, myList5)
    djunto <- data.frame(junto)
    mydata2 <- junto
    DFG <- lapply(mydata2, factor, levels = likertLabels)
    #DFG <- lapply(mydata2, factor, levels = 1:5)
    print(DFG)
    d <- data.frame(DFG)
    ##plot
    df24<-likert(d)
    s<- plot(df24, color=cc,text.size=4, plot.percents=TRUE,  plot.percents.center=FALSE,plot.percent.neutral=FALSE,plot.percent.low=FALSE, plot.percent.high=FALSE, ordered=FALSE, group.order=names(d), include.histogram=TRUE)
    s


    s<- plot(df24, color=cc,text.size=9,plot.percents=TRUE, plot.percent.neutral=FALSE,plot.percent.low=FALSE, plot.percent.high=FALSE, ordered=FALSE, group.order=names(d))
    s + theme(text = element_text(size=34), plot.title = element_text(lineheight=.8, face="bold", size=30)) + ggtitle(title)
    ggsave("~/plt_ef.png", width = 16, height = 9, dpi = 120)

}


graph_when <- function(DFdataUnderCiteWhento, DFdataUnderShareWhento, title=NULL ){
#    cc <-brewer.pal(4, "RdPu")

    cc <-colorRampPalette(brewer.pal(11, 'RdPu'))(30)
    cc <- cc[c(9,13,19,27)]


    tempLabels<- c("6m", "1y","3y", "10y")

    dAlcite <- data.frame(DFdataUnderCiteWhento)
    dAshare <- data.frame(DFdataUnderShareWhento)
    myList5 <- list(dAshare, dAlcite)
    junto <-do.call(rbind.fill, myList5)
    djunto <- data.frame(junto)
    mydata2 <- junto
    DFG <- lapply(mydata2, factor, levels = tempLabels)

    d <- data.frame(DFG)
    df24<-likert(d)
    s<- plot(df24, color=cc,text.size=4,plot.percents=TRUE, plot.percent.neutral=FALSE,plot.percent.low=FALSE, plot.percent.high=FALSE, ordered=FALSE, group.order=names(d), include.histogram=TRUE)
    s
    s<- plot(df24, color=cc,text.size=9,plot.percents=TRUE, plot.percent.neutral=FALSE,plot.percent.low=FALSE, plot.percent.high=FALSE, ordered=FALSE, group.order=names(d))
    s + theme(text = element_text(size=34), plot.title = element_text(lineheight=.8, face="bold", size=30)) + ggtitle(title)
    ggsave("~/plt_scc.png", width = 16, height = 9, dpi = 120)
}


graph_usability<-function(DFdataUnderCiteEase, DFdataUnderShareEase, DFdataUnderCiteSupport, DFdataUnderShareSupport, DFdataUnderCiteTime, DFdataUnderShareTime){
    ##cc <-brewer.pal(4, "PuBu")
    cc <-colorRampPalette(brewer.pal(11, 'PuBu'))(30)
    cc <- cc[c(9,13,19,27)]
    likertLabels<- c("Strongly Disagree", "Disagree", "Neither", "Agree", "Strongly Agree")

    dProduct_Gain_support <- data.frame(DFdataUnderCiteSupport)
    dProduct_Loss_support <- data.frame(DFdataUnderShareSupport)
    dProduct_Gain_ease <- data.frame(DFdataUnderCiteEase)
    dProduct_Loss_ease <- data.frame(DFdataUnderShareEase)
    dProduct_Gain_time <- data.frame(DFdataUnderCiteTime)
    dProduct_Loss_time <- data.frame(DFdataUnderShareTime)

    myList5 <- list(dProduct_Gain_support,dProduct_Loss_support,dProduct_Gain_ease,dProduct_Loss_ease,dProduct_Gain_time,dProduct_Loss_time)
    junto <-do.call(rbind.fill, myList5)
    djunto <- data.frame(junto)
    mydata2 <- junto
    #   DFG2 <- lapply(mydata2, factor, labels = likertLabels)
    #   DFG <- lapply(DFG2, factor, levels = likertLabels)

    DFG <- lapply(mydata2, factor, levels = likertLabels)
    d <- data.frame(DFG)
    df24<-likert(d)
    s<- plot(df24, color=cc,text.size=4, center=3, plot.percent.low=TRUE, plot.percent.high=TRUE, ordered=FALSE, group.order=names(d))

    s
#    s<- plot(df24, color=cc,text.size=10, center=3, plot.percent.low=TRUE, plot.percent.high=TRUE, ordered=FALSE, group.order=names(d))
#    s + theme(text = element_text(size=34))
#    ggsave("~/plt_usability.png", width = 16, height = 9, dpi = 120)

}



graph_linkert<-function(DFdataUnderCiteRegret, DFdataUnderShareRegret){
    ##cc <-brewer.pal(4, "PuBu")
    cc <-colorRampPalette(brewer.pal(11, 'PuBu'))(30)
    cc <- cc[c(9,13,19,27)]

      likertLabels<- c("Strongly Disagree", "Disagree", "Neither", "Agree", "Strongly Agree")

       dAlcite <- data.frame(DFdataUnderCiteRegret)
       dAshare <- data.frame(DFdataUnderShareRegret)

       myList5 <- list(dAshare, dAlcite)
       junto <-do.call(rbind.fill, myList5)
       djunto <- data.frame(junto)
       mydata2 <- junto

    DFG <- lapply(mydata2, factor, levels = likertLabels)
    d <- data.frame(DFG)
    df24<-likert(d)
    s<- plot(df24, color=cc, text.size=4,center=3,plot.percent.low=TRUE, plot.percent.neutral=TRUE,plot.percent.high=TRUE, ordered=FALSE, group.order=names(d))
    s
    s + theme(text = element_text(size=34))
    ggsave("~/plt_linkert.png", width = 16, height = 9, dpi = 120)

}