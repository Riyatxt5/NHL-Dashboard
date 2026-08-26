import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pymysql

conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = 'hub'
)
cursor = conn.cursor()

with open("css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)

st.set_page_config(
    page_title="NHL Dashboard",
    page_icon="🏒",
    layout="wide"
)

with st.sidebar:
    selected = option_menu(
    menu_title=None,
    options=[
        "Home",
        "Standings",
        "Team Info",
        "Player Search",
        "Game Results",
        "Leaderboards",
        "Goalie Center",
        "Game Details",
        "Query Explorer"
    ],
    icons=[
        "house",
        "bar-chart",
        "people",
        "person",
        "calendar-event",
        "trophy",
        "shield-shaded",
        "clipboard-data",
        "search"
    ],
    default_index=1
)

    # ---------------------------------------------------------
    # Home Page
    # ---------------------------------------------------------

if selected == "Home":

    st.title("🏒 NHL Analytics Dashboard")
    st.write("National Hockey League — Overall Statistics & Highlights")

    # ---------------------------------------------------------
    # KPI 1 - TOTAL TEAMS
    # ---------------------------------------------------------

    team_count = pd.read_sql("""
        SELECT COUNT(*) AS total_teams
        FROM teams;
    """, conn)

    total_teams = int(team_count.iloc[0]["total_teams"])


    # ---------------------------------------------------------
    # KPI 2 - TOTAL PLAYERS
    # ---------------------------------------------------------

    player_count = pd.read_sql("""
        SELECT COUNT(*) AS total_players
        FROM players;
    """, conn)

    total_players = int(player_count.iloc[0]["total_players"])


    # ---------------------------------------------------------
    # KPI 3 - TOTAL GAMES
    # ---------------------------------------------------------

    game_count = pd.read_sql("""
        SELECT COUNT(*) AS total_games
        FROM games
        WHERE season = '20252026';
    """, conn)

    total_games = int(game_count.iloc[0]["total_games"])


    # ---------------------------------------------------------
    # KPI 4 - TOTAL GOALS
    # ---------------------------------------------------------

    goal_count = pd.read_sql("""
        SELECT SUM(goals_for) AS total_goals
        FROM standings
        WHERE season = '20252026';
    """, conn)

    total_goals = int(goal_count.iloc[0]["total_goals"] or 0)


    # ---------------------------------------------------------
    # KPI CARDS
    # ---------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.metric(
                label="Total Teams",
                value=total_teams
            )

    with col2:
        with st.container(border=True):
            st.metric(
                label="Total Players",
                value=total_players
            )

    with col3:
        with st.container(border=True):
            st.metric(
                label="Total Games",
                value=total_games
            )

    with col4:
        with st.container(border=True):
            st.metric(
                label="Total Goals",
                value=total_goals
            )


    st.markdown("---")


    # ---------------------------------------------------------
    # TOP POINT SCORER
    # ---------------------------------------------------------

    top_scorer = pd.read_sql("""
        SELECT
            CONCAT(p.first_name, ' ', p.last_name) AS player_name,
            t.team_name,
            s.points,
            s.goals,
            s.assists
        FROM skater_season_stats s
        INNER JOIN players p
            ON s.player_id = p.player_id
        INNER JOIN teams t
            ON s.team_id = t.team_id
        WHERE s.season = '20252026'
        ORDER BY s.points DESC
        LIMIT 1;
    """, conn)


    # ---------------------------------------------------------
    # TOP GOAL SCORER
    # ---------------------------------------------------------

    top_goal_scorer = pd.read_sql("""
        SELECT
            CONCAT(p.first_name, ' ', p.last_name) AS player_name,
            t.team_name,
            s.goals,
            s.points
        FROM skater_season_stats s
        INNER JOIN players p
            ON s.player_id = p.player_id
        INNER JOIN teams t
            ON s.team_id = t.team_id
        WHERE s.season = '20252026'
        ORDER BY s.goals DESC
        LIMIT 1;
    """, conn)


    # ---------------------------------------------------------
    # BEST GOALIE
    # ---------------------------------------------------------

    best_goalie = pd.read_sql("""
        SELECT
            CONCAT(p.first_name, ' ', p.last_name) AS player_name,
            t.team_name,
            g.save_pct,
            g.goals_against_avg,
            g.shutouts
        FROM goalie_season_stats g
        INNER JOIN players p
            ON g.player_id = p.player_id
        INNER JOIN teams t
            ON g.team_id = t.team_id
        WHERE g.season = '20252026'
          AND g.save_pct IS NOT NULL
        ORDER BY g.save_pct DESC
        LIMIT 1;
    """, conn)


    # ---------------------------------------------------------
    # TEAM WITH MOST WINS
    # ---------------------------------------------------------

    most_wins_team = pd.read_sql("""
        SELECT
            t.team_name,
            s.wins,
            s.points,
            s.goals_for
        FROM standings s
        INNER JOIN teams t
            ON s.team_id = t.team_id
        WHERE s.season = '20252026'
        ORDER BY s.wins DESC
        LIMIT 1;
    """, conn)


    # ---------------------------------------------------------
    # HIGHLIGHT CARDS - TOP SCORERS
    # ---------------------------------------------------------

    col1, col2 = st.columns(2)

    # ---------------------------------------------------------
    # TOP POINT SCORER CARD
    # ---------------------------------------------------------

    with col1:

        with st.container(border=True):

            st.subheader("🏆 Top Point Scorer")

            if not top_scorer.empty:

                player = top_scorer.iloc[0]

                st.write(
                    f"**{player['player_name']}**"
                )

                st.write(
                    f"Team: {player['team_name']}"
                )

                st.metric(
                    "Points",
                    int(player["points"])
                )

                st.write(
                    f"Goals: {int(player['goals'])}  |  "
                    f"Assists: {int(player['assists'])}"
                )

            else:
                st.info("No player data available.")


    # ---------------------------------------------------------
    # TOP GOAL SCORER CARD
    # ---------------------------------------------------------

    with col2:

        with st.container(border=True):

            st.subheader("🥅 Top Goal Scorer")

            if not top_goal_scorer.empty:

                player = top_goal_scorer.iloc[0]

                st.write(
                    f"**{player['player_name']}**"
                )

                st.write(
                    f"Team: {player['team_name']}"
                )

                st.metric(
                    "Goals",
                    int(player["goals"])
                )

                st.write(
                    f"Total Points: {int(player['points'])}"
                )

            else:
                st.info("No player data available.")


    # ---------------------------------------------------------
    # BEST GOALIE + MOST WINS TEAM
    # ---------------------------------------------------------

    col1, col2 = st.columns(2)


    # ---------------------------------------------------------
    # BEST GOALIE CARD
    # ---------------------------------------------------------

    with col1:

        with st.container(border=True, height=250):

            st.subheader("🧤 Best Goalie")

            if not best_goalie.empty:

                goalie = best_goalie.iloc[0]

                st.write(
                    f"**{goalie['player_name']}**"
                )

                st.write(
                    f"Team: {goalie['team_name']}"
                )

                # Save Percentage
                if pd.notna(goalie["save_pct"]):

                    save_pct = float(goalie["save_pct"])

                    # If stored as decimal (example: 0.915)
                    if save_pct <= 1:
                        save_pct = save_pct * 100

                    save_pct_text = f"{save_pct:.2f}%"

                else:

                    save_pct_text = "N/A"


                st.metric(
                    "Save %",
                    save_pct_text
                )


                # Goals Against Average
                if pd.notna(goalie["goals_against_avg"]):

                    gaa_text = f"{float(goalie['goals_against_avg']):.2f}"

                else:

                    gaa_text = "N/A"


                # Shutouts
                if pd.notna(goalie["shutouts"]):

                    shutouts_text = str(
                        int(goalie["shutouts"])
                    )

                else:

                    shutouts_text = "N/A"


                st.write(
                    f"GAA: {gaa_text}  |  "
                    f"Shutouts: {shutouts_text}"
                )

            else:

                st.info("No goalie data available.")


    # ---------------------------------------------------------
    # MOST WINS TEAM CARD
    # ---------------------------------------------------------

    with col2:

        with st.container(border=True, height=250):

            st.subheader("🏅 Most Wins Team")

            if not most_wins_team.empty:

                team = most_wins_team.iloc[0]

                st.write(
                    f"**{team['team_name']}**"
                )

                st.metric(
                    "Wins",
                    int(team["wins"])
                )

                st.write(
                    f"Points: {int(team['points'])}  |  "
                    f"Goals For: {int(team['goals_for'])}"
                )

            else:

                st.info("No standings data available.")

# =========================================================
# STANDINGS PAGE
# =========================================================

