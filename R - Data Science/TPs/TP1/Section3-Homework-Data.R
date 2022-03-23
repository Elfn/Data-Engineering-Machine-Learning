#Data
revenue <- c(14574.49, 7606.46, 8611.41, 9175.41, 8058.65, 8105.44, 11496.28, 9766.09, 10305.32, 14379.96, 10713.97, 15433.50)
expenses <- c(12051.82, 5695.07, 12319.20, 12089.72, 8658.57, 840.20, 3285.73, 5821.12, 6976.93, 16618.61, 10054.37, 3803.96)

# Hint 1
#round()
#mean()
#max()
#min()
#append()
#reset()

length <- seq(1 : length(revenue))
length
#Solution

# Profit for each month
rprofit <- revenue - expenses
rprofit
# Profit after tax rate of 30%
profitAfterTax <- rprofit - (rprofit * 0.3)
profitAfterTax

# Profit margin for each months
profitMargin <- profitAfterTax / revenue
profitMargin

# Profit mean
profitMean <- mean(rprofit)
profitMean

# Good months
new_good_value <- NULL
for(j in length){
   if(profitAfterTax[j] > profitMean){
     new_good_value <- append(new_good_value,j)
   }
}

goodMonths <- month.name[new_good_value]
goodMonths

# Bad months
new_bad_value <- NULL
for(j in length){
  if(profitAfterTax[j] < profitMean){
    new_bad_value <- append(new_bad_value,j)
  }
}
badMonths <- month.name[new_bad_value]
badMonths

# Best month
bestMonth <- month.name[max(new_good_value)]
bestMonth

# Worst month
worstMonth <- month.name[min(new_bad_value)]
worstMonth

