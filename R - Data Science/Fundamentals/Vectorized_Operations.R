

x <- rnorm(5)
x

# R specific programming loop
for(i in x){
  print(i)
}

print(x[1])
print(x[2])
print(x[3])

# Conventional programming loop
for(j in 1:5){
 print(x[i])
}

N <- 100
a <- c(1:3)
b <- c(1:3)
a
b

# Vectorized approach
c <- a * b
c

# De-Vectorized approach
dp <- rep(NA,3)
dp
for(j in 1:3){
  dp[j] <- a[j] * b[j]
}
dp

