# 🏒 NHL Data Analytics Dashboard

A professional **NHL Data Analytics Dashboard** built with **Python,
Streamlit, MySQL, Pandas, and the NHL API**.

This project collects NHL team, player, standings, game, and statistical
data into a relational MySQL database and presents it through an
interactive Streamlit dashboard. Users can explore league standings,
team information, player statistics, game results, leaderboards, game
details, and predefined SQL queries through a clean multi-page
interface.

------------------------------------------------------------------------

## 📌 Project Overview

The NHL Dashboard is designed to turn raw NHL API data into an
easy-to-explore web application.

The project follows a simple data pipeline:

**NHL API → Data Processing → MySQL Database → SQL Queries → Streamlit
Dashboard**

The application focuses on structured data exploration rather than
complex analytics visualizations, making the information easy to access
through tables, filters, KPI cards, and selectable queries.

------------------------------------------------------------------------

## ✨ Key Features

-   🏠 **Home Dashboard**
    -   Overview KPIs
    -   Total teams, players, games, and goals
    -   Top point scorer
    -   Top goal scorer
    -   Best-performing goalie
    -   Team and league highlights
-   🏆 **Standings**
    -   View league standings
    -   Filter by conference
    -   Filter by division
    -   Filter by team
    -   Display wins, losses, points, goals, and streak information
-   🏒 **Team Information**
    -   Select a team
    -   View team details
    -   Conference and division information
    -   Team logo
    -   Roster information
    -   Players grouped by position
-   👤 **Player Search**
    -   Search and select players
    -   Player information
    -   Player headshot
    -   Position and jersey number
    -   Birth information
    -   Physical information
    -   Game statistics
    -   Season statistics
-   🎮 **Game Results**
    -   Browse NHL games
    -   Filter games by team
    -   Filter by game state
    -   Filter by date
    -   View home and away teams
    -   View scores and venue information
-   🏅 **Leaderboards**
    -   Top point scorers
    -   Top goal scorers
    -   Top assist leaders
    -   Plus/minus leaders
    -   Most shots
    -   Most penalty minutes
    -   Top goalie wins
    -   Best save percentage
    -   Most shutouts
-   📋 **Game Details**
    -   Detailed information for a selected game
    -   Match result
    -   Team logos
    -   Scores
    -   Winner information
    -   Game summary
    -   Venue and game status
    -   Player game statistics
-   💻 **SQL Queries**
    -   Pre-built SQL questions
    -   Select a query from a dropdown
    -   Execute SQL against the MySQL database
    -   Display query results using Streamlit tables
    -   Demonstrates SQL concepts such as:
        -   `SELECT`
        -   `WHERE`
        -   `JOIN`
        -   `GROUP BY`
        -   `HAVING`
        -   `ORDER BY`
        -   Aggregation
        -   Subqueries

------------------------------------------------------------------------

## 🗂️ Database Design

The project uses **MySQL** as the relational database.

### Tables

  Table                   Purpose
  ----------------------- -----------------------------------------------
  `teams`                 Stores NHL team information
  `standings`             Stores team standings and season performance
  `players`               Stores player information
  `games`                 Stores game and match information
  `game_stats`            Stores player performance in individual games
  `skater_season_stats`   Stores skater season statistics
  `goalie_season_stats`   Stores goalie season statistics

### Database Relationships

The database uses foreign-key relationships to connect teams, players,
games, and statistics.

-   `standings.team_id` → `teams.team_id`
-   `players.team_id` → `teams.team_id`
-   `games.home_team_id` → `teams.team_id`
-   `games.away_team_id` → `teams.team_id`
-   `game_stats.game_id` → `games.game_id`
-   `game_stats.player_id` → `players.player_id`
-   `game_stats.team_id` → `teams.team_id`
-   `skater_season_stats.player_id` → `players.player_id`
-   `skater_season_stats.team_id` → `teams.team_id`
-   `goalie_season_stats.player_id` → `players.player_id`
-   `goalie_season_stats.team_id` → `teams.team_id`

------------------------------------------------------------------------

## 🛠️ Tech Stack

### Programming Language

-   **Python**

### Dashboard

-   **Streamlit**
-   **streamlit-option-menu**

### Database

-   **MySQL**

### Data Processing

-   **Pandas**

### Database Connectivity

-   **PyMySQL**

### Data Source

-   **NHL API**

### Development Tools

-   **VS Code**
-   **Git**
-   **GitHub**

------------------------------------------------------------------------

## 🔄 Data Flow

``` text
             NHL API
                │
                ▼
        Data Collection
                │
                ▼
       Data Transformation
                │
                ▼
        MySQL Database
                │
        ┌───────┴───────┐
        ▼               ▼
   SQL Queries      Streamlit App
                        │
                        ▼
               Interactive Dashboard
```

------------------------------------------------------------------------

## 📊 SQL Query Examples

