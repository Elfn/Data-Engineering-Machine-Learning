

fVector <- c(12,13,14,15)
fVector
# Check if an object is numeric
is.numeric(fVector)

is.integer(fVector)

is.double(fVector)

sVector <- c(2L,5L,0L)
is.integer(sVector)

tVector <- c("a","B23","Hello")
is.character(tVector)
is.array(tVector)

#Sequence
x <- seq(1,15,4)
x
#OR
1:15

#Replicate
v <- c(20,80) # combine 
rep(v,7) # Replicate combined items

w <- c("a","b","c","d","e","f")

w[-1]
w[-3]
w[-6]
v <- w[-(4:6)]
v
v[1:2]
v[c(-1,-3)]
