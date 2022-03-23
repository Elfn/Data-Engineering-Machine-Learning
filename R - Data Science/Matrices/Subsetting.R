

x <- c("a","b","c","d")
x
x[c(1,4)]

Games
el1 <- Games[c(1,10),1:10]
Games[c(1,10),]
el2 <- Games[1:3,]
el2
el <- Games[2,1:2,drop=F]  # drop
el 
is.matrix(el2)
is.vector(el2)

is.matrix(el1)
is.vector(el1)

is.matrix(el)
is.vector(el)