The SQL Query section includes questions such as:

### 1. Team Goal Leaders

Find the team with the highest total goals.

``` sql
SELECT
    t.team_name,
    s.goals_for AS total_goals
FROM teams t
JOIN standings s
    ON t.team_id = s.team_id
ORDER BY total_goals DESC
LIMIT 1;
```

### 2. Top Point Scorers

Find the top players based on season points.

``` sql
SELECT
    CONCAT(p.first_name, ' ', p.last_name) AS player_name,
    s.points
FROM players p
JOIN skater_season_stats s
    ON p.player_id = s.player_id
ORDER BY s.points DESC
LIMIT 5;
```

The dashboard also demonstrates filtering, multiple conditions,
aggregation, grouping, and subqueries.

------------------------------------------------------------------------

## 🖥️ Application Structure

The Streamlit application is organized into multiple pages:

``` text
NHL Dashboard
│
├── 🏠 Home
├── 🏆 Standings
├── 🏒 Team Information
├── 👤 Player Search
├── 🎮 Game Results
├── 🏅 Leaderboards
├── 📋 Game Details
└── 💻 SQL Queries
```

Sidebar navigation is implemented using `streamlit-option-menu`.

------------------------------------------------------------------------

## 🔍 Filtering

The dashboard uses interactive Streamlit controls such as:

-   `st.selectbox`
-   `st.text_input`
-   `st.radio`
-   `st.date_input`

Where applicable, filters are used to build SQL `WHERE` conditions
dynamically so that the database returns the required records rather
than loading all records and filtering them only in Pandas.

------------------------------------------------------------------------

## 📈 Dashboard Design

The dashboard uses a clean, information-focused layout with:

-   KPI cards
-   Selectable filters
-   Data tables
-   Team logos
-   Player headshots
-   Match summaries
-   Leaderboard tables
-   Sidebar navigation

The application intentionally keeps the presentation focused on **data
exploration and structured information**, rather than relying on complex
analytics visualizations.

------------------------------------------------------------------------

## ⚙️ Installation & Setup

### 1. Clone the repository

``` bash
git clone https://github.com/your-username/your-nhl-dashboard-repository.git
cd your-nhl-dashboard-repository
```

### 2. Install the required packages

``` bash
pip install streamlit pandas pymysql streamlit-option-menu requests
```

### 3. Create the MySQL database

Create a MySQL database and create the required tables:

``` text
teams
standings
players
games
game_stats
skater_season_stats
goalie_season_stats
```

### 4. Configure the database connection

Update the MySQL connection details in the application with your own:

``` python
conn = pymysql.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)
```

> For a public GitHub repository, avoid committing database passwords or
> other credentials directly into the source code.

### 5. Run the Streamlit application

``` bash
streamlit run app.py
```

The application will open in your browser.

------------------------------------------------------------------------

## 📁 Suggested Project Structure

``` text
NHL/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── ...
│
├── database/
│   └── ...
│
└── assets/
    └── ...
```

Adjust the structure according to the files used in your implementation.

------------------------------------------------------------------------

## 🎯 Project Objectives

The main objectives of this project are to:

1.  Collect NHL data from an API.
2.  Store structured data in a relational MySQL database.
3.  Establish relationships between teams, players, games, and
    statistics.
4.  Practice SQL querying and relational database concepts.
5.  Build an interactive Streamlit dashboard.
6.  Provide meaningful filters for exploring NHL data.
7.  Present team, player, game, standings, and leaderboard information
    in one application.

------------------------------------------------------------------------

## 💡 SQL Concepts Demonstrated

This project provides practical usage of:

-   Basic `SELECT` queries
-   Filtering with `WHERE`
-   Multiple conditions
-   `INNER JOIN`
-   Aggregation functions
-   `GROUP BY`
-   `HAVING`
-   `ORDER BY`
-   `LIMIT`
-   Subqueries
-   Foreign-key relationships
-   Dynamic SQL filtering

------------------------------------------------------------------------

## 🚀 Future Enhancements

Possible future improvements include:

-   Automated scheduled data updates
-   Additional NHL seasons
-   Advanced player comparison
-   Team comparison features
-   More detailed game statistics
-   Authentication and user-specific dashboards
-   Deployment to a cloud platform

------------------------------------------------------------------------

## 👩‍💻 Author

**Riya**

NHL Data Analytics Dashboard\
Built using Python, Streamlit, MySQL, Pandas, and NHL API data.

------------------------------------------------------------------------

## 📄 License

This project is intended for educational and portfolio purposes.

If you reuse or modify this project, please provide appropriate
attribution to the original author.

------------------------------------------------------------------------

## ⭐ Acknowledgements

-   **NHL** --- Data source
-   **Streamlit** --- Dashboard framework
-   **Pandas** --- Data processing
-   **MySQL** --- Relational database
-   **PyMySQL** --- Python-MySQL connectivity
