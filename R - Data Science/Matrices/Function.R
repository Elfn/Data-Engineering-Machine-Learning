# Create function

#Data <- MinutesPlayed[c(1,2,9),]

myplot <- function(data,rows){
  
  Data <- data[rows,,drop=F]
  matplot(t(Data),type="b", pch=15:18, col=c(1:4,6))
  legend("bottomleft",inset=0.01,legend = Players[rows], col=c(1:4,6),pch=15:18,horiz = F)
  
}

myplot(FieldGoals/FieldGoalAttempts,1:10)
myplot(FieldGoals/Games,1:10)
myplot(FieldGoalAttempts/Games,1:10)
myplot(Points/Games,1:10)
myplot(Points/FieldGoals,1:10)
