extract.clmm <- function(model, include.thresholds = TRUE, include.aic = TRUE,
    include.bic = TRUE, include.loglik = TRUE, oddsratios = TRUE, conf.level= 0.95, include.nobs = TRUE, ...) {
  s <- summary(model, ...)

  tab <- s$coefficients
  thresh <- tab[rownames(tab) %in% names(s$alpha), ]
  threshold.names <- rownames(thresh)
  threshold.coef <- thresh[, 1]
  threshold.se <- thresh[, 2]
  threshold.pval <- thresh[, 4]
  beta <- tab[rownames(tab) %in% names(s$beta), ]
  beta.names <- rownames(beta)
  beta.coef <- beta[, 1]
  beta.se <- beta[, 2]
  beta.pval <- beta[, 4]



  if (include.thresholds == TRUE) {
    names <- c(beta.names, threshold.names)
    coef <- c(beta.coef, threshold.coef)
    se <- c(beta.se, threshold.se)
    pval <- c(beta.pval, threshold.pval)
  } else {
    names <- beta.names
    coef <- beta.coef
    se <- beta.se
    pval <- beta.pval
  }

  n <- nobs(model)
  lik <- logLik(model)[1]
  aic <- AIC(model)
  bic <- BIC(model)
  gof <- numeric()
  gof.names <- character()
  gof.decimal <- logical()
  if (include.aic == TRUE) {
    gof <- c(gof, aic)
    gof.names <- c(gof.names, "AIC")
    gof.decimal <- c(gof.decimal, TRUE)
  }
  if (include.bic == TRUE) {
    gof <- c(gof, bic)
    gof.names <- c(gof.names, "BIC")
    gof.decimal <- c(gof.decimal, TRUE)
  }
  if (include.loglik == TRUE) {
    gof <- c(gof, lik)
    gof.names <- c(gof.names, "Log Likelihood")
    gof.decimal <- c(gof.decimal, TRUE)
  }
  if (include.nobs == TRUE) {
    gof <- c(gof, n)
    gof.names <- c(gof.names, "Num.\ obs.")
    gof.decimal <- c(gof.decimal, FALSE)
  }


    if (oddsratios == TRUE) {
 #old way
### the problem is that the order of the ci is different to the order of coeff
 #       remove.rows <- grep("|", names, fixed=TRUE)
 #       coefficient.names <- names[-remove.rows]
 #       coefficients <- exp(coef)
 #       coefficients <- coefficients[-remove.rows]
 #       ci <- exp(confint.default(model, level = conf.level))
 #       ci.low <- ci[, 1]
 #       ci.low <- ci.low[-remove.rows]
 #       ci.up <- ci[, 2]
 #       ci.up <- ci.up[-remove.rows]

        ss = (exp(cbind(OR =coef(model), confint(model, level = conf.level))))
        dd =as.data.frame(as.table(ss))
        remove.rows <- grep("|", dd$Var1, fixed=TRUE)
        no_intercepts <- dd[-remove.rows,]
        coefficients = no_intercepts[no_intercepts$Var2 == 'OR',]$Freq
        coefficient.names = as.character(no_intercepts[no_intercepts$Var2 == 'OR',]$Var1)
        ci.low = no_intercepts[no_intercepts$Var2 == '2.5 %',]$Freq
        ci.up  = no_intercepts[no_intercepts$Var2 == '97.5 %',]$Freq


        tr <- createTexreg(
          coef.names = coefficient.names,
          coef = coefficients,
          ci.low = ci.low,
          ci.up = ci.up,
          gof.names = gof.names,
          gof = gof,
          gof.decimal = gof.decimal
        )
    }
    else {


      tr <- createTexreg(
          coef.names = names,
          coef = coef,
          se = se,
          pvalues = pval,
          gof.names = gof.names,
          gof = gof,
          gof.decimal = gof.decimal
      )
   }
  return(tr)
}

setMethod("extract", signature = className("clmm", "ordinal"),
    definition = extract.clmm)