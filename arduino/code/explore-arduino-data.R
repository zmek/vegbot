# Load libraries
# ==============

library(DBI)
library(dplyr)
library(tidyverse)
library(lubridate)

# Create functions
# ===============

calc_ts <- function(df) {
        
        ts_df <- tribble(
                ~ row_num,
                ~ ts2
        )
        
        for (i in 2:nrow(df)) {
                ts2 <- df$ts[i]
                if (df$millis[i-1] == "millis") {
                        start_ts <- ts2 - as.integer(df$millis[i])/1000    
                }
                if (is.na(df$ts[i]) && df$millis[i] != "millis") {
                        ts2 <- start_ts + as.integer(df$millis[i])/1000
                }
                if (!is.na(ts2)) {
                        ts_df <- ts_df %>% add_row(tibble_row(
                                row_num = df$row_num[i],
                                ts2 = ts2
                        ))
                }
                
        } 
        
        ts_df$ts2 <- as.POSIXct(ts_df$ts2)             
        df <- df %>% left_join(ts_df) 
        
        
        return(df)
}

process_log_file <- function(log_file, dat1) {
        log_file <- log_file %>% filter(temp_dht22 != 'nan', humidity_dht22 != 'nan')
        log_file <- log_file %>% mutate(arduinoId = as.numeric(arduinoId),
                                        temp = as.numeric(temp),
                                        temp_dht22 = as.numeric(temp_dht22),
                                        humidity = as.numeric(humidity),
                                        humidity_dht22 = as.numeric(humidity_dht22),
                                        pressure = as.numeric(pressure),
                                        uva = as.numeric(uva),
                                        uvb = as.numeric(uvb),
                                        uvIndex = as.numeric(uvIndex))
        
        if (length(grep("illuminance", colnames(log_file))) > 0) {
                log_file <- log_file %>%  mutate(
                        illuminance = as.numeric(illuminance)
                )
        }
        
        log_file <- log_file %>% left_join(dat1)
        log_file <- rowid_to_column(log_file, "row_num")
        log_file <- calc_ts(log_file)
}

get_plot_data <- function(dat2, loc1, plot ) {
        loc2 <- loc1 %>% filter(location == plot)
        loc_dat <- dat2 %>% filter(ts2 > loc2$dt_from[1],
                                   ts2 < loc2$dt_to[1],
                                   arduinoId == loc2$arduinoId[1])
        for (i in (2:nrow(loc2))) {
                loc_dat_ <- dat2 %>% filter(ts2 > loc2$dt_from[i],
                                                   ts2 < loc2$dt_to[i],
                                                   arduinoId == loc2$arduinoId[i])
                loc_dat <- dplyr::union(loc_dat, loc_dat_)
        }
        loc_dat$location <- plot
        return(loc_dat)
        
}


# Load data
# =========

# ctn <- DBI::dbConnect(RPostgres::Postgres(),
#                       host = "31.170.123.74",
#                       port = 5432,
#                       user = "vegbotsql_user1",
#                       password = "PhAsL@B7vAx2qAw",
#                       dbname = "vegbotsql")
# 
# 
# con <- dbConnect(RMariaDB::MariaDB(),
#                  host = "31.170.123.74",
#                  port = 3306,
#                  user = "vegbotsql,
#                  password = "PhAsL@B7vAx2qAw",
#                  dbname = "vegbotsql")


# Read the data saved to web
dat <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/webfaction/arduino_data.CSV",
                 col_names = c("id","arduinoId","ts", "temp","temp_dht22","humidity","humidity_dht22","pressure","illuminance", "uva", "uvb" , "uvIndex","rssi","millis","filename" )))
dat1 <- dat %>% filter(millis != "NULL")
loc <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/webfaction/arduino_location.CSV",
                          col_names = c("id","arduinoId","location","dt_from", "dt_to","compare","site_testing", "ts","note")))
loc1 <- loc # %>% filter(site_testing == 1)


# # data without timestamp - harvested on or prior to 13 July
# x_0001 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/LOG-0001.CSV"))
# x_0002 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/LOG-0002.CSV"))
# a1_1001_200713 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/LOG-1001.CSV"))
# a2_2001_200713 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/LOG-2001.CSV"))

# data harvested 200720 (other files contain no useful data)
log_1001 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino1/LOG-1001.CSV"))
log_1002 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino1/LOG-1002.CSV"))
log_2001 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino2/LOG-2001.CSV"))

log_1003 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino1/LOG-1003.CSV"))
log_2003 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino2/LOG-2003.CSV"))

log_1004 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino1/LOG-1004.CSV"))
log_2004 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino2/LOG-2004.CSV"))

log_1005 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino1/LOG-1005.CSV"))
log_2005 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino2/LOG-2005.CSV"))

log_1006 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino1/LOG-1006.CSV"))
log_2006 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino2/LOG-2006.CSV"))

log_1007 <- as_tibble(read_csv("~/GitHubRepos/vegbot/arduino/data-raw/sdcards/Arduino1/LOG-1007.CSV"))



