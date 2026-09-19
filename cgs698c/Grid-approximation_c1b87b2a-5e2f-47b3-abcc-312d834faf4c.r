# data: 9, 6, 8, 5
x <- c(9,6,8,5)
n <- 10
# x_i ~ Binomial(theta,10)
# theta ~ Beta(2,2)

# Analytically derived
# theta|x ~ Beta(2+sum(x),2+sum(10-x))

post_samples <- rbeta(10000,2+sum(x),2+sum(n-x))
hist(post_samples)

# Grid approximation
theta_grid <- seq(from=0,to=1,length=100000)
likelihood <- dbinom(sum(x),size=n*4,prob = theta_grid)
plot(theta_grid,likelihood)
prior <- dbeta(theta_grid,2,2)
unnorm_posterior <- likelihood*prior

post_samples_ga <- sample(theta_grid,
                          size=10000,
                          prob = unnorm_posterior)

hist(post_samples_ga)

samples <- rbind(
  data.frame(method=rep("Analytical",10000),
             posterior=post_samples),
  data.frame(method=rep("Grid Approximation",10000),
             posterior=post_samples_ga))

library(ggplot2)
ggplot(samples,aes(x=posterior,group=method,color=method))+
  geom_density(size=1.3)

quantile(post_samples,probs = c(.025,.975))
quantile(post_samples_ga,probs = c(.025,.975))

########################################




