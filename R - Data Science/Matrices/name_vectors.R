

# Naming Matrix Dimensions 1
temp.vec <- rep(c("A","B","C"), each=3)

temp.vec

bb <- matrix(temp.vec, 3, 3)
bb
rownames(bb) <- c("l1","l2","l3")
bb
colnames(bb) <- c("r1","r2","r3")
bb
