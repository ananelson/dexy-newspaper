library(rjson)

data = read.csv("dexy--sim-output.csv")

strategy.counts <- table(list(strategy=data$strategy, step=data$step))

pdf(file="dexy--strategy-counts.pdf", width=5.5, height=5.5)
barplot(
    strategy.counts,
    legend.text = TRUE,
    border=NA,
    args.legend = pairlist(bty='n')
)
dev.off()

last.period = subset(data, data$step==max(data$step))

pdf(file="dexy--hist.pdf", width=5.5, height=5.5)
hist(last.period$points, main="", ylab="Number of Agents", xlab="Final Score")
dev.off()

max_points_in_last_period <- max(last.period$points)
