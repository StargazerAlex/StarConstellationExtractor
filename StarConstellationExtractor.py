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
        self.z = self.sky_coordinates.z
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
    
    def addStar(self, star_id: str, catalogue_number: str, right_ascension: str, declination: str, visual_magnitude: str, bayer_designation: str):
        try:
            star_id = int(star_id)
            catalogue_number = int(catalogue_number)
            visual_magnitude = float(visual_magnitude)
        except ValueError:
            star_id = -1
            catalogue_number = -1
            visual_magnitude = -1.0
            print('WARNING: Invalid value conversion inside constellation', self.latin_name)
        
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
            if count < 15:
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
    Constellation('Antlia', 'Luftpumpe', 'Antlia',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAnt',
    [94890, 90610, 82150]),
    Constellation('Apus', 'Paradiesvogel', 'Apus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAps',
    [129078, 145366, 147675, 149324]),
    Constellation('Aquarius', 'Wassermann', 'Aquarius',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAqr',
    [198001, 204867, 209750, 212061, 213051, 213998, 216386, 216032, 216627, 218594]),
    Constellation('Aquila', 'Adler', 'Aquila',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAql',
    [177756, 182640, 187929, 191692, 188512, 187642, 186791, 187642, 177724, 182640, 187642]),
    Constellation('Ara', 'Altar', 'Ara',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAra',
    [158427, 157244, 157246, 158094, 157246, 157244, 152786, 152980, 152786, 151249]),
    Constellation('Aries', 'Widder', 'Aries',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAri',
    [12929, 11636]),
    Constellation('Auriga', 'Fuhrmann', 'Auriga',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AAur',
    [40312, 40183, 34029, 31964, 31398, 35497, 40312]),
    Constellation('Boötes', 'Bärenhüter', 'Boötes',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ABoo',
    [121370, 124897, 129989, 135722, 133208, 127762, 127665, 124897]),
    Constellation('Caelum', 'Grabstichel', 'Caelum',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACae',
    [28873, 29875, 29992, 32831]),
    Constellation('Camelopardalis', 'Giraffe', 'Camelopardalis',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACam',
    [30614, 31910]),
    Constellation('Cancer', 'Krebs', 'Cancer',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACnc',
    [74739, 74198, 74442, 76756, 74442, 69267]),
    Constellation('Canes Venatici', 'Jagdhunde', 'Canes Venatici',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACVn',
    [112413, 109358]),
    Constellation('Canis Major', 'Großer Hund', 'Canis Major',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACMa',
    [44743, 48915, 53138, 54605, 58350, 54605, 52877, 52089, 44402]),
    Constellation('Canis Minor', 'Kleiner Hund', 'Canis Minor',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACMi',
    [61421, 58715]),
    Constellation('Capricornus', 'Steinbock', 'Capricornus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACap',
    [192947, 193495, 200761, 203387, 206088, 207098, 204075, 198542, 197692, 194636, 193495]),
    Constellation('Carina', 'Kiel des Schiffs', 'Carina',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACar',
    [45348, 71129, 80404, 85123, 80007, 89080, 93030, 91465, 89388, 80404]),
    Constellation('Cassiopeia', 'Kassiopeia', 'Cassiopeia',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACas',
    [432, 3712, 5394, 8538, 11415]),
    Constellation('Centaurus', 'Zentaur', 'Centaurus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACen',
    [128620, 122451, 118716, 110304, 105435, 110304, 118716, 121263, 120324, 120307, 115892, 120307, 123139, 127972, 132200]),
    Constellation('Cepheus', 'Kepheus', 'Cepheus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACep',
    [198149, 203280, 210745, 213306, 216228, 222404, 205021, 203280]),
    Constellation('Cetus', 'Walfisch', 'Cetus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACet',
    [4128, 1522, 6805, 4128, 6805, 8512, 11353, 10700, 12274, 10700, 11353, 14386, 16582, 16970, 18884, 18604, 16620, 16970]),  # Two connections missing near alpha
    Constellation('Chamaeleon', 'Chamäleon', 'Chamaeleon',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACha',
    [71701, 71243, 92305, 93779]),
    Constellation('Circinus', 'Zirkel', 'Circinus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACir',
    [135379, 128898, 136415]),
    Constellation('Columba', 'Taube', 'Columba',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACol',
    [36597, 37795, 39425, 40494, 44762]),
    Constellation('Coma Berenices', 'Haar der Berenike', 'Coma Berenices',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACom',
    [114378, 114710, 108381]),
    Constellation('Corona Australis', 'Südliche Krone', 'Corona Australis',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACrA',
    [176638, 177873, 178345, 178253, 177475, 175813]),
    Constellation('Corona Borealis', 'Nördliche Krone', 'Corona Borealis',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACrB',
    [138749, 137909, 139006, 140436, 141714, 143807]),
    Constellation('Corvus', 'Rabe', 'Corvus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACrv',
    [105452, 105707, 109379, 108767, 108903, 105707]),
    Constellation('Crater', 'Becher', 'Crater',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACrt',
    [92214, 93813, 95272, 98430, 99211, 97277, 95272, 97277, 100286]),  # A couple of stars are outside the constellation itself so I am not sure if I chose the correct ones
    Constellation('Crux', 'Kreuz des Südens', 'Crux',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACru',
    [108248, 108968, 108903, 108968, 106490, 108968, 111123]),  # Is a bit crooked because I needed a star in the middle to connect to which is not actually part of the constellation
    Constellation('Cygnus', 'Schwan', 'Cygnus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ACy%2A',
    [183912, 188947, 194093, 197345, 194093, 197989, 202109, 197989, 194093, 186882, 184006, 181276]),
    Constellation('Delphinus', 'Delphin', 'Delphinus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ADel',
    [195810, 196524, 196867, 197964, 197461, 196524]),
    Constellation('Dorado', 'Schwertfisch', 'Dorado',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ADor',
    [27290, 29305, 37350, 39014]),
    Constellation('Draco', 'Drache', 'Draco',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ADra',
    [100029, 109387, 123299, 137759, 144284, 148387, 155763, 170153, 188119, 180711, 163588, 159541, 159181, 164058, 163588]),
    Constellation('Equuleus', 'Füllen', 'Equuleus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AEqu',
    [202447, 202275, 201601]),
    Constellation('Eridanus', 'Eridanus', 'Eridanus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AEri',
    [10144, 11937, 14228, 16815, 18622, 24072, 27376, 28028, 29291, 23878, 22203, 20720, 18978, 18322, 19107, 20320, 22049, 23249, 25025, 27861, 29248, 30211, 33111]), # Constellation contains a lot of minor stars, I am not sure if I got all of them correct
    Constellation('Fornax', 'Chemischer Ofen', 'Fornax',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AFor',
    [20010, 17652]),
    Constellation('Gemini', 'Zwillinge', 'Gemini',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AGem',
    [42995, 44478, 48329, 60179, 62509, 56986, 52973, 47105]),
    Constellation('Grus', 'Kranich', 'Grus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AGru',
    [215789, 214952, 213009, 209952, 213009, 211088, 209688, 207971]),
    Constellation('Hercules', 'Herkules', 'Hercules',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AHer',
    [156014, 148856, 147547, 148856, 150680, 150997, 149630, 147394, 149630, 150997, 156283, 157779, 163770, 157779, 156283, 153808, 156164, 161797, 163993, 166014, 163993, 161797, 156164, 153808, 150680]),
    Constellation('Horologium', 'Pendeluhr', 'Horologium',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AHor',
    [26967, 17051, 16555, 16920, 19319, 18866]),
    Constellation('Hydra', 'Wasserschlange', 'Hydra',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AHya',
    [123123, 115659, 103192, 100407, 96202, 93813, 90432, 88284, 85444, 81797, 79469, 76294, 74874]),   # Constellation contains a lot of minor stars, at least two of them are missing close to zeta
    Constellation('Hydrus', 'Kleine Wasserschlange', 'Hydrus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AHyi',
    [12311, 16978, 24512, 2151]),
    Constellation('Indus', 'Indianer', 'Indus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AInd',
    [196171, 197157, 198700, 202730, 209529]),   # A couple of stars are outside the constellation itself so I am not sure if I chose the correct ones
    Constellation('Lacerta', 'Eidechse', 'Lacerta',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ALac',
    [212496, 213558, 212593, 213310, 212120]),
    Constellation('Leo', 'Löwe', 'Leo',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ALeo',
    [84441, 85503, 89025, 89484, 87737, 87901, 97633, 102647, 97603, 89484]),
    Constellation('Leo Minor', 'Kleiner Löwe', 'Leo Minor',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ALMi',
    [90537, 94264]),
    Constellation('Lepus', 'Hase', 'Lepus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ALep',
    [40136, 38678, 36673, 33904, 36673, 36079, 32887, 36079, 38393, 39364]),
    Constellation('Libra', 'Waage', 'Libra',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ALib',
    [138905, 135742, 130841, 133216]),
    Constellation('Lupus', 'Wolf', 'Lupus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ALup',
    [134505, 134481, 136504, 138690, 143118, 138690, 136298, 136422, 136298, 132058, 129056]),
    Constellation('Lynx', 'Luchs', 'Lynx',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ALyn',
    [80493, 80081, 75506, 70272]),
    Constellation('Lyra', 'Leier', 'Lyra',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ALyr',
    [172167, 173648, 174638, 176437, 175588, 173648]),
    Constellation('Mensa', 'Tafelberg', 'Mensa',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AMen',
    [43834, 37763, 32440, 33285]),
    Constellation('Microscopium', 'Mikroskop', 'Microscopium',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AMic',
    [198232, 197937, 203006, 202627, 199951, 198232]),
    Constellation('Monoceros', 'Einhorn', 'Monoceros',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AMon',
    [61935, 55185, 45725, 43232]),
    Constellation('Musca', 'Fliege', 'Musca',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AMus',
    [110879, 112985, 109026, 109668, 106849, 102249]),
    Constellation('Norma', 'Winkelmaß', 'Norma',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ANor',
    [147971, 146686, 143546, 144197, 147971]),
    Constellation('Octans', 'Oktant', 'Octans',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AOct',
    [205478, 214846, 124882]),
    Constellation('Ophiuchus', 'Schlangenträger', 'Ophiuchus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AOph',
    [157056, 155125, 149757, 146791, 146051, 148857, 153210, 156247, 159561, 161096, 161868, 163917, 156897, 155125]),
    Constellation('Orion', 'Orion', 'Orion',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AOri',
    [39801, 37742, 38771, 37742, 37128, 36486, 35468, 36486, 34085]),
    Constellation('Pavo', 'Pfau', 'Pavo',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APav',
    [193924, 197051, 190248, 173948, 160635, 171759, 188228, 197051]),
    Constellation('Pegasus', 'Pegasus', 'Pegasus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APeg',
    [206778, 210418, 214923, 215648, 218045, 217906, 215182, 217906, 358, 886, 218045]),
    Constellation('Perseus', 'Perseus', 'Perseus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APer',
    [24398, 24760, 22928, 20902, 18925, 20902, 19356, 19058]),
    Constellation('Phoenix', 'Phönix', 'Phoenix',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APhe',
    [2261, 6595, 9362, 9053, 2261]),
    Constellation('Pictor', 'Maler', 'Pictor',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APic',
    [50241, 39523, 39060]),
    Constellation('Pisces', 'Fische', 'Pisces',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APsc',
    [9270, 12446, 219615]), # Constellation contains a lot of minor stars, I won't be able to get them assigned properly before the rotation works better
    Constellation('Piscis Austrinus', 'Südlicher Fisch', 'Piscis Austrinus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APsA',
    [216956, 214748, 206742, 210049, 213398, 216336, 216763, 216956]),
    Constellation('Puppis', 'Achterdeck des Schiffs', 'Puppis',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APup',
    [67523, 65228, 63700, 61555, 56855, 47670, 50310, 59717, 66811, 56855]),
    Constellation('Pyxis', 'Schiffskompass', 'Pyxis',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2APyx',
    [75691, 74575, 74006]),
    Constellation('Reticulum', 'Netz', 'Reticulum',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ARet',
    [27256, 23817, 25422, 27442, 27256]),
    Constellation('Sagitta', 'Pfeil', 'Sagitta',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ASge',
    [185758, 187076, 185958, 187076, 189319]),
    Constellation('Sagittarius', 'Schütze', 'Sagittarius',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ASgr',
    [167618, 169022, 168454, 165135, 168454, 169916, 166937, 169916, 173300, 175191, 177716, 176687, 177716, 175191, 177241, 175775]),
    Constellation('Scorpius', 'Skorpion', 'Scorpius',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ASco',
    [144217, 147165, 143275, 147165, 143018, 147165, 148478, 149438, 151680, 151890, 152334, 155203, 159532, 161471, 160578, 158926, 158408]),
    Constellation('Sculptor', 'Bildhauer', 'Sculptor',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AScl',
    [5737, 223352, 219784, 221507]),
    Constellation('Scutum', 'Schild', 'Scutum',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ASct',
    [173764, 171443, 170296]),
    Constellation('Serpens', 'Schlange', 'Serpens',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ASer',
    [141477, 141003, 141850, 141003, 138917, 140573, 141795]),
    Constellation('Sextans', 'Sextant', 'Sextans',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ASex',
    [87887, 90994, 90882, 89254, 85558, 87887]),
    Constellation('Taurus', 'Stier', 'Taurus',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ATau',
    [37202, 29139, 28319, 27371, 25204, 21364, 25204, 27371, 28305, 27045, 25604, 23630, 25604, 27045, 28305, 35497]),
    Constellation('Telescopium', 'Teleskop', 'Telescopium',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ATel',
    [169467, 169767]),  # The map does not show how the other stars are connected
    Constellation('Triangulum', 'Dreieck', 'Triangulum',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ATri',
    [11443, 13161, 14055, 11443]),
    Constellation('Triangulum Australe', 'Südliches Dreieck', 'Triangulum Australe',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ATrA',
    [150798, 141891, 135382, 150798]),
    Constellation('Tucana', 'Fliegender Fisch', 'Tucana',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2ATuc',
    [211416, 219571, 2884, 1581, 224686, 212581, 211416]),
    Constellation('Ursa Major', 'Großer Bär', 'Ursa Major',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AUMa',
    [120315, 116656, 112185, 106591, 95689, 95418, 103287, 106591]),
    Constellation('Ursa Minor', 'Kleiner Bär', 'Ursa Minor',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AUMi',
    [8890, 166205, 153751, 142105, 131873, 137422, 148048, 142105]),
    Constellation('Vela', 'Segel des Schiffs', 'Vela',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AVel',
    [93497, 86440, 81188, 78647, 81188, 74956, 68273, 78647, 82434, 88955]),
    Constellation('Virgo', 'Jungfrau', 'Virgo',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AVir',
    [102212, 102870, 107259, 110379, 112300, 113226, 112300, 110379, 114330, 116658, 114330, 118098]),
    Constellation('Volans', 'Fliegender Fisch', 'Volans',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AVol',
    [78045, 71878, 57623, 55865, 63295, 68520, 71878]),
    Constellation('Vulpecula', 'Fuchs', 'Vulpecula',
    'http://vizier.u-strasbg.fr/viz-bin/VizieR-4?-source=IV%2F27%2Fcatalog&-out.max=200&-out.all=1&-sort=Vmag&-order=I&Cst=%2AVul',
    [180554, 183439, 187811, 189849, 192806])   # The map does not show any star identifiers, I might have gotten some of them wrong
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
            'z': float(star.z),
            'visualMagnitude': star.visual_magnitude,
            'bayerDesignation': star.bayer_designation,
            "mainStar": main_star,
            "connection": star.connections
        })
    
    with open('output/' + constellation.latin_name + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=2)
    
    constellation.drawPNG()
    
    print("Constellation", constellation.latin_name, "done!")