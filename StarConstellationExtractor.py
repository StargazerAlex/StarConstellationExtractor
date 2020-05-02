#!/usr/bin/python3

import json
from astropy import units as u
from astropy.coordinates import SkyCoord
from HTMLTableParser import HTMLTableParser

max_main_stars = 10

class Star():
    def __init__(self, star_id: int, catalogue_number: int, right_ascension: str, declination: str, visual_magnitude: float, bayer_designation:str):
        self.star_id = star_id
        self.catalogue_number = catalogue_number
        self.right_ascension = right_ascension
        self.declination = declination
        self.sky_coordinates = SkyCoord(ra=right_ascension, dec=declination, unit=(u.hourangle, u.deg))
        self.sky_coordinates.representation_type='cartesian'
        self.x = self.sky_coordinates.x
        self.y = self.sky_coordinates.y
        self.visual_magnitude = visual_magnitude
        self.bayer_designation = bayer_designation
        self.connections = []

class Connection():
    def __init__(self, origin_star: str, connected_stars: list):
        self.origin_star = origin_star
        self.connected_stars = connected_stars
        self.origin_star_id = 0
        self.connected_star_ids = []
    
    def print(self):
        print(self.origin_star, self.origin_star_id, self.connected_stars, self.connected_star_ids)

class Constellation():
    def __init__(self, latin_name: str, german_name: str, english_name: str, url: str, connection_list: list):
        self.latin_name = latin_name
        self.german_name = german_name
        self.english_name = english_name
        self.url = url
        self.connection_list = connection_list
        self.star_list = []
    
    def addStar(self, star_id: str, catalogue_number: str, right_ascension: str, declination: str, visual_magnitude: str, bayer_designation:str):
        new_star = Star(int(star_id), int(catalogue_number), right_ascension, declination, float(visual_magnitude), bayer_designation)
        self.star_list.append(new_star)
        return new_star.x, new_star.y
    
    def print(self):
        print(self.latin_name, self.german_name, self.english_name)
        print('ID', 'X', 'Y', 'Visual magnitude', 'Bayer Designation', 'Connections')
        for star in self.star_list:
            print(star.star_id, star.x, star.y, star.visual_magnitude, star.bayer_designation, star.connections)