if selected == "Standings":

    st.title("🏆 NHL Standings")
    st.write("League standings by conference and division")


    # =========================================================
    # 1. CONFERENCE FILTER
    # =========================================================

    conference_list = pd.read_sql("""
        SELECT DISTINCT conference_name
        FROM teams
        WHERE conference_name IS NOT NULL
          AND conference_name <> ''
        ORDER BY conference_name;
    """, conn)

    conference_options = (
        ["All Conferences"]
        + conference_list["conference_name"].tolist()
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        selected_conference = st.selectbox(
            "Select Conference",
            conference_options
        )


    # =========================================================
    # 2. DIVISION FILTER
    #    Depends on Conference
    # =========================================================

    if selected_conference == "All Conferences":

        division_list = pd.read_sql("""
            SELECT DISTINCT central_name
            FROM teams
            WHERE central_name IS NOT NULL
              AND central_name <> ''
            ORDER BY central_name;
        """, conn)

    else:

        division_list = pd.read_sql("""
            SELECT DISTINCT central_name
            FROM teams
            WHERE conference_name = %s
              AND central_name IS NOT NULL
              AND central_name <> ''
            ORDER BY central_name;
        """, conn, params=[selected_conference])


    division_options = (
        ["All Divisions"]
        + division_list["central_name"].tolist()
    )


    with col2:

        selected_division = st.selectbox(
            "Select Division",
            division_options
        )


    # =========================================================
    # 3. TEAM FILTER
    #    Depends on Conference + Division
    # =========================================================

    if selected_conference == "All Conferences":

        if selected_division == "All Divisions":

            team_list = pd.read_sql("""
                SELECT team_name
                FROM teams
                ORDER BY team_name;
            """, conn)

        else:

            team_list = pd.read_sql("""
                SELECT team_name
                FROM teams
                WHERE central_name = %s
                ORDER BY team_name;
            """, conn, params=[selected_division])

    else:

        if selected_division == "All Divisions":

            team_list = pd.read_sql("""
                SELECT team_name
                FROM teams
                WHERE conference_name = %s
                ORDER BY team_name;
            """, conn, params=[selected_conference])

        else:

            team_list = pd.read_sql("""
                SELECT team_name
                FROM teams
                WHERE conference_name = %s
                  AND central_name = %s
                ORDER BY team_name;
            """, conn, params=[
                selected_conference,
                selected_division
            ])


    team_options = (
        ["All Teams"]
        + team_list["team_name"].tolist()
    )


    with col3:

        selected_team = st.selectbox(
            "Select Team",
            team_options
        )


    st.markdown("---")


    # =========================================================
    # 4. BUILD STANDINGS QUERY
    # =========================================================

    query = """
        SELECT
            t.team_abbrv AS Team,
            t.team_name AS Team_Name,
            t.conference_name AS Conference,
            t.central_name AS Division,
            s.games_played AS GP,
            s.wins AS W,
            s.losses AS L,
            s.ot_losses AS OT_L,
            s.points AS PTS,
            s.goals_for AS GF,
            s.goals_against AS GA,
            s.home_wins AS Home_Wins,
            s.away_wins AS Away_Wins,
            s.streak_type AS Streak,
            s.streak_count AS Streak_Count

        FROM standings s

        INNER JOIN teams t
            ON s.team_id = t.team_id

        WHERE s.season = '20252026'
    """

    params = []


    # =========================================================
    # 5. APPLY CONFERENCE FILTER
    # =========================================================

    if selected_conference != "All Conferences":

        query += """
            AND t.conference_name = %s
        """

        params.append(selected_conference)


    # =========================================================
    # 6. APPLY DIVISION FILTER
    # =========================================================

    if selected_division != "All Divisions":

        query += """
            AND t.central_name = %s
        """

        params.append(selected_division)


    # =========================================================
    # 7. APPLY TEAM FILTER
    # =========================================================

    if selected_team != "All Teams":

        query += """
            AND t.team_name = %s
        """

        params.append(selected_team)


    # =========================================================
    # 8. ORDER STANDINGS
    # =========================================================

    query += """
        ORDER BY
            s.points DESC,
            s.wins DESC,
            s.goals_for DESC;
    """


    # =========================================================
    # 9. EXECUTE QUERY
    # =========================================================

    try:

        df = pd.read_sql(
            query,
            conn,
            params=params
        )


        # =====================================================
        # 10. DISPLAY RESULT
        # =====================================================

        if df.empty:

            st.warning(
                "No teams found for the selected filters."
            )

        else:

            st.subheader("League Standings")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    except Exception as e:

        st.error(
            f"Unable to load standings data: {e}"
        )

# =========================================================
# PLAYER SEARCH PAGE
# =========================================================

if selected == "Player Search":

    st.title("👤 Player Search")
    st.write("Search and view detailed player information and season statistics")


    # =========================================================
    # 1. GET PLAYER LIST
    # =========================================================

    player_list = pd.read_sql("""
        SELECT
            player_id,
            CONCAT(first_name, ' ', last_name) AS player_name
        FROM players
        ORDER BY first_name, last_name;
    """, conn)


    player_options = player_list["player_name"].tolist()


    # =========================================================
    # 2. PLAYER SELECT BOX
    # =========================================================

    selected_player = st.selectbox(
        "Select Player",
        player_options
    )


    st.markdown("---")


    # =========================================================
    # 3. GET SELECTED PLAYER INFORMATION
    # =========================================================

    player_info = pd.read_sql("""
        SELECT
            p.player_id,
            p.first_name,
            p.last_name,
            p.position,
            p.jersey_number,
            p.birth_date,
            p.birth_country,
            p.height_cm,
            p.weight_kg,
            p.shoots_catches,
            p.headshot_url,

            t.team_id,
            t.team_abbrv,
            t.team_name,
            t.conference_name,
            t.central_name

        FROM players p

        INNER JOIN teams t
            ON p.team_id = t.team_id

        WHERE CONCAT(p.first_name, ' ', p.last_name) = %s

        LIMIT 1;
    """, conn, params=[selected_player])


    try:

        if player_info.empty:

            st.warning(
                "No information found for the selected player."
            )

        else:

            player = player_info.iloc[0]

            player_id = int(player["player_id"])


            # =================================================
            # 4. PLAYER HEADER + PHOTO
            # =================================================

            photo_col, info_col = st.columns([1, 3])


            with photo_col:

                if (
                    pd.notna(player["headshot_url"])
                    and str(player["headshot_url"]).strip() != ""
                ):

                    st.image(
                        player["headshot_url"],
                        width=180
                    )

                else:

                    st.write("📷")
                    st.caption("Player photo not available")


            with info_col:

                st.subheader(
                    f"{player['first_name']} {player['last_name']}"
                )

                jersey = player["jersey_number"]

                if pd.isna(jersey):
                    jersey = "N/A"
                else:
                    jersey = int(jersey)

                st.write(
                    f"**{player['position']}**  |  "
                    f"Jersey #{jersey}  |  "
                    f"{player['team_name']}"
                )

                st.write(
                    f"{player['conference_name']} Conference  |  "
                    f"{player['central_name']} Division"
                )


            st.markdown("---")


            # =================================================
            # 5. PLAYER INFORMATION
            # =================================================

            st.subheader("Player Information")


            info_col1, info_col2, info_col3, info_col4 = st.columns(4)


            with info_col1:

                position = player["position"]

                if pd.isna(position):
                    position = "N/A"

                st.metric(
                    "Position",
                    position
                )


            with info_col2:

                jersey = player["jersey_number"]

                if pd.isna(jersey):
                    jersey = "N/A"
                else:
                    jersey = int(jersey)

                st.metric(
                    "Jersey Number",
                    jersey
                )


            with info_col3:

                team_abbrv = player["team_abbrv"]

                if pd.isna(team_abbrv):
                    team_abbrv = "N/A"

                st.metric(
                    "Team",
                    team_abbrv
                )


            with info_col4:

                country = player["birth_country"]

                if pd.isna(country):
                    country = "N/A"

                st.metric(
                    "Birth Country",
                    country
                )


            # =================================================
            # 6. ADDITIONAL PLAYER DETAILS
            # =================================================

            detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(
                [1.4, 1, 1, 1]
            )


            with detail_col1:

                if pd.isna(player["birth_date"]):

                    birth_date = "N/A"

                else:

                    birth_date = pd.to_datetime(
                        player["birth_date"]
                    ).strftime("%Y-%m-%d")


                st.markdown("**Birth Date**")
                st.write(birth_date)


            with detail_col2:

                if pd.isna(player["height_cm"]):

                    height = "N/A"

                else:

                    height = f"{float(player['height_cm']):.1f} cm"


                st.markdown("**Height**")
                st.write(height)


            with detail_col3:

                if pd.isna(player["weight_kg"]):

                    weight = "N/A"

                else:

                    weight = f"{float(player['weight_kg']):.1f} kg"


                st.markdown("**Weight**")
                st.write(weight)


            with detail_col4:

                shoots = player["shoots_catches"]

                if pd.isna(shoots):

                    shoots = "N/A"

                st.markdown("**Shoots / Catches**")
                st.write(shoots)


            st.markdown("---")


            # =================================================
            # 7. CHECK PLAYER POSITION
            # =================================================

            position = str(player["position"]).upper()


            # =================================================
            # 8. SKATER SEASON STATISTICS
            # =================================================

            if position != "G":

                st.subheader("Season Statistics")


                skater_stats = pd.read_sql("""
                    SELECT
                        games_played,
                        goals,
                        assists,
                        points,
                        plus_minus,
                        penalty_min,
                        shots,
                        avg_toi
                    FROM skater_season_stats
                    WHERE player_id = %s
                      AND season = '20252026'
                    LIMIT 1;
                """, conn, params=[player_id])


                if skater_stats.empty:

                    st.info(
                        "No season statistics available for this player."
                    )

                else:

                    stats = skater_stats.iloc[0]


                    # -----------------------------------------
                    # KPI ROW 1
                    # -----------------------------------------

                    kpi1, kpi2, kpi3, kpi4 = st.columns(4)


                    with kpi1:

                        gp = stats["games_played"]

                        if pd.isna(gp):
                            gp = 0
                        else:
                            gp = int(gp)

                        st.metric(
                            "Games Played",
                            gp
                        )


                    with kpi2:

                        goals = stats["goals"]

                        if pd.isna(goals):
                            goals = 0
                        else:
                            goals = int(goals)

                        st.metric(
                            "Goals",
                            goals
                        )


                    with kpi3:

                        assists = stats["assists"]

                        if pd.isna(assists):
                            assists = 0
                        else:
                            assists = int(assists)

                        st.metric(
                            "Assists",
                            assists
                        )


                    with kpi4:

                        points = stats["points"]

                        if pd.isna(points):
                            points = 0
                        else:
                            points = int(points)

                        st.metric(
                            "Points",
                            points
                        )


                    # -----------------------------------------
                    # KPI ROW 2
                    # -----------------------------------------

                    kpi5, kpi6, kpi7, kpi8 = st.columns(4)


                    with kpi5:

                        plus_minus = stats["plus_minus"]

                        if pd.isna(plus_minus):
                            plus_minus = 0
                        else:
                            plus_minus = int(plus_minus)

                        st.metric(
                            "Plus / Minus",
                            plus_minus
                        )


                    with kpi6:

                        penalty_min = stats["penalty_min"]

                        if pd.isna(penalty_min):
                            penalty_min = 0
                        else:
                            penalty_min = int(penalty_min)

                        st.metric(
                            "Penalty Minutes",
                            penalty_min
                        )


                    with kpi7:

                        shots = stats["shots"]

                        if pd.isna(shots):
                            shots = 0
                        else:
                            shots = int(shots)

                        st.metric(
                            "Shots",
                            shots
                        )


                    with kpi8:

                        avg_toi = stats["avg_toi"]

                        if pd.isna(avg_toi):
                            avg_toi = "N/A"

                        st.metric(
                            "Average TOI",
                            avg_toi
                        )


            # =================================================
            # 9. GOALIE SEASON STATISTICS
            # =================================================

            else:

                st.subheader("Goalie Season Statistics")


                goalie_stats = pd.read_sql("""
                    SELECT
                        games_played,
                        wins,
                        losses,
                        ot_losses,
                        save_pct,
                        goals_against_avg,
                        shutouts,
                        saves
                    FROM goalie_season_stats
                    WHERE player_id = %s
                      AND season = '20252026'
                    LIMIT 1;
                """, conn, params=[player_id])


                if goalie_stats.empty:

                    st.info(
                        "No goalie season statistics available "
                        "for this player."
                    )

                else:

                    stats = goalie_stats.iloc[0]


                    # -----------------------------------------
                    # KPI ROW 1
                    # -----------------------------------------

                    kpi1, kpi2, kpi3, kpi4 = st.columns(4)


                    with kpi1:

                        gp = stats["games_played"]

                        if pd.isna(gp):
                            gp = 0
                        else:
                            gp = int(gp)

                        st.metric(
                            "Games Played",
                            gp
                        )


                    with kpi2:

                        wins = stats["wins"]

                        if pd.isna(wins):
                            wins = 0
                        else:
                            wins = int(wins)

                        st.metric(
                            "Wins",
                            wins
                        )


                    with kpi3:

                        losses = stats["losses"]

                        if pd.isna(losses):
                            losses = 0
                        else:
                            losses = int(losses)

                        st.metric(
                            "Losses",
                            losses
                        )


                    with kpi4:

                        shutouts = stats["shutouts"]

                        if pd.isna(shutouts):
                            shutouts = 0
                        else:
                            shutouts = int(shutouts)

                        st.metric(
                            "Shutouts",
                            shutouts
                        )


                    # -----------------------------------------
                    # KPI ROW 2
                    # -----------------------------------------

                    kpi5, kpi6, kpi7, kpi8 = st.columns(4)


                    with kpi5:

                        save_pct = stats["save_pct"]

                        if pd.isna(save_pct):

                            save_display = "N/A"

                        else:

                            save_display = f"{float(save_pct):.3f}"


                        st.metric(
                            "Save %",
                            save_display
                        )


                    with kpi6:

                        gaa = stats["goals_against_avg"]

                        if pd.isna(gaa):

                            gaa_display = "N/A"

                        else:

                            gaa_display = f"{float(gaa):.2f}"


                        st.metric(
                            "GAA",
                            gaa_display
                        )


                    with kpi7:

                        saves = stats["saves"]

                        if pd.isna(saves):
                            saves = 0
                        else:
                            saves = int(saves)

                        st.metric(
                            "Saves",
                            saves
                        )


                    with kpi8:

                        ot_losses = stats["ot_losses"]

                        if pd.isna(ot_losses):
                            ot_losses = 0
                        else:
                            ot_losses = int(ot_losses)

                        st.metric(
                            "OT Losses",
                            ot_losses
                        )


            st.markdown("---")


            # =================================================
            # 10. PLAYER GAME STATISTICS
            # =================================================

            st.subheader("Game Statistics")


            game_stats = pd.read_sql("""
                SELECT
                    gs.game_id AS Game_ID,
                    g.game_date AS Game_Date,

                    CONCAT(
                        ht.team_abbrv,
                        ' vs ',
                        at.team_abbrv
                    ) AS Game_Match,

                    gs.goals AS Goals,
                    gs.assists AS Assists,
                    gs.points AS Points,
                    gs.shots_on_goal AS Shots,
                    gs.penalty_min AS Penalty_Min,
                    gs.toi AS TOI,
                    gs.plus_minus AS Plus_Minus

                FROM game_stats gs

                INNER JOIN games g
                    ON gs.game_id = g.game_id

                INNER JOIN teams ht
                    ON g.home_team_id = ht.team_id

                INNER JOIN teams at
                    ON g.away_team_id = at.team_id

                WHERE gs.player_id = %s

                ORDER BY
                    g.game_date DESC;
            """, conn, params=[player_id])


            if game_stats.empty:

                st.info(
                    "No game statistics available for this player."
                )

            else:

                st.dataframe(
                    game_stats,
                    use_container_width=True,
                    hide_index=True
                )


    except Exception as e:

        st.error(
            f"Unable to load player information: {e}"
        )

# =========================================================
# GAME RESULTS PAGE
# =========================================================

if selected == "Game Results":

    st.title("🏒 Game Results")
    st.write("Browse NHL games using date, team, game type and game state filters")


    # =========================================================
    # 1. FILTER OPTIONS
    # =========================================================

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)


    # =========================================================
    # TEAM FILTER
    # =========================================================

    with filter_col1:

        team_list = pd.read_sql("""
            SELECT
                team_id,
                team_name
            FROM teams
            ORDER BY team_name;
        """, conn)


        team_options = ["All Teams"] + team_list["team_name"].tolist()


        selected_team = st.selectbox(
            "Select Team",
            team_options
        )


    # =========================================================
    # GAME TYPE FILTER
    # =========================================================

    with filter_col2:

        game_type_options = {
            "All Game Types": None,
            "Preseason": 1,
            "Regular Season": 2,
            "Playoffs": 3
        }


        selected_game_type = st.selectbox(
            "Select Game Type",
            list(game_type_options.keys())
        )


    # =========================================================
    # GAME STATE FILTER
    # =========================================================

    with filter_col3:

        game_state_options = [
            "All Game States",
            "Final",
            "Upcoming",
            "In Progress"
        ]


        selected_game_state = st.selectbox(
            "Select Game State",
            game_state_options
        )


    # =========================================================
    # DATE FILTER
    # =========================================================

    with filter_col4:

        date_filter = st.radio(
            "Date Filter",
            [
                "All Dates",
                "Select Date"
            ],
            horizontal=True
        )


    selected_date = None


    if date_filter == "Select Date":

        selected_date = st.date_input(
            "Choose Game Date"
        )


    st.markdown("---")


    # =========================================================
    # 2. BUILD DYNAMIC SQL QUERY
    # =========================================================

    query = """
        SELECT

            g.game_id AS Game_ID,

            g.game_date AS Game_Date,

            CASE
                WHEN g.game_type = 1 THEN 'Preseason'
                WHEN g.game_type = 2 THEN 'Regular Season'
                WHEN g.game_type = 3 THEN 'Playoffs'
                ELSE 'Unknown'
            END AS Game_Type,

            ht.team_abbrv AS Home_Team,

            ht.team_name AS Home_Team_Name,

            g.home_score AS Home_Score,

            at.team_abbrv AS Away_Team,

            at.team_name AS Away_Team_Name,

            g.away_score AS Away_Score,

            CASE
                WHEN g.game_state = 'OFF' THEN 'Final'
                WHEN g.game_state = 'FUT' THEN 'Upcoming'
                WHEN g.game_state = 'LIVE' THEN 'In Progress'
                ELSE g.game_state
            END AS Game_State,

            g.venue_name AS Venue

        FROM games g

        INNER JOIN teams ht
            ON g.home_team_id = ht.team_id

        INNER JOIN teams at
            ON g.away_team_id = at.team_id

        WHERE 1 = 1
    """


    params = []


    # =========================================================
    # TEAM FILTER
    # =========================================================

    if selected_team != "All Teams":

        query += """
            AND (
                ht.team_name = %s
                OR at.team_name = %s
            )
        """

        params.extend([
            selected_team,
            selected_team
        ])


    # =========================================================
    # GAME TYPE FILTER
    # =========================================================

    if selected_game_type != "All Game Types":

        query += """
            AND g.game_type = %s
        """

        params.append(
            game_type_options[selected_game_type]
        )


    # =========================================================
    # GAME STATE FILTER
    # =========================================================

    if selected_game_state != "All Game States":

        state_mapping = {
            "Final": "OFF",
            "Upcoming": "FUT",
            "In Progress": "LIVE"
        }

        query += """
            AND g.game_state = %s
        """

        params.append(
            state_mapping[selected_game_state]
        )


    # =========================================================
    # DATE FILTER
    # =========================================================

    if selected_date is not None:

        query += """
            AND g.game_date = %s
        """

        params.append(
            selected_date
        )


    # =========================================================
    # ORDER RESULTS
    # =========================================================

    query += """
        ORDER BY
            g.game_date DESC,
            g.game_id DESC;
    """


    # =========================================================
    # 3. EXECUTE QUERY
    # =========================================================

    try:

        games_df = pd.read_sql(
            query,
            conn,
            params=params
        )


        # =====================================================
        # 4. KPI INFORMATION
        # =====================================================

        total_games = len(games_df)


        if total_games > 0:

            completed_games = len(
                games_df[
                    games_df["Game_State"] == "Final"
                ]
            )


            upcoming_games = len(
                games_df[
                    games_df["Game_State"] == "Upcoming"
                ]
            )


            live_games = len(
                games_df[
                    games_df["Game_State"] == "In Progress"
                ]
            )


        else:

            completed_games = 0
            upcoming_games = 0
            live_games = 0


        # =====================================================
        # 5. KPI CARDS
        # =====================================================

        st.subheader("Game Overview")


        kpi1, kpi2, kpi3, kpi4 = st.columns(4)


        with kpi1:

            st.metric(
                "Total Games",
                total_games
            )


        with kpi2:

            st.metric(
                "Completed Games",
                completed_games
            )


        with kpi3:

            st.metric(
                "Upcoming Games",
                upcoming_games
            )


        with kpi4:

            st.metric(
                "Games In Progress",
                live_games
            )


        st.markdown("---")


        # =====================================================
        # 6. GAME RESULTS TABLE
        # =====================================================

        st.subheader("Game Results")


        if games_df.empty:

            st.warning(
                "No games found for the selected filters."
            )

        else:

            display_df = games_df[
                [
                    "Game_ID",
                    "Game_Date",
                    "Game_Type",
                    "Home_Team",
                    "Home_Team_Name",
                    "Home_Score",
                    "Away_Team",
                    "Away_Team_Name",
                    "Away_Score",
                    "Game_State",
                    "Venue"
                ]
            ]


            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )


    except Exception as e:

        st.error(
            f"Unable to load game results: {e}"
        )

