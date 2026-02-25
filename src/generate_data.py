"""
generate_data.py
Generates a synthetic VAA (Voting Advice Application) dataset.

Output: data/vaa_synthetic.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
N_RESPONDENTS = 500
N_PARTIES = 6
N_ISSUES = 10

PARTIES = ["Party A", "Party B", "Party C", "Party D", "Party E", "Party F"]

ISSUES = [
    "tax_policy",
    "climate_action",
    "immigration",
    "healthcare",
    "education_spending",
    "eu_integration",
    "pension_reform",
    "defence_spending",
    "drug_policy",
    "electoral_reform",
]

# Party positions on each issue: -2 (strongly against) to +2 (strongly for)
PARTY_POSITIONS = {
    "Party A": [ 2,  1, -2,  1,  1,  2,  0,  1, -1,  1],  # Centre-right, pro-EU
    "Party B": [-2,  2,  1,  2,  2,  1,  2, -1,  1,  2],  # Left, progressive
    "Party C": [ 1, -1, -2, -1, -1,  2,  1,  2, -2,  0],  # Conservative
    "Party D": [-1,  2,  2,  1,  1, -2,  0, -1,  1, -1],  # Eurosceptic left
    "Party E": [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # Centrist
    "Party F": [ 2, -2, -2, -1,  0,  1,  1,  2, -1,  0],  # Right-wing
}


def generate_respondents(rng: np.random.Generator) -> pd.DataFrame:
    """Generate respondent-level data with positions and demographics."""
    positions = rng.integers(-2, 3, size=(N_RESPONDENTS, N_ISSUES))
    df = pd.DataFrame(positions, columns=ISSUES)
    df.insert(0, "respondent_id", range(1, N_RESPONDENTS + 1))
    df["age"] = rng.integers(18, 81, size=N_RESPONDENTS)
    df["gender"] = rng.choice(["male", "female", "other"], size=N_RESPONDENTS, p=[0.48, 0.48, 0.04])
    df["education"] = rng.choice(["primary", "secondary", "tertiary"], size=N_RESPONDENTS, p=[0.2, 0.5, 0.3])
    return df


def compute_vote_choice(respondents: pd.DataFrame) -> pd.Series:
    """Assign vote choice based on minimum Manhattan distance to party positions."""
    party_pos = np.array([PARTY_POSITIONS[p] for p in PARTIES])
    resp_pos = respondents[ISSUES].values
    distances = np.abs(resp_pos[:, np.newaxis, :] - party_pos[np.newaxis, :, :]).sum(axis=2)
    # Add small noise to break ties randomly
    rng = np.random.default_rng(SEED + 1)
    noise = rng.uniform(0, 0.5, size=distances.shape)
    closest = np.argmin(distances + noise, axis=1)
    return pd.Series([PARTIES[i] for i in closest], name="vote_choice")


def generate_party_positions() -> pd.DataFrame:
    """Return tidy party-position reference table."""
    rows = []
    for party, positions in PARTY_POSITIONS.items():
        for issue, pos in zip(ISSUES, positions):
            rows.append({"party": party, "issue": issue, "position": pos})
    return pd.DataFrame(rows)


def main():
    rng = np.random.default_rng(SEED)
    out_dir = Path(__file__).parent.parent / "data"
    out_dir.mkdir(exist_ok=True)

    respondents = generate_respondents(rng)
    respondents["vote_choice"] = compute_vote_choice(respondents)

    respondents.to_csv(out_dir / "vaa_respondents.csv", index=False)
    generate_party_positions().to_csv(out_dir / "vaa_party_positions.csv", index=False)

    print(f"Respondents: {len(respondents)} rows -> data/vaa_respondents.csv")
    print(f"Party positions: -> data/vaa_party_positions.csv")
    print(f"\nVote share:\n{respondents['vote_choice'].value_counts(normalize=True).mul(100).round(1).to_string()}")


if __name__ == "__main__":
    main()
