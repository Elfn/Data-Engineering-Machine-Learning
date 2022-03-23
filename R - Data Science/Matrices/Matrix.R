

# matrix
my.data <- 1:10
my.data
A <- matrix(my.data,2,5)
A
A[2,5]

B <- matrix(my.data,2,5,byrow=T)
B
B[2,5]


# rbind

r1 <- c("A","B","C")   
r2 <- c("E","R","G")
r3 <- c("Z","Y","Q")
C <- rbind(r1,r2,r3)
C
C[3,3]

# cbind

D <- cbind(r1,r2,r3)
D <- Colnames('l1','l2','l3')
D <- Rownames('r1','r2','r3')


