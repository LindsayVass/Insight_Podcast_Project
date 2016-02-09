library(dplyr)
library(ggplot2)
library(ggthemes)

podcast_subscribe <- read.csv('csv//podcast_sim_by_subscribe.csv')

# summarise by search_podcast
subscribe_summary <- podcast_subscribe %>%
  select(-X) %>%
  group_by(search_podcast_id, subscribe_status) %>%
  summarise(similarity = mean(similarity))

group_summary <- subscribe_summary %>%
  ungroup() %>%
  group_by(subscribe_status) %>%
  summarise(mean_similarity = mean(similarity),
            sem_similarity = sd(similarity) / sqrt(n()))

group_summary$subscribe_status <- factor(group_summary$subscribe_status, levels = c('True', 'False'))
group_summary$subscribe_status <- plyr::mapvalues(group_summary$subscribe_status,
                                                  from = c('True', 'False'),
                                                  to = c('Also Subscribed To', 'Not Subscribed To'))

# plot subscribe results
pSubscribe <- ggplot(group_summary, aes(x = subscribe_status,
                          y = mean_similarity,
                          ymin = mean_similarity - sem_similarity,
                          ymax = mean_similarity + sem_similarity,
                          fill = subscribe_status)) +
  geom_errorbar() +
  geom_bar(stat='identity') +
  theme_fivethirtyeight() +
  theme(axis.title.x = element_blank(),
        axis.text.x = element_blank(),
        axis.ticks.x = element_blank(),
        axis.ticks.y = element_line(colour="black"),
        axis.title.y = element_text(size=24, margin = margin(0,10,0,0)),
        legend.title = element_blank(),
        legend.position = 'top',
        legend.text = element_text(size=18),
        panel.background = element_rect(colour = "black")) +
  ylab('Similarity') +
  scale_fill_brewer(palette = 'Paired', direction=-1)
ggsave('r_plots/similarity_by_subscribe.pdf', width = 6, height = 8)
