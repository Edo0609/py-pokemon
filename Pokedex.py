import requests
import random

class Pokemon:
    def __init__(self, id = None):
        self.url = 'https://pokeapi.co/api/v2/pokemon'
        self.id = id
        self.pokemon = None
    
    def __str__(self):
        return f"{self.pokemon['name']} #ID: {self.pokemon['id']}"
    
    def get(self):
        response = requests.get(f"{self.url}/{self.id}")
        if response.ok:
            data = response.json()
            self.pokemon = {
                "name": data['name'],
                "id": data['id'],
                "abilities": [item['ability']['name'] for item in data['abilities']],
                "types": [type['type']['name'] for type in data['types']],
                "species": data['species']['url'],
                "evolution_chain": requests.get(data['species']['url']).json()['evolution_chain']['url']
            }
        else:
            print(response.status_code)
        

class Pokedex:
    def __init__(self, url):
        self.url = url
        self.pokemons = []
        
    def all(self):
        if len(self.pokemons) > 0:
            return self.pokemons
        response = requests.get(f"{self.url}?limit=151")
        if response.ok:
            data = response.json()
            self.pokemons = [item['name'] for item in data['results']]
            print(self.pokemons)
        else:
            print(response.status_code)
            self.pokemons = []
    
    def get(self, id):
        pokemon = Pokemon(id)
        pokemon.get()
        return pokemon
    
    def catch(self, pokemon):
        pokemon = (self.get(pokemon)).pokemon
        response = requests.get(pokemon['species'])
        if response.ok:
            data = response.json()
            random_number = random.randint(1, 255)
            capture_rate = data['capture_rate']
            if random_number <= capture_rate:
                print(f"You caught {pokemon['name']}!")
            else:
                print(f"{pokemon['name']} escaped!")
    
    def search(self, term):
        print(f"searching for {term} in list...")
        results = [pokemon for pokemon in self.pokemons if term.lower() in pokemon]
        print(results)
    
    def release(self, pokemon):
        pass
    
    def evolve(self, pokemon):
        pokemon = (self.get(pokemon)).pokemon
        response = requests.get(pokemon['evolution_chain'])
        if response.ok:
            chain = response.json()['chain']
            if chain['species']['name'] == pokemon['name']:
                evol = random.randint(0, len(chain['evolves_to']) - 1)
                print(f"{pokemon['name']} evolved into {chain['evolves_to'][evol]['species']['name']}!")
            elif chain['evolves_to'][0]['species']['name'] == pokemon['name']:
                print(f"{pokemon['name']} evolved into {chain['evolves_to'][0]['evolves_to'][0]['species']['name']}!")
            elif chain['evolves_to'][0]['evolves_to'][0]['species']['name'] == pokemon['name']:
                print(f"{pokemon['name']} is already fully evolved!")
        else:
            print(response.status_code)
        
    

pokedex = Pokedex('https://pokeapi.co/api/v2/pokemon')
pokedex.evolve("charmander")