# =========================================================
# LEADERBOARDS PAGE
# =========================================================

if selected == "Leaderboards":

    # ---------------------------------------------------------
    # CSS - Show full player/goalie names in metric cards
    # ---------------------------------------------------------

    st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 20px !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    </style>
    """, unsafe_allow_html=True)


    st.title("🏆 Leaderboards")

    st.write(
        "Explore the leading NHL players across different "
        "season performance categories"
    )


    # =========================================================
    # 1. SELECT LEADERBOARD TYPE
    # =========================================================

    leaderboard_type = st.selectbox(
        "Select Leaderboard",
        (
            "Top Point Scorers",
            "Top Goal Scorers",
            "Top Assist Leaders",
            "Plus / Minus Leaders",
            "Most Shots",
            "Most Penalty Minutes",
            "Top Goalie Wins",
            "Best Save Percentage",
            "Most Shutouts"
        )
    )


    st.markdown("---")


    # =========================================================
    # 2. TOP POINT SCORERS
    # =========================================================

    if leaderboard_type == "Top Point Scorers":

        st.subheader("🏒 Top Point Scorers")


        df = pd.read_sql("""
            SELECT
                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS Player,

                t.team_abbrv AS Team,

                p.position AS Position,

                s.games_played AS GP,

                s.goals AS Goals,

                s.assists AS Assists,

                s.points AS Points

            FROM skater_season_stats s

            INNER JOIN players p
                ON s.player_id = p.player_id

            INNER JOIN teams t
                ON s.team_id = t.team_id

            WHERE s.season = '20252026'

            ORDER BY
                s.points DESC

            LIMIT 10;
        """, conn)


        if df.empty:

            st.warning(
                "No point scoring data available."
            )

        else:

            top_player = df.iloc[0]


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Top Point Scorer",
                    top_player["Player"]
                )


            with col2:

                st.metric(
                    "Points",
                    int(top_player["Points"])
                )


            with col3:

                st.metric(
                    "Team",
                    top_player["Team"]
                )


            st.markdown("---")


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    # =========================================================
    # 3. TOP GOAL SCORERS
    # =========================================================

    elif leaderboard_type == "Top Goal Scorers":

        st.subheader("🎯 Top Goal Scorers")


        df = pd.read_sql("""
            SELECT
                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS Player,

                t.team_abbrv AS Team,

                p.position AS Position,

                s.games_played AS GP,

                s.goals AS Goals,

                s.assists AS Assists,

                s.points AS Points

            FROM skater_season_stats s

            INNER JOIN players p
                ON s.player_id = p.player_id

            INNER JOIN teams t
                ON s.team_id = t.team_id

            WHERE s.season = '20252026'

            ORDER BY
                s.goals DESC

            LIMIT 10;
        """, conn)


        if df.empty:

            st.warning(
                "No goal scoring data available."
            )

        else:

            top_player = df.iloc[0]


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Top Goal Scorer",
                    top_player["Player"]
                )


            with col2:

                st.metric(
                    "Goals",
                    int(top_player["Goals"])
                )


            with col3:

                st.metric(
                    "Team",
                    top_player["Team"]
                )


            st.markdown("---")


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    # =========================================================
    # 4. TOP ASSIST LEADERS
    # =========================================================

    elif leaderboard_type == "Top Assist Leaders":

        st.subheader("🅰️ Top Assist Leaders")


        df = pd.read_sql("""
            SELECT
                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS Player,

                t.team_abbrv AS Team,

                p.position AS Position,

                s.games_played AS GP,

                s.goals AS Goals,

                s.assists AS Assists,

                s.points AS Points

            FROM skater_season_stats s

            INNER JOIN players p
                ON s.player_id = p.player_id

            INNER JOIN teams t
                ON s.team_id = t.team_id

            WHERE s.season = '20252026'

            ORDER BY
                s.assists DESC

            LIMIT 10;
        """, conn)


        if df.empty:

            st.warning(
                "No assist data available."
            )

        else:

            top_player = df.iloc[0]


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Assist Leader",
                    top_player["Player"]
                )


            with col2:

                st.metric(
                    "Assists",
                    int(top_player["Assists"])
                )


            with col3:

                st.metric(
                    "Team",
                    top_player["Team"]
                )


            st.markdown("---")


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    # =========================================================
    # 5. PLUS / MINUS LEADERS
    # =========================================================

    elif leaderboard_type == "Plus / Minus Leaders":

        st.subheader("💪 Plus / Minus Leaders")


        df = pd.read_sql("""
            SELECT
                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS Player,

                t.team_abbrv AS Team,

                p.position AS Position,

                s.games_played AS GP,

                s.plus_minus AS Plus_Minus,

                s.points AS Points

            FROM skater_season_stats s

            INNER JOIN players p
                ON s.player_id = p.player_id

            INNER JOIN teams t
                ON s.team_id = t.team_id

            WHERE s.season = '20252026'

            ORDER BY
                s.plus_minus DESC

            LIMIT 10;
        """, conn)


        if df.empty:

            st.warning(
                "No plus/minus data available."
            )

        else:

            top_player = df.iloc[0]


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Plus / Minus Leader",
                    top_player["Player"]
                )


            with col2:

                st.metric(
                    "Plus / Minus",
                    int(top_player["Plus_Minus"])
                )


            with col3:

                st.metric(
                    "Team",
                    top_player["Team"]
                )


            st.markdown("---")


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    # =========================================================
    # 6. MOST SHOTS
    # =========================================================

    elif leaderboard_type == "Most Shots":

        st.subheader("⚡ Most Shots")


        df = pd.read_sql("""
            SELECT
                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS Player,

                t.team_abbrv AS Team,

                p.position AS Position,

                s.games_played AS GP,

                s.shots AS Shots,

                s.goals AS Goals,

                s.points AS Points

            FROM skater_season_stats s

            INNER JOIN players p
                ON s.player_id = p.player_id

            INNER JOIN teams t
                ON s.team_id = t.team_id

            WHERE s.season = '20252026'

            ORDER BY
                s.shots DESC

            LIMIT 10;
        """, conn)


        if df.empty:

            st.warning(
                "No shot data available."
            )

        else:

            top_player = df.iloc[0]


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Most Shots",
                    top_player["Player"]
                )


            with col2:

                st.metric(
                    "Shots",
                    int(top_player["Shots"])
                )


            with col3:

                st.metric(
                    "Team",
                    top_player["Team"]
                )


            st.markdown("---")


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    # =========================================================
    # 7. MOST PENALTY MINUTES
    # =========================================================

    elif leaderboard_type == "Most Penalty Minutes":

        st.subheader("🚨 Most Penalty Minutes")


        df = pd.read_sql("""
            SELECT
                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS Player,

                t.team_abbrv AS Team,

                p.position AS Position,

                s.games_played AS GP,

                s.penalty_min AS Penalty_Minutes,

                s.goals AS Goals,

                s.points AS Points

            FROM skater_season_stats s

            INNER JOIN players p
                ON s.player_id = p.player_id

            INNER JOIN teams t
                ON s.team_id = t.team_id

            WHERE s.season = '20252026'

            ORDER BY
                s.penalty_min DESC

            LIMIT 10;
        """, conn)


        if df.empty:

            st.warning(
                "No penalty minute data available."
            )

        else:

            top_player = df.iloc[0]


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Most Penalty Minutes",
                    top_player["Player"]
                )


            with col2:

                st.metric(
                    "Penalty Minutes",
                    int(top_player["Penalty_Minutes"])
                )


            with col3:

                st.metric(
                    "Team",
                    top_player["Team"]
                )


            st.markdown("---")


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    # =========================================================
    # 8. TOP GOALIE WINS
    # =========================================================

    elif leaderboard_type == "Top Goalie Wins":

        st.subheader("🥅 Top Goalie Wins")


        df = pd.read_sql("""
            SELECT
                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS Goalie,

                t.team_abbrv AS Team,

                g.games_played AS GP,

                g.wins AS Wins,

                g.losses AS Losses,

                g.ot_losses AS OT_Losses,

                g.save_pct AS Save_Pct,

                g.goals_against_avg AS GAA,

                g.shutouts AS Shutouts

            FROM goalie_season_stats g

            INNER JOIN players p
                ON g.player_id = p.player_id

            INNER JOIN teams t
                ON g.team_id = t.team_id

            WHERE g.season = '20252026'

            ORDER BY
                g.wins DESC

            LIMIT 10;
        """, conn)


        if df.empty:

            st.warning(
                "No goalie win data available."
            )

        else:

            top_goalie = df.iloc[0]


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Top Winning Goalie",
                    top_goalie["Goalie"]
                )


            with col2:

                wins = top_goalie["Wins"]

                if pd.isna(wins):
                    wins = 0
                else:
                    wins = int(wins)

                st.metric(
                    "Wins",
                    wins
                )


            with col3:

                st.metric(
                    "Team",
                    top_goalie["Team"]
                )


            st.markdown("---")


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    # =========================================================
    # 9. BEST SAVE PERCENTAGE
    # =========================================================

    elif leaderboard_type == "Best Save Percentage":

        st.subheader("🧤 Best Save Percentage")


        df = pd.read_sql("""
            SELECT
                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS Goalie,

                t.team_abbrv AS Team,

                g.games_played AS GP,

                g.save_pct AS Save_Pct,

                g.goals_against_avg AS GAA,

                g.wins AS Wins,

                g.shutouts AS Shutouts

            FROM goalie_season_stats g

            INNER JOIN players p
                ON g.player_id = p.player_id

            INNER JOIN teams t
                ON g.team_id = t.team_id

            WHERE g.season = '20252026'
              AND g.save_pct IS NOT NULL

            ORDER BY
                g.save_pct DESC

            LIMIT 10;
        """, conn)


        if df.empty:

            st.warning(
                "No save percentage data available."
            )

        else:

            top_goalie = df.iloc[0]


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Best Save Percentage",
                    top_goalie["Goalie"]
                )


            with col2:

                save_pct = top_goalie["Save_Pct"]

                if pd.isna(save_pct):

                    save_display = "N/A"

                else:

                    save_display = f"{float(save_pct):.3f}"


                st.metric(
                    "Save %",
                    save_display
                )


            with col3:

                st.metric(
                    "Team",
                    top_goalie["Team"]
                )


            st.markdown("---")


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    # =========================================================
    # 10. MOST SHUTOUTS
    # =========================================================

    elif leaderboard_type == "Most Shutouts":

        st.subheader("🏆 Most Shutouts")


        df = pd.read_sql("""
            SELECT
                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS Goalie,

                t.team_abbrv AS Team,

                g.games_played AS GP,

                g.shutouts AS Shutouts,

                g.wins AS Wins,

                g.save_pct AS Save_Pct,

                g.goals_against_avg AS GAA

            FROM goalie_season_stats g

            INNER JOIN players p
                ON g.player_id = p.player_id

            INNER JOIN teams t
                ON g.team_id = t.team_id

            WHERE g.season = '20252026'

            ORDER BY
                g.shutouts DESC

            LIMIT 10;
        """, conn)


        if df.empty:

            st.warning(
                "No shutout data available."
            )

        else:

            top_goalie = df.iloc[0]


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Most Shutouts",
                    top_goalie["Goalie"]
                )


            with col2:

                shutouts = top_goalie["Shutouts"]

                if pd.isna(shutouts):
                    shutouts = 0
                else:
                    shutouts = int(shutouts)

                st.metric(
                    "Shutouts",
                    shutouts
                )


            with col3:

                st.metric(
                    "Team",
                    top_goalie["Team"]
                )


            st.markdown("---")


            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


# =========================================================
# GOALIE CENTER PAGE
# =========================================================

if selected == "Goalie Center":

    st.title("🥅 Goalie Center")

    st.write(
        "View goalie information and season performance."
    )


    # =========================================================
    # 1. GET GOALIES
    # =========================================================

    try:

        goalies = pd.read_sql("""
            SELECT DISTINCT
                p.player_id,
                CONCAT(
                    p.first_name,
                    ' ',
                    p.last_name
                ) AS Goalie

            FROM players p

            INNER JOIN goalie_season_stats g
                ON p.player_id = g.player_id

            WHERE p.position = 'G'

            ORDER BY Goalie;
        """, conn)


        if goalies.empty:

            st.warning(
                "No goalie information available."
            )

        else:

            # =================================================
            # 2. GOALIE SELECTION
            # =================================================

            selected_goalie = st.selectbox(
                "Select Goalie",
                goalies["Goalie"].tolist()
            )


            # Get selected goalie's player ID

            selected_player_id = goalies.loc[
                goalies["Goalie"] == selected_goalie,
                "player_id"
            ].iloc[0]


            # =================================================
            # 3. GOALIE INFORMATION
            # =================================================

            goalie_info = pd.read_sql("""
                SELECT
                    CONCAT(
                        p.first_name,
                        ' ',
                        p.last_name
                    ) AS Goalie,

                    t.team_name AS Team,

                    t.team_abbrv AS Team_Abbreviation,

                    p.jersey_number AS Jersey_Number,

                    p.birth_date AS Birth_Date,

                    p.birth_country AS Birth_Country,

                    p.height_cm AS Height_CM,

                    p.weight_kg AS Weight_KG,

                    p.shoots_catches AS Catches,

                    p.headshot_url AS Headshot

                FROM players p

                INNER JOIN teams t
                    ON p.team_id = t.team_id

                WHERE p.player_id = %s;
            """, conn, params=(selected_player_id,))


            if not goalie_info.empty:

                goalie = goalie_info.iloc[0]


                st.markdown("---")


                # =================================================
                # 4. GOALIE DETAILS
                # =================================================

                col1, col2 = st.columns([1, 3])


                with col1:

                    if (
                        pd.notna(goalie["Headshot"])
                        and str(goalie["Headshot"]).strip() != ""
                    ):

                        st.image(
                            goalie["Headshot"],
                            width=150
                        )


                with col2:

                    st.subheader(
                        goalie["Goalie"]
                    )

                    st.write(
                        f"**Team:** {goalie['Team']}"
                    )

                    st.write(
                        f"**Team:** {goalie['Team_Abbreviation']}"
                    )


                st.markdown("---")


                # =================================================
                # 5. BASIC INFORMATION
                # =================================================

                st.subheader("Goalie Information")


                info_col1, info_col2, info_col3, info_col4 = st.columns(4)


                with info_col1:

                    st.write("**Jersey Number**")

                    jersey = goalie["Jersey_Number"]

                    if pd.isna(jersey):
                        st.write("N/A")
                    else:
                        st.write(int(jersey))


                with info_col2:

                    st.write("**Birth Date**")

                    birth_date = goalie["Birth_Date"]

                    if pd.isna(birth_date):

                        st.write("N/A")

                    else:

                        st.write(
                            pd.to_datetime(
                                birth_date
                            ).strftime("%Y-%m-%d")
                        )


                with info_col3:

                    st.write("**Birth Country**")

                    if pd.isna(goalie["Birth_Country"]):

                        st.write("N/A")

                    else:

                        st.write(
                            goalie["Birth_Country"]
                        )


                with info_col4:

                    st.write("**Catches**")

                    if pd.isna(goalie["Catches"]):

                        st.write("N/A")

                    else:

                        st.write(
                            goalie["Catches"]
                        )


                st.markdown("---")


                # =================================================
                # 6. SEASON STATISTICS
                # =================================================

                st.subheader(
                    "Season Statistics"
                )


                season_stats = pd.read_sql("""
                    SELECT

                        g.season AS Season,

                        g.games_played AS GP,

                        g.wins AS Wins,

                        g.losses AS Losses,

                        g.ot_losses AS OT_Losses,

                        g.save_pct AS Save_Pct,

                        g.goals_against_avg AS GAA,

                        g.shutouts AS Shutouts,

                        g.saves AS Saves

                    FROM goalie_season_stats g

                    WHERE g.player_id = %s

                    ORDER BY g.season DESC;
                """, conn, params=(selected_player_id,))


                if season_stats.empty:

                    st.info(
                        "No season statistics available for this goalie."
                    )

                else:

                    # Format Save Percentage

                    season_stats["Save_Pct"] = season_stats[
                        "Save_Pct"
                    ].apply(
                        lambda x:
                        f"{float(x):.3f}"
                        if pd.notna(x)
                        else "N/A"
                    )


                    # Format GAA

                    season_stats["GAA"] = season_stats[
                        "GAA"
                    ].apply(
                        lambda x:
                        f"{float(x):.2f}"
                        if pd.notna(x)
                        else "N/A"
                    )


                    st.dataframe(
                        season_stats,
                        use_container_width=True,
                        hide_index=True
                    )


    except Exception as e:

        st.error(
            f"Unable to load goalie information: {e}"
        )

# =========================================================
# GAME DETAILS PAGE
# =========================================================

if selected == "Game Details":

    st.title("🏒 Game Details")

    st.write(
        "View complete information and player statistics "
        "for a selected game."
    )


    # =========================================================
    # 1. GET AVAILABLE GAMES
    # =========================================================

    try:

        games_list = pd.read_sql("""
            SELECT
                g.game_id,
                g.game_date,

                CONCAT(
                    ht.team_name,
                    ' vs ',
                    at.team_name
                ) AS Game

            FROM games g

            INNER JOIN teams ht
                ON g.home_team_id = ht.team_id

            INNER JOIN teams at
                ON g.away_team_id = at.team_id

            ORDER BY
                g.game_date DESC;
        """, conn)


        if games_list.empty:

            st.warning(
                "No game information available."
            )

        else:

            # =================================================
            # 2. SELECT GAME
            # =================================================

            game_options = games_list.apply(
                lambda row:
                f"{row['game_date']} | "
                f"{row['Game']} | "
                f"ID: {row['game_id']}",
                axis=1
            ).tolist()


            selected_game = st.selectbox(
                "Select Game",
                game_options
            )


            selected_game_id = games_list.loc[
                games_list.apply(
                    lambda row:
                    f"{row['game_date']} | "
                    f"{row['Game']} | "
                    f"ID: {row['game_id']}",
                    axis=1
                ) == selected_game,
                "game_id"
            ].iloc[0]


            st.markdown("---")


            # =================================================
            # 3. GAME INFORMATION
            # =================================================

            game_info = pd.read_sql("""
                SELECT

                    g.game_id AS Game_ID,

                    g.season AS Season,

                    g.game_type AS Game_Type,

                    g.game_date AS Game_Date,

                    g.game_state AS Game_State,

                    g.venue_name AS Venue,

                    ht.team_name AS Home_Team,

                    ht.team_abbrv AS Home_Abbreviation,

                    ht.logo AS Home_Logo,

                    at.team_name AS Away_Team,

                    at.team_abbrv AS Away_Abbreviation,

                    at.logo AS Away_Logo,

                    g.home_score AS Home_Score,

                    g.away_score AS Away_Score

                FROM games g

                INNER JOIN teams ht
                    ON g.home_team_id = ht.team_id

                INNER JOIN teams at
                    ON g.away_team_id = at.team_id

                WHERE g.game_id = %s;
            """, conn, params=(selected_game_id,))


            if game_info.empty:

                st.warning(
                    "No details found for the selected game."
                )

            else:

                game = game_info.iloc[0]


                # =================================================
                # 4. GAME INFORMATION
                # =================================================

                st.subheader("Game Information")


                info_col1, info_col2, info_col3, info_col4 = st.columns(4)


                with info_col1:

                    st.write("**Game Date**")

                    if pd.isna(game["Game_Date"]):

                        st.write("N/A")

                    else:

                        st.write(
                            pd.to_datetime(
                                game["Game_Date"]
                            ).strftime("%Y-%m-%d")
                        )


                with info_col2:

                    st.write("**Season**")

                    if pd.isna(game["Season"]):

                        st.write("N/A")

                    else:

                        st.write(
                            game["Season"]
                        )


                with info_col3:

                    st.write("**Game Type**")

                    game_type = game["Game_Type"]

                    if game_type == 1:

                        game_type_text = "Preseason"

                    elif game_type == 2:

                        game_type_text = "Regular Season"

                    elif game_type == 3:

                        game_type_text = "Playoffs"

                    else:

                        game_type_text = str(game_type)

                    st.write(game_type_text)


                with info_col4:

                    st.write("**Game State**")

                    game_state = game["Game_State"]

                    if pd.isna(game_state):

                        st.write("N/A")

                    else:

                        game_state = str(game_state)

                        if game_state == "OFF":

                            st.write("Final")

                        elif game_state == "FUT":

                            st.write("Upcoming")

                        elif game_state == "LIVE":

                            st.write("Live")

                        else:

                            st.write(game_state)


                # =================================================
                # 5. VENUE
                # =================================================

                st.write("**Venue:**")

                if pd.isna(game["Venue"]):

                    st.write("N/A")

                else:

                    st.write(game["Venue"])


                st.markdown("---")


                # =================================================
                # 6. MATCH RESULT
                # =================================================

                st.subheader("Match Result")


                home_col, vs_col, away_col = st.columns(
                    [1, 1, 1]
                )


                # -------------------------------------------------
                # HOME TEAM
                # -------------------------------------------------

                with home_col:

                    if (
                        pd.notna(game["Home_Logo"])
                        and str(game["Home_Logo"]).strip() != ""
                    ):

                        st.image(
                            game["Home_Logo"],
                            width=100
                        )


                    st.markdown(
                        f"### {game['Home_Team']}"
                    )


                    st.caption(
                        game["Home_Abbreviation"]
                    )


                    home_score = game["Home_Score"]


                    if pd.isna(home_score):

                        st.metric(
                            game["Home_Team"],
                            "N/A"
                        )

                    else:

                        st.metric(
                            game["Home_Team"],
                            int(home_score)
                        )


                # -------------------------------------------------
                # VS
                # -------------------------------------------------

                with vs_col:

                    st.markdown(
                        """
                        <div style="
                            text-align:center;
                            padding-top:50px;
                        ">
                            <h2>VS</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # -------------------------------------------------
                # AWAY TEAM
                # -------------------------------------------------

                with away_col:

                    if (
                        pd.notna(game["Away_Logo"])
                        and str(game["Away_Logo"]).strip() != ""
                    ):

                        st.image(
                            game["Away_Logo"],
                            width=100
                        )


                    st.markdown(
                        f"### {game['Away_Team']}"
                    )


                    st.caption(
                        game["Away_Abbreviation"]
                    )


                    away_score = game["Away_Score"]


                    if pd.isna(away_score):

                        st.metric(
                            game["Away_Team"],
                            "N/A"
                        )

                    else:

                        st.metric(
                            game["Away_Team"],
                            int(away_score)
                        )


                st.markdown("---")


                # =================================================
                # 7. GAME SUMMARY
                # =================================================

                st.subheader("Game Summary")


                home_score = game["Home_Score"]
                away_score = game["Away_Score"]


                # -------------------------------------------------
                # DETERMINE WINNER
                # -------------------------------------------------

                if (
                    pd.notna(home_score)
                    and pd.notna(away_score)
                ):

                    if home_score > away_score:

                        winner = game["Home_Team"]

                    elif away_score > home_score:

                        winner = game["Away_Team"]

                    else:

                        winner = "Tie"

                else:

                    winner = "Not Available"


                # =================================================
                # EQUAL WIDTH SUMMARY COLUMNS
                # =================================================

                summary_col1, summary_col2, summary_col3 = st.columns(
                    [1, 1, 1]
                )


                # -------------------------------------------------
                # WINNER
                # -------------------------------------------------

                with summary_col1:

                    st.write("**Winner**")

                    st.markdown(
                        f"""
                        <div style="
                            font-size: 22px;
                            font-weight: 600;
                            line-height: 1.3;
                            word-wrap: break-word;
                            overflow-wrap: break-word;
                        ">
                            {winner}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # -------------------------------------------------
                # HOME TEAM SCORE
                # -------------------------------------------------

                with summary_col2:

                    if pd.notna(home_score):

                        st.metric(
                            game["Home_Team"],
                            int(home_score)
                        )

                    else:

                        st.metric(
                            game["Home_Team"],
                            "N/A"
                        )


                # -------------------------------------------------
                # AWAY TEAM SCORE
                # -------------------------------------------------

                with summary_col3:

                    if pd.notna(away_score):

                        st.metric(
                            game["Away_Team"],
                            int(away_score)
                        )

                    else:

                        st.metric(
                            game["Away_Team"],
                            "N/A"
                        )


                st.markdown("---")


                # =================================================
                # 8. PLAYER GAME STATISTICS
                # =================================================

                st.subheader(
                    "Player Game Statistics"
                )


                player_stats = pd.read_sql("""
                    SELECT

                        CONCAT(
                            p.first_name,
                            ' ',
                            p.last_name
                        ) AS Player,

                        t.team_abbrv AS Team,

                        p.position AS Position,

                        gs.goals AS Goals,

                        gs.assists AS Assists,

                        gs.points AS Points,

                        gs.shots_on_goal AS Shots,

                        gs.penalty_min AS PIM,

                        gs.toi AS TOI,

                        gs.plus_minus AS Plus_Minus

                    FROM game_stats gs

                    INNER JOIN players p
                        ON gs.player_id = p.player_id

                    INNER JOIN teams t
                        ON gs.team_id = t.team_id

                    WHERE gs.game_id = %s

                    ORDER BY
                        gs.points DESC,
                        gs.goals DESC,
                        gs.assists DESC;

                """, conn, params=(selected_game_id,))


                if player_stats.empty:

                    st.info(
                        "No player statistics available "
                        "for this game."
                    )

                else:

                    st.dataframe(
                        player_stats,
                        use_container_width=True,
                        hide_index=True
                    )


    except Exception as e:

        st.error(
            f"Unable to load game details: {e}"
        )

# =========================================================
# TEAM INFO PAGE
# =========================================================

if selected == "Team Info":

    st.title("🏒 Team Information")

    st.write(
        "Select a team to view its information, "
        "season performance and roster."
    )

    # =========================================================
    # 1. GET TEAMS
    # =========================================================

    try:

        teams_df = pd.read_sql("""
            SELECT
                team_id,
                team_abbrv,
                team_name,
                conference_name,
                central_name,
                logo
            FROM teams
            ORDER BY team_name;
        """, conn)

        if teams_df.empty:

            st.warning(
                "No team information available."
            )

        else:

            # =================================================
            # 2. TEAM SELECTION
            # =================================================

            team_options = teams_df["team_name"].tolist()

            selected_team = st.selectbox(
                "Select Team",
                team_options
            )

            # Get selected team's information

            team = teams_df[
                teams_df["team_name"] == selected_team
            ].iloc[0]

            team_id = int(team["team_id"])

            st.markdown("---")

            # =================================================
            # 3. TEAM OVERVIEW
            # =================================================

            st.subheader("Team Overview")

            logo_col, info_col1, info_col2, info_col3 = st.columns(
                [1, 2, 2, 2]
            )

            # -------------------------------------------------
            # TEAM LOGO
            # -------------------------------------------------

            with logo_col:

                if (
                    pd.notna(team["logo"])
                    and str(team["logo"]).strip() != ""
                ):

                    st.image(
                        team["logo"],
                        width=100
                    )

            # -------------------------------------------------
            # TEAM NAME
            # -------------------------------------------------

            with info_col1:

                st.write("**Team Name**")

                st.markdown(
                    f"""
                    <div style="
                        font-size: 22px;
                        font-weight: 600;
                        line-height: 1.3;
                        word-wrap: break-word;
                        overflow-wrap: break-word;
                    ">
                        {team["team_name"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # -------------------------------------------------
            # ABBREVIATION
            # -------------------------------------------------

            with info_col2:

                st.write("**Abbreviation**")

                st.markdown(
                    f"""
                    <div style="
                        font-size: 22px;
                        font-weight: 600;
                    ">
                        {team["team_abbrv"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # -------------------------------------------------
            # CONFERENCE
            # -------------------------------------------------

            with info_col3:

                st.write("**Conference**")

                st.markdown(
                    f"""
                    <div style="
                        font-size: 22px;
                        font-weight: 600;
                    ">
                        {team["conference_name"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("")

            # =================================================
            # DIVISION
            # =================================================

            division_col1, division_col2 = st.columns(2)

            with division_col1:

                st.write("**Division**")

                st.write(
                    team["central_name"]
                )

            with division_col2:

                st.write("**Team ID**")

                st.write(
                    team_id
                )

            st.markdown("---")

            # =================================================
            # 4. SEASON PERFORMANCE
            # =================================================

            st.subheader("Season Performance")

            standings_df = pd.read_sql("""
                SELECT
                    games_played,
                    wins,
                    losses,
                    ot_losses,
                    points,
                    goals_for,
                    goals_against,
                    home_wins,
                    away_wins,
                    streak_type,
                    streak_count,
                    season
                FROM standings
                WHERE team_id = %s
                ORDER BY season DESC
                LIMIT 1;
            """, conn, params=(team_id,))

            if standings_df.empty:

                st.info(
                    "No season performance data available "
                    "for this team."
                )

            else:

                standing = standings_df.iloc[0]

                # =============================================
                # KPI ROW 1
                # =============================================

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    games_played = standing["games_played"]

                    if pd.isna(games_played):
                        games_played = 0
                    else:
                        games_played = int(games_played)

                    st.metric(
                        "Games Played",
                        games_played
                    )

                with col2:

                    wins = standing["wins"]

                    if pd.isna(wins):
                        wins = 0
                    else:
                        wins = int(wins)

                    st.metric(
                        "Wins",
                        wins
                    )

                with col3:

                    losses = standing["losses"]

                    if pd.isna(losses):
                        losses = 0
                    else:
                        losses = int(losses)

                    st.metric(
                        "Losses",
                        losses
                    )

                with col4:

                    points = standing["points"]

                    if pd.isna(points):
                        points = 0
                    else:
                        points = int(points)

                    st.metric(
                        "Points",
                        points
                    )

                # =============================================
                # KPI ROW 2
                # =============================================

                col5, col6, col7, col8 = st.columns(4)

                with col5:

                    goals_for = standing["goals_for"]

                    if pd.isna(goals_for):
                        goals_for = 0
                    else:
                        goals_for = int(goals_for)

                    st.metric(
                        "Goals For",
                        goals_for
                    )

                with col6:

                    goals_against = standing["goals_against"]

                    if pd.isna(goals_against):
                        goals_against = 0
                    else:
                        goals_against = int(goals_against)

                    st.metric(
                        "Goals Against",
                        goals_against
                    )

                with col7:

                    home_wins = standing["home_wins"]

                    if pd.isna(home_wins):
                        home_wins = 0
                    else:
                        home_wins = int(home_wins)

                    st.metric(
                        "Home Wins",
                        home_wins
                    )

                with col8:

                    away_wins = standing["away_wins"]

                    if pd.isna(away_wins):
                        away_wins = 0
                    else:
                        away_wins = int(away_wins)

                    st.metric(
                        "Away Wins",
                        away_wins
                    )

                st.markdown("---")

                # =============================================
                # 5. CURRENT STREAK
                # =============================================

                st.subheader("Current Streak")

                streak_col1, streak_col2 = st.columns(2)

                with streak_col1:

                    streak_type = standing["streak_type"]

                    if pd.isna(streak_type):

                        streak_display = "N/A"

                    else:

                        streak_type = str(
                            streak_type
                        )

                        if streak_type == "W":

                            streak_display = "Winning Streak"

                        elif streak_type == "L":

                            streak_display = "Losing Streak"

                        elif streak_type == "OT":

                            streak_display = (
                                "Overtime Loss Streak"
                            )

                        else:

                            streak_display = streak_type

                    st.metric(
                        "Streak Type",
                        streak_display
                    )

                with streak_col2:

                    streak_count = standing["streak_count"]

                    if pd.isna(streak_count):

                        streak_count = 0

                    else:

                        streak_count = int(
                            streak_count
                        )

                    st.metric(
                        "Streak Count",
                        streak_count
                    )

            st.markdown("---")

            # =================================================
            # 6. TEAM ROSTER
            # =================================================

            st.subheader("Team Roster")

            players_df = pd.read_sql("""
                SELECT

                    CONCAT(
                        first_name,
                        ' ',
                        last_name
                    ) AS Player,

                    position AS Position,

                    jersey_number AS Jersey_Number,

                    birth_date AS Birth_Date,

                    birth_country AS Birth_Country,

                    shoots_catches AS Shoots_Catches

                FROM players

                WHERE team_id = %s

                ORDER BY
                    position,
                    jersey_number;
            """, conn, params=(team_id,))

            if players_df.empty:

                st.info(
                    "No player information available "
                    "for this team."
                )

            else:

                # =================================================
                # FORMAT BIRTH DATE
                # =================================================

                players_df["Birth_Date"] = pd.to_datetime(
                    players_df["Birth_Date"],
                    errors="coerce"
                ).dt.strftime("%Y-%m-%d")

                players_df["Birth_Date"] = (
                    players_df["Birth_Date"]
                    .fillna("N/A")
                )

                # =================================================
                # ROSTER TABLE
                # =================================================

                st.dataframe(
                    players_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("---")

                # =================================================
                # 7. PLAYERS BY POSITION
                # =================================================

                st.subheader("Players by Position")

                forwards_df = players_df[
                    players_df["Position"].isin(
                        ["C", "LW", "RW"]
                    )
                ]

                defensemen_df = players_df[
                    players_df["Position"] == "D"
                ]

                goalies_df = players_df[
                    players_df["Position"] == "G"
                ]

                # =================================================
                # FORWARDS
                # =================================================

                st.write("### 🏒 Forwards")

                if forwards_df.empty:

                    st.info(
                        "No forwards available."
                    )

                else:

                    st.dataframe(
                        forwards_df,
                        use_container_width=True,
                        hide_index=True
                    )

                # =================================================
                # DEFENSEMEN
                # =================================================

                st.write("### 🛡️ Defensemen")

                if defensemen_df.empty:

                    st.info(
                        "No defensemen available."
                    )

                else:

                    st.dataframe(
                        defensemen_df,
                        use_container_width=True,
                        hide_index=True
                    )

                # =================================================
                # GOALIES
                # =================================================

                st.write("### 🥅 Goalies")

                if goalies_df.empty:

                    st.info(
                        "No goalies available."
                    )

                else:

                    st.dataframe(
                        goalies_df,
                        use_container_width=True,
                        hide_index=True
                    )

    except Exception as e:

        st.error(
            f"Unable to load team information: {e}"
        )


    # ---------------------------------------------------------
    # QUERY EXPLORER
    # ---------------------------------------------------------
if selected == "Query Explorer":

    option = st.selectbox(
        "What would you like to explore?",
        (
            "1. Which team has scored the most total goals this season?",
            "2. Who are the top 5 point scorers across the entire league?",
            "3. Which players have scored more than 20 goals and recorded more than 30 assists in the season?",
            "4. Which teams have a season points total above the league average?",
            "5. Which divisions have an average team points total above 90?",
            "6. Which teams have the highest number of wins this season?",
            "7. Which players have scored at least 50 points this season?",
            "8. Which teams have the best home record based on home wins?",
            "9. Which teams have scored more goals than they have conceded?",
            "10. What is the total number of goals scored by each division?",
            "11. Which team has the highest average points per game?",
            "12. Which players have recorded more than 10 goals across individual games?",
            "13. Which teams have the highest number of player points in game statistics?",
            "14. Which goalies have a save percentage greater than 90%?",
            "15. Which teams have played more than 10 games and have more than 5 overtime losses?"
        )
    )

# QUERY BAR

    # Query 1
    if option == "1. Which team has scored the most total goals this season?":

        df = pd.read_sql("""
            SELECT 
                t.team_name,
                s.goals_for
            FROM teams t
            JOIN standings s 
                ON t.team_id = s.team_id
            WHERE s.season = '20252026'
            ORDER BY s.goals_for DESC
            LIMIT 1;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 2
    elif option == "2. Who are the top 5 point scorers across the entire league?":

        df = pd.read_sql("""
            SELECT 
                CONCAT(p.first_name, ' ', p.last_name) AS player_name,
                t.team_name,
                s.points
            FROM players p
            JOIN skater_season_stats s 
                ON p.player_id = s.player_id
            JOIN teams t 
                ON s.team_id = t.team_id
            WHERE s.season = '20252026'
            ORDER BY s.points DESC
            LIMIT 5;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 3
    elif option == "3. Which players have scored more than 20 goals and recorded more than 30 assists in the season?":

        df = pd.read_sql("""
            SELECT 
                CONCAT(p.first_name, ' ', p.last_name) AS player_name,
                t.team_name,
                s.goals,
                s.assists,
                s.points
            FROM players p
            JOIN skater_season_stats s 
                ON p.player_id = s.player_id
            JOIN teams t 
                ON s.team_id = t.team_id
            WHERE s.season = '20252026'
              AND s.goals > 20
              AND s.assists > 30
            ORDER BY s.points DESC;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 4
    elif option == "4. Which teams have a season points total above the league average?":

        df = pd.read_sql("""
            SELECT 
                t.team_name,
                s.points
            FROM teams t
            JOIN standings s 
                ON t.team_id = s.team_id
            WHERE s.season = '20252026'
              AND s.points > (
                  SELECT AVG(points)
                  FROM standings
                  WHERE season = '20252026'
              )
            ORDER BY s.points DESC;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 5
    elif option == "5. Which divisions have an average team points total above 90?":

        df = pd.read_sql("""
            SELECT 
                t.central_name AS division_name,
                ROUND(AVG(s.points), 2) AS average_points
            FROM teams AS t
            INNER JOIN standings AS s
                ON t.team_id = s.team_id
            WHERE s.season = '20252026'
            GROUP BY t.central_name
            HAVING AVG(s.points) > 90
            ORDER BY average_points DESC;
        """, conn)

        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 6
    elif option == "6. Which teams have the highest number of wins this season?":

        df = pd.read_sql("""
            SELECT 
                t.team_name,
                s.wins,
                s.losses,
                s.points
            FROM teams t
            JOIN standings s 
                ON t.team_id = s.team_id
            WHERE s.season = '20252026'
            ORDER BY s.wins DESC
            LIMIT 10;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 7
    elif option == "7. Which players have scored at least 50 points this season?":

        df = pd.read_sql("""
            SELECT 
                CONCAT(p.first_name, ' ', p.last_name) AS player_name,
                t.team_name,
                s.goals,
                s.assists,
                s.points
            FROM players p
            JOIN skater_season_stats s 
                ON p.player_id = s.player_id
            JOIN teams t 
                ON s.team_id = t.team_id
            WHERE s.season = '20252026'
              AND s.points >= 50
            ORDER BY s.points DESC;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 8
    elif option == "8. Which teams have the best home record based on home wins?":

        df = pd.read_sql("""
            SELECT 
                t.team_name,
                s.home_wins,
                s.wins,
                s.points
            FROM teams t
            JOIN standings s 
                ON t.team_id = s.team_id
            WHERE s.season = '20252026'
            ORDER BY s.home_wins DESC
            LIMIT 5;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 9
    elif option == "9. Which teams have scored more goals than they have conceded?":

        df = pd.read_sql("""
            SELECT 
                t.team_name,
                s.goals_for,
                s.goals_against,
                (s.goals_for - s.goals_against) AS goal_difference
            FROM teams t
            JOIN standings s 
                ON t.team_id = s.team_id
            WHERE s.season = '20252026'
              AND s.goals_for > s.goals_against
            ORDER BY goal_difference DESC;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 10
    elif option == "10. What is the total number of goals scored by each division?":

        df = pd.read_sql("""
            SELECT 
                t.central_name AS division_name,
                SUM(s.goals_for) AS total_goals
            FROM teams AS t
            INNER JOIN standings AS s
                ON t.team_id = s.team_id
            WHERE s.season = '20252026'
            GROUP BY t.central_name
            ORDER BY total_goals DESC;
        """, conn)

        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 11
    elif option == "11. Which team has the highest average points per game?":

        df = pd.read_sql("""
            SELECT 
                t.team_name,
                s.points,
                s.games_played,
                ROUND(
                    s.points / NULLIF(s.games_played, 0), 
                    2
                ) AS points_per_game
            FROM teams t
            JOIN standings s 
                ON t.team_id = s.team_id
            WHERE s.season = '20252026'
            ORDER BY points_per_game DESC
            LIMIT 5;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 12
    elif option == "12. Which players have recorded more than 10 goals across individual games?":

        df = pd.read_sql("""
            SELECT 
                CONCAT(p.first_name, ' ', p.last_name) AS player_name,
                t.team_name,
                SUM(gs.goals) AS total_goals
            FROM game_stats gs
            JOIN players p 
                ON gs.player_id = p.player_id
            JOIN teams t 
                ON gs.team_id = t.team_id
            GROUP BY 
                p.player_id,
                p.first_name,
                p.last_name,
                t.team_name
            HAVING SUM(gs.goals) > 10
            ORDER BY total_goals DESC;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 13
    elif option == "13. Which teams have the highest number of player points in game statistics?":

        df = pd.read_sql("""
            SELECT 
                t.team_name,
                SUM(gs.points) AS total_player_points
            FROM game_stats gs
            JOIN teams t 
                ON gs.team_id = t.team_id
            GROUP BY t.team_id, t.team_name
            ORDER BY total_player_points DESC
            LIMIT 10;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 14
    elif option == "14. Which goalies have a save percentage greater than 90%?":

        df = pd.read_sql("""
            SELECT 
                CONCAT(p.first_name, ' ', p.last_name) AS goalie_name,
                t.team_name,
                g.save_pct,
                g.goals_against_avg,
                g.shutouts
            FROM players p
            JOIN goalie_season_stats g 
                ON p.player_id = g.player_id
            JOIN teams t 
                ON g.team_id = t.team_id
            WHERE g.season = '20252026'
              AND g.save_pct > 0.900
            ORDER BY g.save_pct DESC;
        """, conn)
        df.index = range(1, len(df) + 1)

        st.dataframe(df)


    # Query 15
    elif option == "15. Which teams have played more than 10 games and have more than 5 overtime losses?":

        df = pd.read_sql("""
            SELECT 
                t.team_name,
                s.games_played,
                s.ot_losses,
                s.points
            FROM teams t
            JOIN standings s 
                ON t.team_id = s.team_id
            WHERE s.season = '20252026'
              AND s.games_played > 10
              AND s.ot_losses > 5
            ORDER BY s.ot_losses DESC;
        """, conn)

        df.index = range(1, len(df) + 1)

        st.dataframe(df)