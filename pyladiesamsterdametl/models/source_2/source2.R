#Throw an error.

yesterday = format(as.Date(Sys.Date()) - 1, "%Y-%m-%d 10:00:00")
data_frame = read.csv(file = file.path(Sys.getenv("RAW_DATA_LOCAL"), "COVID-19_aantallen_gemeente_cumulatief.csv"), sep = ";", stringsAsFactors = FALSE) %>%
  filter(Date_of_report <= yesterday) %>%
  group_by(Province) %>%
  summarise(total_admissions = sum(Hospital_admission)) %>%
  rename(province = Province)

write_delim(data_frame, file.path(Sys.getenv("RESULTS_DATA_LOCAL"), "source1.csv"), delim = ",")