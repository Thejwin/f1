import fastf1
import pandas as pd
import datetime


POINTS_DISTRIBUTION = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
SPRINT_POINTS = [8, 7, 6, 5, 4, 3, 2, 1]


def session_ids_for_event(event_row: pd.Series) -> list[str]:
    """Return the session identifiers to load for this event."""
    event_format = event_row["EventFormat"]
    if event_format == "sprint_qualifying":
        return ["S", "R"]
    return ["R"]


def points_for_position(position: int, sprint: bool = False) -> int:
    if sprint:
        return SPRINT_POINTS[position - 1] if 1 <= position <= len(SPRINT_POINTS) else 0
    return POINTS_DISTRIBUTION[position - 1] if 1 <= position <= len(POINTS_DISTRIBUTION) else 0


def get_event_sessions(schedule: pd.DataFrame) -> list[tuple[pd.Series, str]]:
    sessions = []
    for _, row in schedule.iterrows():
        if row["RoundNumber"] == 0:
            continue
        for session_id in session_ids_for_event(row):
            sessions.append((row, session_id))
    return sessions


def collect_session_results(year: int, event_name: str, session_id: str) -> pd.DataFrame:
    session = fastf1.get_session(year, event_name, session_id)
    session.load(laps=False, telemetry=False, weather=False, messages=False)
    results = session.results.copy()
    results["SessionId"] = session_id
    results["EventName"] = event_name
    results["Sprint"] = session_id == "S"
    return results


def build_standings(schedule: pd.DataFrame, year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    sessions = get_event_sessions(schedule)
    all_results = []

    for event_row, session_id in sessions:
        event_name = event_row["EventName"]
        try:
            result_df = collect_session_results(year, event_name, session_id)
        except Exception as exc:
            print(f"Skipping {event_name} {session_id}: {exc}")
            continue
        all_results.append(result_df)

    if not all_results:
        return pd.DataFrame(), pd.DataFrame()

    results = pd.concat(all_results, ignore_index=True)
    results["PointsEarned"] = results.apply(
        lambda row: points_for_position(int(row["Position"]) if pd.notna(row["Position"]) else 0, sprint=bool(row["Sprint"])),
        axis=1,
    )

    # Build driver standings using official F1 tiebreakers:
    # 1) total points, 2) number of wins, 3) number of 2nds, 4) number of 3rds, ...
    driver_points = (
        results.groupby(["DriverId", "FullName", "TeamName"], dropna=False)["PointsEarned"]
        .sum()
    )
    driver_df = driver_points.reset_index()

    # position counts per driver (1,2,3,...)
    pos_df = results.dropna(subset=["Position"]).copy()
    pos_df["Pos"] = pos_df["Position"].astype(int)
    if not pos_df.empty:
        max_pos = int(pos_df["Pos"].max())
    else:
        max_pos = 0

    if max_pos > 0:
        driver_pos_counts = (
            pos_df.groupby(["DriverId", "FullName", "TeamName", "Pos"]).size().unstack(fill_value=0)
        )
        # ensure consistent column order
        for i in range(1, max_pos + 1):
            col = i
            if col not in driver_pos_counts.columns:
                driver_pos_counts[col] = 0
        driver_pos_counts = driver_pos_counts.reindex(driver_df.set_index(["DriverId", "FullName", "TeamName"]).index, fill_value=0)
        for i in range(1, max_pos + 1):
            driver_df[f"pos_{i}"] = driver_pos_counts[i].values
    else:
        max_pos = 0

    driver_df["PointsEarned"] = driver_df["PointsEarned"].astype(float)
    # sort by points then by counts of 1st, 2nd, 3rd ... (descending)
    sort_cols = ["PointsEarned"] + [f"pos_{i}" for i in range(1, max_pos + 1)]
    if sort_cols:
        driver_standings = driver_df.sort_values(sort_cols, ascending=[False] * len(sort_cols)).reset_index(drop=True)
    else:
        driver_standings = driver_df.sort_values(["PointsEarned"], ascending=[False]).reset_index(drop=True)

    # Constructors: same tiebreaker logic but aggregated by team
    team_points = results.groupby(["TeamName"], dropna=False)["PointsEarned"].sum().reset_index()
    if max_pos > 0:
        team_pos_counts = (
            pos_df.groupby(["TeamName", "Pos"]).size().unstack(fill_value=0)
        )
        for i in range(1, max_pos + 1):
            if i not in team_pos_counts.columns:
                team_pos_counts[i] = 0
        team_pos_counts = team_pos_counts.reindex(team_points.set_index(["TeamName"]).index, fill_value=0)
        for i in range(1, max_pos + 1):
            team_points[f"pos_{i}"] = team_pos_counts[i].values

    constructor_sort_cols = ["PointsEarned"] + [c for c in team_points.columns if c.startswith("pos_")]
    if constructor_sort_cols:
        constructor_standings = team_points.sort_values(constructor_sort_cols, ascending=[False] * len(constructor_sort_cols)).reset_index(drop=True)
    else:
        constructor_standings = team_points.sort_values(["PointsEarned"], ascending=[False]).reset_index(drop=True)

    return driver_standings, constructor_standings


def main() -> None:
    year = datetime.datetime.now().year
    schedule = fastf1.get_event_schedule(year)
    driver_standings, constructor_standings = build_standings(schedule, year)

    if driver_standings.empty and constructor_standings.empty:
        print("No session standings could be computed.")
        return

    


    # Print compact top-10 summaries
    print("\nDriver standings:")
    driver_cols = [c for c in ["DriverId", "FullName", "TeamName", "PointsEarned"] if c in driver_standings.columns]
    print(driver_standings[driver_cols].head(22).to_string(index=False))

    print("\nConstructer standings:")
    team_cols = [c for c in ["TeamId", "TeamName", "PointsEarned"] if c in constructor_standings.columns]
    print(constructor_standings[team_cols].head(11).to_string(index=False))


if __name__ == "__main__":
    main()