log_1001$filename <- "log-1001.csv"
log_1002$filename <- "log-1002.csv"
log_2001$filename <- "log-2001.csv"
log_1003$filename <- "log-1003.csv"
log_2003$filename <- "log-2003.csv"
log_1004$filename <- "log_1004.csv"
log_2004$filename <- "log-2004.csv"
log_1005$filename <- "log-1005.csv"
log_2005$filename <- "log-2005.csv"
log_1006$filename <- "log-1006.csv"
log_2006$filename <- "log-2006.csv"
log_1007$filename <- "log-1007.csv"



# process data from WebFaction

dat1 <- dat1 %>% mutate(temp_dht22 = as.numeric(temp_dht22),
                        humidity_dht22 = as.numeric(humidity_dht22),
                        pressure = as.numeric(pressure),
                        uva = as.numeric(uva),
                        uvb = as.numeric(uvb),
                        uvIndex = as.numeric(uvIndex))


# process data from log files



log_1001 <- process_log_file(log_1001, dat1)
log_1002 <- process_log_file(log_1002, dat1)
log_1003 <- process_log_file(log_1003, dat1)
log_2001 <- process_log_file(log_2001, dat1)
log_2003 <- process_log_file(log_2003, dat1)
log_1004 <- process_log_file(log_1004, dat1) # something very strange happening with this - not joining
log_2004 <- process_log_file(log_2004, dat1)
log_1005 <- process_log_file(log_1005, dat1)
log_2005 <- process_log_file(log_2005, dat1)
log_1006 <- process_log_file(log_1006, dat1)
log_2006 <- process_log_file(log_2006, dat1)
log_1007 <- process_log_file(log_1007, dat1)

# merge files
dat2 <- dplyr::union(log_1001, log_1002)
dat2 <- dplyr::union(dat2, log_1003)
dat2 <- dplyr::union(dat2, log_2001)
dat2 <- dplyr::union(dat2, log_2003)
dat2 <- dplyr::union(dat2, log_1004) # error here
dat2 <- dplyr::union(dat2, log_2004)
dat2 <- dplyr::union(dat2, log_1005)
dat2 <- dplyr::union(dat2, log_2005)
dat2 <- dplyr::union(dat2, log_1006)
dat2 <- dplyr::union(dat2, log_2006)
dat2 <- dplyr::union(dat2, log_1007)


dat_upper <- get_plot_data(dat2, loc1, "Upper plot")
dat_lower <- get_plot_data(dat2, loc1, "Lower plot")
dat_swingball <- get_plot_data(dat2, loc1, "Swingball")
dat_steps <- get_plot_data(dat2, loc1, "Top of steps")
dat_farmbot_compost_end <- get_plot_data(dat2, loc1, "Farmbot compost end")
dat_farmbot_qube_end <- get_plot_data(dat2, loc1, "Farmbot Qube end")
dat_qube_inside <- get_plot_data(dat2, loc1, "Qube inside")
dat_garage_inside <- get_plot_data(dat2, loc1, "Garage inside")
dat_balcony <- get_plot_data(dat2, loc1, "Balcony")

dat_all <- dplyr::union(dat_upper, dat_lower)
dat_all <- dplyr::union(dat_all, dat_swingball)
dat_all <- dplyr::union(dat_all, dat_steps)
dat_all <- dplyr::union(dat_all, dat_steps)
dat_all <- dplyr::union(dat_all, dat_farmbot_compost_end)
dat_all <- dplyr::union(dat_all, dat_farmbot_qube_end)
dat_all <- dplyr::union(dat_all, dat_qube_inside)
dat_all <- dplyr::union(dat_all, dat_garage_inside)
dat_all <- dplyr::union(dat_all, dat_balcony)


dat_all <- dat_all %>% mutate(ts2 = ts2 + hours(1) )

# Create charts
dat_all %>% ggplot(aes(x = ts2, y = temp_dht22, col = location)) + geom_line() +
        theme_classic()

dat_all %>% mutate(date = date(ts2)) %>% 
        ggplot(aes(x = ts2, y = temp_dht22, col = location)) + geom_line() +
        theme_classic() +
        facet_grid(date ~ .)

dat_all %>% mutate(date = date(ts2)) %>% 
        ggplot(aes(x = ts2, y = illuminance, col = location)) + geom_line() +
        theme_classic() +
        facet_grid(date ~ .)


dat_all %>% filter(date(ts2) == "2020-07-10") %>% 
        ggplot(aes(x = ts2, y = temp_dht22, col = location)) + geom_line() +
        theme_classic() 

