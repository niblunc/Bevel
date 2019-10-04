


ph.data<-read.csv("Bevel/ana/beta/punish_corr_matrix.csv", header=FALSE) 
rwd.data<-read.csv("Bevel/ana/beta/reward_corr_matrix.csv", header=FALSE) 


rwd.corr<-cor(rwd.data)
ph.corr<-cor(ph.data)

#head(rwd.corr,2)
#head(round(ph.corr,2))

library(corrplot)
library(RColorBrewer)

corrplot(rwd.corr, method="circle")
corrplot(ph.corr, method="circle")
corrplot(rwd.corr,  type="upper", order="hclust")

corrplot(rwd.corr, type="upper", order="hclust",  tl.col="black", tl.srt=45,
         col=brewer.pal(n=8, name="PuOr"))

corrplot(ph.corr, type="upper", order="hclust",  tl.col="black", tl.srt=45,
         col=brewer.pal(n=8, name="PuOr"))

corrplot(rwd.corr, type="upper", order="hclust", col=c("black", "white"),
         bg="lightblue", tl.col="black", tl.srt=45)
corrplot(ph.corr, type="upper", order="hclust", col=c("black", "white"),
         bg="lightblue",  tl.col="black", tl.srt=45)


cortest.normal(ph.corr,rwd.corr,n1=1000,n2=1000,fisher =TRUE) #The Steiger test
cortest.jennrich(ph.corr,rwd.corr,n1=100,n2=10000) # The Jennrich test
cortest.mat(ph.corr,rwd.corr,n1=1000,n2=1000)  #twice the degrees of freedom as the Jennrich


cor.mtest <- function(mat, ...) {
  mat <- as.matrix(mat)
  n <- ncol(mat)
  p.mat<- matrix(NA, n, n)
  diag(p.mat) <- 0
  for (i in 1:(n - 1)) {
    for (j in (i + 1):n) {
      tmp <- cor.test(mat[, i], mat[, j], ...)
      p.mat[i, j] <- p.mat[j, i] <- tmp$p.value
    }
  }
  colnames(p.mat) <- rownames(p.mat) <- colnames(mat)
  p.mat
}
# matrix of the p-value of the correlation
ph.mat <- cor.mtest(ph.data)
head(ph.mat[, 1:5])

rwd.mat <- cor.mtest(rwd.data)
head(rwd.mat[, 1:5])
