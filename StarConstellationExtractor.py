#!/usr/bin/python3

import json
from astropy import units as u
from astropy.coordinates import SkyCoord
from HTMLTableParser import HTMLTableParser
from PIL import Image, ImageDraw

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
    
    def getStarByStarID(self, star_id: int):
        for star in self.star_list:
            if star.star_id == star_id:
                return star
        print("WARNING: Could not find star id:", star_id)
        return None
    
    def getStarByCatalogueNumber(self, catalogue_number: int):
        for star in self.star_list:
            if star.catalogue_number == catalogue_number:
                return star
        print("WARNING: Could not find catalogue number:", catalogue_number)
        return None
    
    def drawPNG(self):
        img = Image.new('RGB', (1920, 1080), color = (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        count = 0
        for star in self.star_list:
            color_code = (255, 255, 0)
            if count < 10:
                color_code = (0, 0, 0)
            count += 1
            
            radius = int(round(10.0 - star.visual_magnitude, 2))
            x0 = star.x - radius
            x1 = star.x + radius
            y0 = star.y - radius
            y1 = star.y + radius
            draw.ellipse([(x0, y0), (x1, y1)], fill=color_code, outline=color_code)
            draw.text((x1+1,y1+1), star.bayer_designation + "," + str(star.catalogue_number), fill=color_code)
            
            for connection_id in star.connections:
                target_star = self.getStarByStarID(connection_id)
                draw.line([(star.x, star.y), (target_star.x, target_star.y)], fill =(0, 0, 0), width = 0)
        
        img.save('output/' + self.latin_name + '.png')
    
    def print(self):
        print(self.latin_name, self.german_name, self.english_name)
        print('ID', 'X', 'Y', 'Visual magnitude', 'Bayer Designation', 'Connections')
        for star in self.star_list:
            print(star.star_id, star.x, star.y, star.visual_magnitude, star.bayer_designation, star.connections)

constellation_list = [
    Constellation('Andromeda', 'Andromeda', 'Andromeda',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAnd',
    [12533, 6860, 3627, 358]),
    Constellation('Aquila', 'Adler', 'Aquila',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAql',
    []),
    Constellation('Puppis', 'Achterdeck des Schiffs', 'Puppis',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APup',
    [67523, 65228, 63700, 61555, 56855, 47670, 50310, 59717, 66811, 56855]),
    Constellation('Ara', 'Altar', 'Ara',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAra',
    []),
    Constellation('Boötes', 'Bärenhüter', 'Boötes',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ABoo',
    []),
    Constellation('Crater', 'Becher', 'Crater',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACrt',
    []),
    Constellation('Sculptor', 'Bildhauer', 'Sculptor',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AScl',
    []),
    Constellation('Chamaeleon', 'Chamäleon', 'Chamaeleon',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACha',
    []),
    Constellation('Fornax', 'Chemischer Ofen', 'Fornax',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AFor',
    []),
    Constellation('Delphinus', 'Delphin', 'Delphinus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ADel',
    []),
    Constellation('Draco', 'Drache', 'Draco',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ADra',
    []),
    Constellation('Triangulum', 'Dreieck', 'Triangulum',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ATri',
    []),
    Constellation('Lacerta', 'Eidechse', 'Lacerta',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ALac',
    []),
    Constellation('Monoceros', 'Einhorn', 'Monoceros',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AMon',
    []),
    Constellation('Eridanus', 'Eridanus', 'Eridanus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AEri',
    []),
    Constellation('Pisces', 'Fische', 'Pisces',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APsc',
    []),
    Constellation('Musca', 'Fliege', 'Musca',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AMus',
    []),
    Constellation('Volans', 'Fliegender Fisch', 'Volans',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AVol',
    []),
    Constellation('Vulpecula', 'Fuchs', 'Vulpecula',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AVul',
    []),
    Constellation('Auriga', 'Fuhrmann', 'Auriga',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAur',
    []),
]

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
    # Map Henry Draper Catalog Numbers of connections to star ids
    for index in range(len(constellation.connection_list) - 1):
        origin_star = constellation.getStarByCatalogueNumber(constellation.connection_list[index])
        target_star = constellation.getStarByCatalogueNumber(constellation.connection_list[index + 1])
        origin_star.connections.append(target_star.star_id)
    
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
    
    constellation.drawPNG()