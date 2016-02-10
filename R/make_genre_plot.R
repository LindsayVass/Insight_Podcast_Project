library(RPostgreSQL)
library(dplyr)
library(ggplot2)
library(ggthemes)

# load PostgreSQL driver
drv <- dbDriver("PostgreSQL")

# create connection
dbname <- "podcast"
host   <- "localhost"
port   <- 5432
user   <- "lindsay"
con    <- dbConnect(drv, 
                    dbname = dbname,
                    host = host,
                    port = port,
                    user = user)

# get names and genres
podcast_df <- dbGetQuery(con, "SELECT name, podcast.id, podcast_has_genre.genre_id FROM podcast INNER JOIN podcast_has_genre ON podcast.id = podcast_has_genre.podcast_id;")
genre_df  <- dbGetQuery(con, "SELECT name, id FROM genre;")

# join the tables
merge_df <- inner_join(podcast_df, genre_df, by = c('genre_id' = 'id'))
names(merge_df) <- c('podcast_name', 'podcast_id', 'genre_id', 'genre_name')

# plot podcasts per genre
genreSummary <- merge_df %>%
  group_by(genre_name) %>%
  filter(genre_name != "Podcasts") %>%
  summarise(Count = n()) %>%
  transform(genre_name = reorder(genre_name, Count)) 
pGenre <- ggplot(genreSummary, aes(x = genre_name, y = Count)) +
  geom_bar(stat='identity') +
  coord_flip(ylim=c(50,1200)) +
  theme_few() +
  theme(axis.title.y = element_blank()) +
  xlab('Number of Podcasts')
ggsave('r_plots/genre_counts.pdf', width = 20, height = 20)

# top 10 genres
pTop10 <- genreSummary %>%
  mutate(Proportion = Count / length(unique(podcast_df$id))) %>%
  arrange(desc(Proportion)) %>%
  top_n(10) %>%
  ggplot(aes(x = genre_name, y = Proportion)) +
  geom_bar(stat='identity') +
  geom_text(aes(x = genre_name, y = 0.01, label = genre_name, hjust = 0), colour = "white", size = 7) +
  scale_y_continuous(labels = scales::percent) +
  coord_flip() +
  theme_fivethirtyeight() +
  theme(axis.text.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.text.x = element_text(size=24),
        axis.title.x = element_text(size=18),
        axis.title.y = element_text(size=18)) 
ggsave('r_plots/genre_counts_top10.pdf', width = 13, height = 10)