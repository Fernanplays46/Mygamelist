#import random
#from mgl.domain import models, database

# Datos base para generar juegos ficticios
titles_prefix = [
    "Dragon", "Shadow", "Galaxy", "Hero", "Legend", "Eternal", "Chrono", "Mystic", "Cyber", "Steel",
    "Rogue", "Phantom", "Crystal", "Dark", "Omega", "Inferno", "Neon", "Nova", "Titan", "Vortex",
    "Star", "Blood", "Spirit", "Quantum", "Echo"
]
titles_suffix = [
    "Quest", "Saga", "Strike", "Tales", "Odyssey", "Chronicles", "Reborn", "Legacy", "Arena", "Frontier",
    "Storm", "Rebellion", "Rift", "War", "Edge", "Eclipse", "Destiny", "Rise", "Horizon", "Empire"
]
genres = ["Action", "Adventure", "RPG", "Shooter", "Strategy", "Simulation", "Platform", "Puzzle", "Roguelike"]
platforms = ["PC", "PS4", "PS5", "Xbox One", "Xbox Series X", "Nintendo Switch"]
years = list(range(2000, 2025))

# Crear 50 juegos ficticios
games_data = []
for i in range(1, 51):
    title = f"{random.choice(titles_prefix)} {random.choice(titles_suffix)} {random.randint(1, 9)}"
    genre = random.choice(genres)
    platform = random.choice(platforms)
    year = random.choice(years)
    games_data.append((title, genre, platform, year))

# Conexión a la base de datos
db = next(database.get_db())
print("📂 Conectado a la base de datos correctamente.")


added = 0
for title, genre, platform, year in games_data:
    exists = db.query(models.Game).filter_by(title=title).first()
    if not exists:
        new_game = models.Game(title=title, genre=genre, platform=platform, release_year=year)
        db.add(new_game)
        added += 1

db.commit()
print(f"✅ {added} juegos ficticios añadidos correctamente.")