constellation_list = [
    Constellation('Puppis', 'Achterdeck des Schiffs', 'Puppis',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APup',
    [Connection('rho', ['ksi']), Connection('ksi', ['rho', 'pi.']), Connection('pi.', ['ksi', 'zet', 'nu.']), Connection('nu.', ['pi.', 'tau']), Connection('tau', ['pi.', 'sig']), Connection('sig', ['tau', 'zet']), Connection('zet', ['sig', 'pi.'])]),
    Constellation('Aquila', 'Adler', 'Aquila',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAql',
    [Connection('alf', ['bet', 'gam', 'zet', 'del']), Connection('gam', ['alf']), Connection('bet', ['the', 'alf']), Connection('the', ['bet', 'eta']), Connection('eta', ['the', 'del']), Connection('del', ['eta', 'alf', 'zet', 'lam']), Connection('lam', ['del']), Connection('zet', ['alf', 'del'])]),
    Constellation('Ara', 'Altar', 'Ara',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAra',
    [Connection('alf', ['bet']), Connection('bet', ['alf', 'gam', 'zet']), Connection('gam', ['bet', 'del']), Connection('del', ['gam']), Connection('zet', ['eta', 'eps01']), Connection('eta', ['zet']), Connection('eps01', ['zet'])]),
    Constellation('Andromeda', 'Andromeda', 'Andromeda',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAnd',
    [Connection('alf', ['del']), Connection('del', ['alf', 'bet']), Connection('bet', ['del', 'gam']), Connection('gam', ['bet'])]),
    Constellation('Boötes', 'Bärenhüter', 'Boötes',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ABoo',
    [Connection('alf', ['eta', 'eps', 'rho']), Connection('eta', ['alf']), Connection('eps', ['alf', 'del']), Connection('del', ['eps', 'bet']), Connection('bet', ['del', 'gam']), Connection('gam', ['bet', 'rho']), Connection('rho', ['gam', 'alf'])]),
    Constellation('Crater', 'Becher', 'Crater',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACrt',
    [Connection('alf', ['bet', 'del']), Connection('bet', ['alf', 'gam']), Connection('gam', ['bet', 'del']), Connection('del', ['gam', 'alf'])]),
    Constellation('Sculptor', 'Bildhauer', 'Sculptor',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AScl',
    [Connection('alf', ['del']), Connection('del', ['alf', 'gam']), Connection('gam', ['del', 'bet']), Connection('bet', ['game'])]),
    Constellation('Chamaeleon', 'Chamäleon', 'Chamaeleon',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACha',
    [Connection('alf', ['gam']), Connection('gam', ['alf', 'del01']), Connection('del01', ['gam'])]),
    Constellation('Fornax', 'Chemischer Ofen', 'Fornax',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AFor',
    [Connection('alf', ['bet']), Connection('bet', ['alf'])]),
    Constellation('Delphinus', 'Delphin', 'Delphinus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ADel',
    [Connection('alf', ['bet', 'gam']), Connection('bet', ['alf', 'eps', 'del']), Connection('eps', ['bet']), Connection('del', ['bet', 'gam']), Connection('gam', ['alf', 'del'])]),
    Constellation('Draco', 'Drache', 'Draco',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ADra',
    [Connection('lam', ['kap']), Connection('kap', ['lam', 'alf']), Connection('alf', ['kap', 'iot']), Connection('iot', ['alf', 'the']), Connection('the', ['iot', 'eta']), Connection('eta', ['the', 'zet']), Connection('zet', ['eta', 'chi']), Connection('chi', ['zet', 'eps']), Connection('eps', ['chi', 'del']), Connection('del', ['eps', 'ksi']), Connection('ksi', ['del', 'nu.01', 'gam']), Connection('nu.01', ['ksi', 'bet']), Connection('bet', ['nu.01', 'gam']), Connection('gam', ['ksi', 'bet'])]),
    Constellation('Triangulum', 'Dreieck', 'Triangulum',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ATri',
    [Connection('alf', ['bet', 'gam']), Connection('bet', ['alf', 'gam']), Connection('gam', ['alf', 'bet'])]),
    Constellation('Lacerta', 'Eidechse', 'Lacerta',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ALac',
    [Connection('bet', ['alf'])]),  # Missing Bayer designations (broken)
    Constellation('Monoceros', 'Einhorn', 'Monoceros',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AMon',
    [Connection('alf', ['del']), Connection('del', ['alf', 'bet']), Connection('bet', ['del', 'gam']), Connection('gam', ['bet'])]),
    Constellation('Eridanus', 'Eridanus', 'Eridanus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AEri',
    [Connection('bet', ['gam']), Connection('gam', ['bet', 'del']), Connection('del', ['gam', 'tau04']), Connection('tau04', ['del', 'ups04']), Connection('ups04', ['tau04', 'the']), Connection('the', ['ups04', 'phi']), Connection('phi', ['the', 'alf'])]),
    Constellation('Pisces', 'Fische', 'Pisces',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APsc',
    [Connection('eta', ['alf']), Connection('alf', ['eta', 'gam']), Connection('gam', ['alf'])]),
    Constellation('Musca', 'Fliege', 'Musca',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AMus',
    [Connection('bet', ['del']), Connection('del', ['bet', 'alf']), Connection('alf', ['del', 'gam']), Connection('gam', ['alf'])]),
    Constellation('Volans', 'Fliegender Fisch', 'Volans',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AVol',
    [Connection('alf', ['bet']), Connection('bet', ['alf', 'eps', 'del']), Connection('eps', ['bet', 'zet']), Connection('zet', ['eps', 'gam']), Connection('gam', ['zet', 'del']), Connection('del', ['bet', 'gam'])]),
    Constellation('Vulpecula', 'Fuchs', 'Vulpecula',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AVul',
    []),    # Missing Bayer designations (broken)
    Constellation('Auriga', 'Fuhrmann', 'Auriga',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAur',
    [Connection('alf', ['eps', 'bet']), Connection('eps', ['alf', 'iot']), Connection('iot', ['eps', 'the']), Connection('the', ['iot', 'bet']), Connection('bet', ['alf', 'the'])]),
]

