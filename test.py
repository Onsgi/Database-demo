import duckdb

connection = duckdb.connect("abilities.duckdb")
connection.execute("""
    CREATE TABLE abilities AS
    SELECT * FROM 'data_export_abilities_csv_semicolon.csv';
""")
connection.close()

connection = duckdb.connect("games.duckdb")
connection.execute("""
    CREATE TABLE games AS
    SELECT * FROM 'data_export_games_csv_comma.csv';
""")
connection.close()

connection = duckdb.connect("pokedex.duckdb")
connection.execute("""
    CREATE TABLE pokedex AS
    SELECT * FROM 'data_export_national_pokedexes_csv_comma.csv';
""")
connection.close()