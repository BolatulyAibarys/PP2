import psycopg2
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Database init error:", e)


def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO players (username)
        VALUES (%s)
        ON CONFLICT (username) DO NOTHING;
    """, (username,))

    cur.execute("""
        SELECT id FROM players
        WHERE username = %s;
    """, (username,))

    player_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return player_id


def save_result(username, score, level_reached):
    try:
        player_id = get_or_create_player(username)

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO game_sessions (player_id, score, level_reached)
            VALUES (%s, %s, %s);
        """, (player_id, score, level_reached))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Save result error:", e)


def get_top_scores(limit=10):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                players.username,
                game_sessions.score,
                game_sessions.level_reached,
                game_sessions.played_at
            FROM game_sessions
            JOIN players ON players.id = game_sessions.player_id
            ORDER BY game_sessions.score DESC, game_sessions.level_reached DESC
            LIMIT %s;
        """, (limit,))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows
    except Exception as e:
        print("Leaderboard error:", e)
        return []


def get_personal_best(username):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT MAX(game_sessions.score)
            FROM game_sessions
            JOIN players ON players.id = game_sessions.player_id
            WHERE players.username = %s;
        """, (username,))

        result = cur.fetchone()[0]

        cur.close()
        conn.close()

        if result is None:
            return 0

        return result
    except Exception as e:
        print("Personal best error:", e)
        return 0