dat_all %>% filter(date(ts2) == "2020-07-21") %>% 
        ggplot(aes(x = ts2, y = temp_dht22, col = location)) + geom_line() +
        scale_x_datetime(date_breaks = "hours" , date_labels = "%H") +
        theme_classic() +
        theme(legend.position = "bottom") +
        labs(title = "Comparing lower plot and swingball sites 2020-07-21",
             subtitle = "Lower plot is to left of sleeper path as you look from house; swingball is near compost",
             x = "Hour",
             y = "Temperature",
             col = "Location") +
        annotate("rect", xmin=as.POSIXct("2020-07-21 10:00"),
                 xmax=as.POSIXct("2020-07-21 12:22"), 
                 ymin=10, ymax=40,
                 alpha = .2) +
        annotate("rect", xmin=as.POSIXct("2020-07-21 17:10"),
                      xmax=as.POSIXct("2020-07-21 18:20"), 
                      ymin=10, ymax=40,
                 alpha = .2) +
        annotate("text", x = as.POSIXct("2020-07-21 11:15"), y = 12, size = 3,
                 label = "Swingball plot in shade") +
        annotate("text", x = as.POSIXct("2020-07-21 17:45"), y = 12, size = 3,
                 label = "Lower plot\nin shade") +
        annotate("text", x = as.POSIXct("2020-07-21 15:00"), y = 20, size = 3,
                 label = "Temperature fluctuations reflect periods of \nsun and cloud.Temperatures significantly \ninflated by direct sun on the sensor. Highest \nair temperature on this date was 22 celsius")

dat_all %>% filter(date(ts2) == "2020-07-21") %>% 
        ggplot(aes(x = ts2, y = illuminance, col = location)) + geom_line() +
        theme_classic() +
        labs(title = "2020-07-21")

dat_all %>% filter(date(ts2) == "2020-07-22") %>% 
        ggplot(aes(x = ts2, y = temp_dht22, col = location)) + geom_line() +
        theme_classic() +
        labs(title = "2020-07-22")

dat_all %>% filter(date(ts2) == "2020-07-22") %>% 
        ggplot(aes(x = ts2, y = temp_dht22, col = location)) + geom_line() +
        theme_classic() +
        labs(title = "2020-07-22")

# Compare garage and Qube inside
dat_all %>% filter(date(ts2) == "2020-07-31") %>% 
        ggplot(aes(x = ts2, y = temp_dht22, col = location)) + geom_line() +
        scale_x_datetime(date_breaks = "hours" , date_labels = "%H") +
        theme_classic() +
        theme(legend.position = "bottom") +
        labs(title = "Comparing Qube and garage temperatures 2020-07-31",
             x = "Hour",
             y = "Temperature") +
        geom_vline(xintercept = as.POSIXct("2020-07-31 19:00"), linetype="dashed", , 
                                           color = "black", size=0.5) +
        annotate("text", x = as.POSIXct("2020-07-31 20:50"), y = 32, label = "I closed the Qube door")

# Compare garage and Qube inside
dat_all %>% filter(date(ts2) == "2020-09-22", ts2 > "2020-09-22 10:35:04") %>% 
        mutate(location = ifelse(location == "Swingball", "Farmbot", location)) %>% 
        ggplot(aes(x = ts2, y = temp_dht22, col = location)) + geom_line() +
        scale_x_datetime(date_breaks = "hours" , date_labels = "%H") +
        theme_classic() +
        theme(legend.position = "bottom") +
        labs(title = "Comparing balcony and Farmbot temperatures 2020-09-22",
             x = "Hour",
             y = "Temperature")

# Compare garage and Qube inside
dat_all %>% filter(date(ts2) == "2020-10-07") %>% 
        mutate(location = ifelse(location == "Swingball", "Farmbot", location)) %>% 
        ggplot(aes(x = ts2, y = temp_dht22, col = location)) + geom_line() +
        scale_x_datetime(date_breaks = "hours" , date_labels = "%H") +
        theme_classic() +
        theme(legend.position = "bottom") +
        labs(title = "Comparing balcony and Farmbot temperatures 2020-10-07",
             x = "Hour",
             y = "Temperature")

# save data for d3


dat_all <- dat_all %>% mutate(time = substr(ts2,  12,19)) 

write_delim(x = dat_all %>% filter(date(ts2) == "2020-10-07") %>% select((time), temp_dht22), 
            path ="~/Google Drive/WhatsNext/What not/D3 files/temp_20_10_07.csv",
            delim = ",")

write_delim(x = dat_all %>% filter(date(ts2) == "2020-10-07") %>% select(ts2, temp_dht22), 
            path ="~/Google Drive/WhatsNext/What not/D3 files/temp_20_10_07_2.csv",
            delim = ",")

dat_all <- dat_all %>% mutate(date = substr(ts2,  1,10)) 

write_delim(x = dat_all %>% filter(date(ts2) == "2020-10-07") %>% select(date, temp_dht22), 
            path ="~/Google Drive/WhatsNext/What not/D3 files/temp_20_10_07_3.csv",
            delim = ",")

date_beg = date("2020-07-10")
date_beg + 834
date = as_tibble(seq(date_beg,date_beg + 833,1))

temperature = dat_all %>% filter(date(ts2) == "2020-10-07") %>% select(temp_dht22)
bind_cols(date, temperature)


write_delim(temperature, 
            path ="~/Google Drive/WhatsNext/What not/D3 files/temp_20_10_07_4.csv",
            delim = ",")


loc1 %>% count(location)




