# generate_data.R
# Generates a synthetic VAA dataset using R/tidyverse.
# Output: data/vaa_respondents.csv, data/vaa_party_positions.csv

library(tidyverse)

set.seed(42)

N_RESPONDENTS <- 500
ISSUES <- c(
  "tax_policy", "climate_action", "immigration", "healthcare",
  "education_spending", "eu_integration", "pension_reform",
  "defence_spending", "drug_policy", "electoral_reform"
)

PARTIES <- c("Party A", "Party B", "Party C", "Party D", "Party E", "Party F")

party_positions_raw <- tribble(
  ~party,    ~tax_policy, ~climate_action, ~immigration, ~healthcare,
             ~education_spending, ~eu_integration, ~pension_reform,
             ~defence_spending, ~drug_policy, ~electoral_reform,
  "Party A",  2,  1, -2,  1,  1,  2,  0,  1, -1,  1,
  "Party B", -2,  2,  1,  2,  2,  1,  2, -1,  1,  2,
  "Party C",  1, -1, -2, -1, -1,  2,  1,  2, -2,  0,
  "Party D", -1,  2,  2,  1,  1, -2,  0, -1,  1, -1,
  "Party E",  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
  "Party F",  2, -2, -2, -1,  0,  1,  1,  2, -1,  0
)

# Tidy party positions for export
party_pos_tidy <- party_positions_raw |>
  pivot_longer(-party, names_to = "issue", values_to = "position")

# Generate respondent positions
resp_positions <- map(ISSUES, ~ sample(-2:2, N_RESPONDENTS, replace = TRUE)) |>
  set_names(ISSUES) |>
  as_tibble() |>
  mutate(respondent_id = row_number(), .before = 1)

# Demographics
resp_positions <- resp_positions |>
  mutate(
    age = sample(18:80, N_RESPONDENTS, replace = TRUE),
    gender = sample(c("male", "female", "other"), N_RESPONDENTS,
                    replace = TRUE, prob = c(0.48, 0.48, 0.04)),
    education = sample(c("primary", "secondary", "tertiary"), N_RESPONDENTS,
                       replace = TRUE, prob = c(0.2, 0.5, 0.3))
  )

# Vote choice via Manhattan proximity
party_mat <- party_positions_raw |> select(all_of(ISSUES)) |> as.matrix()
resp_mat  <- resp_positions |> select(all_of(ISSUES)) |> as.matrix()

set.seed(43)
vote_choice <- apply(resp_mat, 1, function(r) {
  dists <- rowSums(abs(sweep(party_mat, 2, r))) + runif(nrow(party_mat), 0, 0.5)
  PARTIES[which.min(dists)]
})

resp_positions <- resp_positions |> mutate(vote_choice = vote_choice)

# Write outputs
dir.create("data", showWarnings = FALSE)
write_csv(resp_positions, "data/vaa_respondents.csv")
write_csv(party_pos_tidy, "data/vaa_party_positions.csv")

vote_share <- resp_positions |>
  count(vote_choice) |>
  mutate(share = round(n / sum(n) * 100, 1)) |>
  arrange(desc(share))

cat("Respondents written to data/vaa_respondents.csv\n")
cat("Party positions written to data/vaa_party_positions.csv\n\n")
print(vote_share)
