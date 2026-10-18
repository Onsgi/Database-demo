import streamlit
import duckdb

# database metadata
DATABASES = {
    "abilities": {
        "file": "abilities.duckdb",
        "table": "abilities",
        "columns": ["id", "name", "identifier", "generation_id", "is_main_series"]
    },
    "games": {
        "file": "games.duckdb",
        "table": "games",
        "columns": ["generation_id","identifier","game_type","genre","developer","publisher","cancelled","abandoned","box_art_image_path","name"]
    },
    "pokedex": {
        "file": "pokedex.duckdb",
        "table": "pokedex",
        "columns": ["id","generation_id","percentage_male","catch_rate","base_friendship_gen3_7","base_friendship_gen8","hatch_time_cycles","leveling_rate_id"]
    }
}

streamlit.title("Wow :0")
selected_db = streamlit.selectbox("Select Database", list(DATABASES.keys()))
config = DATABASES[selected_db]
streamlit.markdown(f"**Table:** `{config['table']}`")

duckDBconnecion = duckdb.connect(config["file"])
dataframe = duckDBconnecion.execute(f"SELECT * FROM {config['table']}").df()
duckDBconnecion.close()

dataframeEditor = streamlit.data_editor(
    dataframe, 
    num_rows="dynamic", 
    key=f"editor_{selected_db}"
)

#Saves the chaneges
if streamlit.button("Save Changes to the database", type="primary"):
    try:
        duckDBconnecion = duckdb.connect(config["file"])
        # shows the updated table
        duckDBconnecion.execute(f"DELETE FROM {config['table']}")
        
        if (not dataframeEditor.empty):
            placeholders = ", ".join(["?"] * len(config["columns"]))
            for _, row in dataframeEditor.iterrows():
                duckDBconnecion.execute(f"INSERT INTO {config['table']} VALUES ({placeholders})", tuple(row))
                
        duckDBconnecion.close()
        streamlit.rerun() # Tells streamlit to reload the site
    except Exception as e:
        streamlit.error(f"Error saving changes: {e}")