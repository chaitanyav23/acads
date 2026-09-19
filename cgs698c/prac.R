if (!require(ggplot2, quietly = TRUE)) {
    install.packages("ggplot2", repos = "https://cran.r-project.org/")
    library(ggplot2)
}

library(reshape2)
library(dplyr)

set.seed(123)
y <- rnorm(50, mean = 300, sd = 10)
hist(y)
sigma <- 10
mu <- seq(from=200,to=400,by=0.05)
likelihoods <- data.frame(mu=mu)
likelihoods$lkl <- NA
for(i in 1:length(mu)){
    likelihoods$lkl[i] <- prod(dnorm(y,mu[i],sd=10))
}
ggplot(likelihoods,aes(x=mu,y=lkl))+geom_line(linewidth=1,color="blue")+
    theme_bw()+xlab(expression(mu))+ylab("Likelihood")


ggplot(likelihoods,aes(x=mu,y=lkl))+geom_line(linewidth=1,color="blue")+
theme_bw()+xlab(expression(mu))+ylab("Likelihood")+
scale_x_continuous(limits = c(275,325))
geom_vline(xintercept = mean(y), color = "red", linetype = "dashed")

likelihoods$prior_density <- NA
for(i in 1:length(mu)){
likelihoods$prior_density[i] <- dnorm(mu[i],mean=350,sd=10)
}
ggplot(likelihoods,aes(x=mu,y=prior_density))+geom_line(linewidth=1,color="orange")+
theme_bw()+xlab(expression(mu))+ylab("Prior density")


df.lkl_prior <- melt(likelihoods,id=c("mu"))
df.lkl_prior$variable <- ifelse(df.lkl_prior$variable=="lkl","Likelihood","Prior density")
ggplot(df.lkl_prior,aes(x=mu,y=value,color=variable))+geom_line(linewidth=1)+
    theme_bw()+xlab(expression(mu))+ylab("")+
    scale_x_continuous(limits = c(250,400))+
    facet_wrap(~variable,scales = "free_y",ncol = 1)+
    scale_color_manual(values = c("blue","orange"))

# Sample from the priors
mu <- rnorm(2000,300,50)
sigma <- rep(10,2000)
# Create a dataframe to store the simulated data
# One way is to simply generate a datapoint
# corresponding to each value of mu
xsim <- rep(NA,length(mu))
for(i in 1:length(mu)){
    xsim[i]<- rnorm(1,mu[i],sd=sigma[i])
}
hist(xsim)

# But we want to make the simulated data
# as comparable as we can to the observed data

# Our observed data y contained 50 observations
# So, we should simulate samples containing 50 observations
# for each value of mu
# Thus, we need to generate 2000 samples
# each containing N observations (datapoints)
N <- 50 # I will keep it same as the number of observations in our data y
df.sim <- data.frame(sample = rep(1:2000,each=N),mu=rep(mu,each=N),sigma=rep(sigma,each=N),observation = rep(1:N,2000))
df.sim$ysim <- NA
for(i in 1:length(mu)){
    df.sim[df.sim$sample==i,]$ysim <- rnorm(N,mean=mu[i],sd=sigma[i])
}
hist(df.sim$ysim)

# ggplot(subset(df.sim,sample<10),aes(x=ysim))+geom_histogram()+facet_wrap(~sample)

ggplot(subset(df.sim,sample<10),aes(x=ysim))+geom_histogram()+ facet_wrap(~sample)+ geom_vline(xintercept = mean(y),color="red",linetype="dashed",linewidth=1)

df.sim.summary <- df.sim %>% group_by(sample) %>%
    summarise(meanRT=mean(ysim),sdRT=sd(ysim))
ggplot(df.sim.summary,aes(x=meanRT))+ geom_histogram(fill="white",color="black")+ theme_bw()+xlab("Sample means of the simulated data")



likelihoods$posterior_unnorm <- likelihoods$lkl*likelihoods$prior_density
ggplot(likelihoods,aes(x=mu,y=posterior_unnorm))+geom_line(linewidth=1,color="black")+
theme_bw()+xlab(expression(mu))+ylab("Posterior density \n Unnormalized")+
scale_x_continuous(limits = c(250,350))


df.lkl_prior <- melt(likelihoods,id=c("mu"))
df.lkl_prior$variable <-
ifelse(df.lkl_prior$variable=="lkl","Likelihood",
ifelse(df.lkl_prior$variable=="prior_density","Prior density","Unnormalized posterior density"))
ggplot(df.lkl_prior,aes(x=mu,y=value,color=variable))+geom_line(linewidth=1)+
theme_bw()+xlab(expression(mu))+ylab("")+
scale_x_continuous(limits = c(250,400))+
facet_wrap(~variable,scales = "free_y",ncol = 1)+
scale_color_manual(values = c("blue","orange","black"))+
theme(legend.position = "none")