# Connection('', ['']), 

"""
Primary Selection:
Aquila, Ara, Auriga, Boötes, Delphinus, Draco, Eridanus, Puppis, Volans

Secondary Selection:
Monoceros, Musca, Sculptor

Tertiary Selection:
Andromeda, Crater, Chamaeleon, Fornax, Pisces, Triangulum
"""

for constellation in constellation_list:
    
    ## Download and parse constellation
    hp = HTMLTableParser()
    table = hp.parse_url(constellation.url)[8]
    x_min = 10000.0
    x_max = -10000.0
    y_min = 10000.0
    y_max = -10000.0
    last_catalogue_number = ''
    for index, row in table.iterrows():
        star_id = row[' Full\n ']
        catalogue_number = row['HD\n ']
        right_ascension = row['RAJ2000\n"h:m:s" ']
        declination = row['DEJ2000\n"d:m:s" ']
        visual_magnitude = row['Vmag\nmag ']
        bayer_designation = row['Bayer\n ']
        # Removes doubles
        if last_catalogue_number != catalogue_number:
            x, y = constellation.addStar(star_id, catalogue_number, right_ascension, declination, visual_magnitude, bayer_designation)
            last_catalogue_number = catalogue_number
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y
    
    ## Scale cartesian coordinate system
    x_target = 1920
    y_target = 1080
    border_size = 20

    # Shift coordinates into positive cartesian system
    x_shift = 0 - x_min
    y_shift = 0 - y_min
    
    # Calculate best scaling factor
    x_scaling_factor = (x_target - (border_size * 2)) / (x_max + x_shift)
    y_scaling_factor = (y_target - (border_size * 2)) / (y_max + y_shift)
    scaling_factor = 0
    if x_scaling_factor < y_scaling_factor:
        scaling_factor = x_scaling_factor
    else:
        scaling_factor = y_scaling_factor
    
    # Update coordinates for all stars
    for star in constellation.star_list:
        star.x = (star.x + x_shift) * scaling_factor + border_size
        star.y = (star.y + y_shift) * scaling_factor + border_size
    
    ## Resolve star connections
    # Map Bayer designations of connections to star ids
    for connection in constellation.connection_list:
        for origin_star in constellation.star_list:
            if connection.origin_star == origin_star.bayer_designation:
                connection.origin_star_id = origin_star.star_id
                break
        for connected_star in connection.connected_stars:
            for star in constellation.star_list:
                if connected_star == star.bayer_designation:
                    connection.connected_star_ids.append(star.star_id)
                    break
    
    #for connection in constellation.connection_list:
    #    connection.print()
    
    # Map connection star ids to stars
    for connection in constellation.connection_list:
        for origin_star in constellation.star_list:
            if connection.origin_star_id == origin_star.star_id:
                origin_star.connections = connection.connected_star_ids
                
    
    ## Print constellation
    # constellation.print()
    
    ## Write constellation to JSON
    data = {}
    data['name'] = {
        'latin': constellation.latin_name,
        'german': constellation.german_name,
        'english': constellation.english_name
    }
    data['stars'] = []
    for star in constellation.star_list:
        main_star = False
        if len(star.connections) > 0:
            main_star = True
        data['stars'].append({
            'id': star.star_id,
            'x': float(star.x),
            'y': float(star.y),
            'visualMagnitude': star.visual_magnitude,
            'bayerDesignation': star.bayer_designation,
            "mainStar": main_star,
            "connection": star.connections
        })
    
    with open('output/' + constellation.latin_name + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)