# likelihoods$posterior <- likelihoods$posterior_unnorm / sum(likelihoods$posterior_unnorm)
# posterior_samples <- sample(
#   likelihoods$mu,           # values to sample from
#   size = 5000,              # number of samples
#   replace = TRUE,           # sampling with replacement
#   prob = likelihoods$posterior  # weights (normalized posterior)
# )
# ggplot(data.frame(mu = posterior_samples), aes(x = mu)) +
#   geom_histogram(bins = 50, fill = "skyblue", color = "black") +
#   theme_bw() +
#   xlab(expression(mu)) +
#   ylab("Posterior sample count") +
#   ggtitle("Samples drawn from posterior distribution")
# mean(posterior_samples)      # Posterior mean
# quantile(posterior_samples, c(0.025, 0.5, 0.975))  # 95% credible interval


mu_0 <- 350
sigma_0 <- 50
sigma <- 10
n <- length(y)

# Parameters of the posterior distribution
sigma_post <- 1 / sqrt((1 / sigma_0^2) + (n / sigma^2))
mu_post <- (sigma_post^2) * ((mu_0 / sigma_0^2) + (sum(y) / sigma^2))

# Draw samples
post_samples <- rnorm(10000, mu_post, sigma_post)

# Plot histogram
hist(post_samples)


df.post_samples <- data.frame(post_samples)
ggplot(df.post_samples,aes(x=post_samples))+
geom_density(linewidth=1)+theme_bw()+
scale_x_continuous(limits = c(275,325))

ggplot(likelihoods,aes(x=mu,y=posterior_unnorm))+geom_line(linewidth=1,color="black")+
theme_bw()+xlab(expression(mu))+ylab("Posterior density \n Unnormalized")+
scale_x_continuous(limits = c(275,325))

mu_samples <- rnorm(2000,mu_post,sigma_post)
sigma <- rep(10,2000)
N <- 50 # I will keep it same as the number of observations in our data y
df.pred <- data.frame(sample = rep(1:2000,each=N),
mu=rep(mu_samples,each=N),sigma=rep(sigma,each=N),
observation = rep(1:N,2000))
df.pred$ypred <- NA
for(i in 1:length(mu_samples)){
df.pred[df.pred$sample==i,]$ypred <- rnorm(N,mean=mu_samples[i],sd=sigma[i])
}
ggplot(df.pred,aes(x=ypred,group=sample))+
geom_density(alpha=0.0001)+theme_bw()

ggplot(df.pred, aes(x = ypred)) +
  geom_density(aes(group = sample), alpha = 0.0001, color = "gray") +
  geom_density(data = data.frame(y = y), aes(x = y), color = "red", linewidth = 1) +
  theme_bw() +
  labs(x = "Value", y = "Density")


obs <- subset(df.pred,sample==1)
obs$ypred <- y
ggplot(df.pred,aes(x=ypred,group=sample))+
geom_density(alpha=0.0001,color="gray")+
geom_density(data=obs,aes(x=ypred),color="red",linewidth=1)


y <- rnorm(10,1,2)
sigma = 2 # Known standard devation of normal distribution
mu_prior = 0 # Mean of prior distribution on mu
sigma_prior = 3 # Standard deviation of prior distribution on mu
n = 10 # no. of observations
analytical_mu_post <- rnorm(10000,
mean=(((sigma^2)*(mu_prior))+
((sigma_prior^2)*sum(y)))/
(sigma^2 + (n*(sigma_prior^2))),
sd=(1/(sigma_prior^2))+(n/(sigma^2)))
hist(analytical_mu_post,freq = FALSE)



# Grid approximation

# Create grid points
mu_grid <- seq(-5,5,length=1000)
#Calculate likelihood and posterior at each grid point
df.posterior <- data.frame(matrix(ncol=3,nrow=length(mu_grid)))
colnames(df.posterior) <- c("mu","likelihood","prior")
for(i in 1:length(mu_grid)){
likelihood <- prod(dnorm(y,mu_grid[i],2))
prior <- dnorm(mu_grid[i],0,3)
df.posterior[i,] <- c(mu_grid[i],likelihood,prior)
}

#Approximate marginal likelihood
df.posterior$ML <- rep(sum(df.posterior$likelihood*df.posterior$prior),1000)
#Estimate posterior density at each grid point
df.posterior <- df.posterior %>%
mutate(posterior=likelihood*prior/ML)
plot(df.posterior$mu,df.posterior$posterior)


df.estimate <- data.frame(matrix(ncol=2,nrow=10000))
colnames(df.estimate) <- c("theta_sample","likelihood")
for(i in 1:10000){
theta_i <- rbeta(1,1,1) # independent sample from the prior
likelihood <- dbinom(2,10,theta_i)
df.estimate[i,] <- c(theta_i,likelihood)
}
# Marginal likelihood
ML <- mean(df.estimate$likelihood)
ML
a <- 0  # Lower bound of θ
b <- 1  # Upper bound of θ
accepted_samples <- numeric(10000)
for(i in 1:10000) {
  theta_star <- runif(1, a, b)  # Propose θ*
  posterior_density <- dbinom(2, 10, theta_star) * 1  # Prior density = 1
  t_star <- runif(1, 0, 1)  # Threshold
  if(posterior_density > t_star) {
    accepted_samples[i] <- theta_star
  }
}
accepted_samples <- accepted_samples[accepted_samples != 0]  # Remove rejects
hist(accepted_samples, main = "Posterior Samples (Rejection Sampling)")
