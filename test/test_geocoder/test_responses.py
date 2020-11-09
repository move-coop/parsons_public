from collections import OrderedDict

geographies_resp = [
    {
        'matchedAddress': '1600 PENNSYLVANIA AVE NW, WASHINGTON, DC, 20500',
        'coordinates': {
            'x': -77.03535,
            'y': 38.898754},
        'tigerLine': {
            'tigerLineId': '76225813',
            'side': 'L'},
        'addressComponents': {
            'fromAddress': '1600',
            'toAddress': '1698',
            'preQualifier': '',
            'preDirection': '',
            'preType': '',
            'streetName': 'PENNSYLVANIA',
            'suffixType': 'AVE',
            'suffixDirection': 'NW',
            'suffixQualifier': '',
            'city': 'WASHINGTON',
            'state': 'DC',
            'zip': '20500'},
        'geographies': {
            '2010 Census Blocks': [{
                'SUFFIX': '',
                'GEOID': '110010062021031',
                'CENTLAT': '+38.8971157',
                'BLOCK': '1031',
                'AREAWATER': 0,
                'STATE': '11',
                'BASENAME': '1031',
                'OID': 210403964788146,
                'LSADC': 'BK',
                'FUNCSTAT': 'S',
                'INTPTLAT': '+38.8971157',
                'STGEOMETRY.AREA': 151236.97,
                'STGEOMETRY.LEN': 1505.6952,
                'NAME': 'Block 1031',
                'OBJECTID': 6398361,
                'TRACT': '006202',
                'CENTLON': '-077.0365336',
                'BLKGRP': '1',
                'AREALAND': 91475,
                'INTPTLON': '-077.0365336',
                'MTFCC': 'G5040',
                'LWBLKTYP': 'L',
                'COUNTY': '001'
            }],
            'States': [{
                'STATENS': '01702382',
                'GEOID': '11',
                'CENTLAT': '+38.9047577',
                'AREAWATER': 18687196,
                'BASENAME': 'District of Columbia',
                'STATE': '11',
                'STUSAB': 'DC',
                'OID': 27490331294090,
                'LSADC': '00',
                'FUNCSTAT': 'A',
                'INTPTLAT': '+38.9041031',
                'DIVISION': '5',
                'STGEOMETRY.AREA': 292745184.0,
                'STGEOMETRY.LEN': 86300.65,
                'NAME': 'District of Columbia',
                'REGION': '3',
                'OBJECTID': 54,
                'CENTLON': '-077.0162863',
                'AREALAND': 158340390,
                'INTPTLON': '-077.0172290',
                'MTFCC': 'G4000'
            }],
            'Counties': [{
                'GEOID': '11001',
                'CENTLAT': '+38.9047577',
                'AREAWATER': 18687196,
                'BASENAME': 'District of Columbia',
                'STATE': '11',
                'OID': 27590331264532,
                'LSADC': '00',
                'FUNCSTAT': 'F',
                'INTPTLAT': '+38.9041031',
                'STGEOMETRY.AREA': 292745184.0,
                'STGEOMETRY.LEN': 86300.65,
                'NAME': 'District of Columbia',
                'OBJECTID': 632,
                'CENTLON': '-077.0162863',
                'COUNTYCC': 'H6',
                'COUNTYNS': '01702382',
                'AREALAND': 158340390,
                'INTPTLON': '-077.0172290',
                'MTFCC': 'G4020',
                'COUNTY': '001'
            }],
            'Census Tracts': [{
                'GEOID': '11001006202',
                'CENTLAT': '+38.8801546',
                'AREAWATER': 4970897,
                'BASENAME': '62.02',
                'STATE': '11',
                'OID': 20790331304119,
                'LSADC': 'CT',
                'FUNCSTAT': 'S',
                'INTPTLAT': '+38.8809933',
                'STGEOMETRY.AREA': 19021758.0,
                'STGEOMETRY.LEN': 34175.344,
                'NAME': 'Census Tract 62.02',
                'OBJECTID': 47245,
                'TRACT': '006202',
                'CENTLON': '-077.0352173',
                'AREALAND': 6539770,
                'INTPTLON': '-077.0363219',
                'MTFCC': 'G5020',
                'COUNTY': '001'
            }]
        }
    }, {
        'matchedAddress': '1600 PENNSYLVANIA AVE SE, WASHINGTON, DC, 20003',
        'coordinates': {
            'x': -76.981895,
            'y': 38.87898},
        'tigerLine': {
            'tigerLineId': '638666807',
            'side': 'L'},
        'addressComponents': {
            'fromAddress': '1600',
            'toAddress': '1698',
            'preQualifier': '',
            'preDirection': '',
            'preType': '',
            'streetName': 'PENNSYLVANIA',
            'suffixType': 'AVE',
            'suffixDirection': 'SE',
            'suffixQualifier': '',
            'city': 'WASHINGTON',
            'state': 'DC',
            'zip': '20003'},
        'geographies': {
            '2010 Census Blocks': [{
                'SUFFIX': '',
                'GEOID': '110010068022013',
                'CENTLAT': '+38.8798010',
                'BLOCK': '2013',
                'AREAWATER': 0,
                'STATE': '11',
                'BASENAME': '2013',
                'OID': 210403964789891,
                'LSADC': 'BK',
                'FUNCSTAT': 'S',
                'INTPTLAT': '+38.8798010',
                'STGEOMETRY.AREA': 23260.527,
                'STGEOMETRY.LEN': 958.01,
                'NAME': 'Block 2013',
                'OBJECTID': 936586,
                'TRACT': '006802',
                'CENTLON': '-076.9828471',
                'BLKGRP': '2',
                'AREALAND': 14076,
                'INTPTLON': '-076.9828471',
                'MTFCC': 'G5040',
                'LWBLKTYP': 'L',
                'COUNTY': '001'
            }],
            'States': [{
                'STATENS': '01702382',
                'GEOID': '11',
                'CENTLAT': '+38.9047577',
                'AREAWATER': 18687196,
                'BASENAME': 'District of Columbia',
                'STATE': '11',
                'STUSAB': 'DC',
                'OID': 27490331294090,
                'LSADC': '00',
                'FUNCSTAT': 'A',
                'INTPTLAT': '+38.9041031',
                'DIVISION': '5',
                'STGEOMETRY.AREA': 292745184.0,
                'STGEOMETRY.LEN': 86300.65,
                'NAME': 'District of Columbia',
                'REGION': '3',
                'OBJECTID': 54,
                'CENTLON': '-077.0162863',
                'AREALAND': 158340390,
                'INTPTLON': '-077.0172290',
                'MTFCC': 'G4000'
            }],
            'Counties': [{
                'GEOID': '11001',
                'CENTLAT': '+38.9047577',
                'AREAWATER': 18687196,
                'BASENAME': 'District of Columbia',
                'STATE': '11',
                'OID': 27590331264532,
                'LSADC': '00',
                'FUNCSTAT': 'F',
                'INTPTLAT': '+38.9041031',
                'STGEOMETRY.AREA': 292745184.0,
                'STGEOMETRY.LEN': 86300.65,
                'NAME': 'District of Columbia',
                'OBJECTID': 632,
                'CENTLON': '-077.0162863',
                'COUNTYCC': 'H6',
                'COUNTYNS': '01702382',
                'AREALAND': 158340390,
                'INTPTLON': '-077.0172290',
                'MTFCC': 'G4020',
                'COUNTY': '001'
            }],
            'Census Tracts': [{
                'GEOID': '11001006802',
                'CENTLAT': '+38.8832158',
                'AREAWATER': 0,
                'BASENAME': '68.02',
                'STATE': '11',
                'OID': 20790331304268,
                'LSADC': 'CT',
                'FUNCSTAT': 'S',
                'INTPTLAT': '+38.8832158',
                'STGEOMETRY.AREA': 462925.4,
                'STGEOMETRY.LEN': 3235.1487,
                'NAME': 'Census Tract 68.02',
                'OBJECTID': 47582,
                'TRACT': '006802',
                'CENTLON': '-076.9814483',
                'AREALAND': 280108,
                'INTPTLON': '-076.9814483',
                'MTFCC': 'G5020',
                'COUNTY': '001'
            }]
        }
    }
]

locations_resp = [{
                      'matchedAddress': '1600 PENNSYLVANIA AVE NW, WASHINGTON, DC, 20500',
                      'coordinates': {
                        'x': -77.03535,
                        'y': 38.898754
                      },
                      'tigerLine': {
                        'tigerLineId': '76225813',
                        'side': 'L'
                      },
                      'addressComponents': {
                        'fromAddress': '1600',
                        'toAddress': '1698',
                        'preQualifier': '',
                        'preDirection': '',
                        'preType': '',
                        'streetName': 'PENNSYLVANIA',
                        'suffixType': 'AVE',
                        'suffixDirection': 'NW',
                        'suffixQualifier': '',
                        'city': 'WASHINGTON',
                        'state': 'DC',
                        'zip': '20500'
                      }
                    }, {
                      'matchedAddress': '1600 PENNSYLVANIA AVE SE, WASHINGTON, DC, 20003',
                      'coordinates': {
                        'x': -76.981895,
                        'y': 38.87898
                      },
                      'tigerLine': {
                        'tigerLineId': '638666807',
                        'side': 'L'
                      },
                      'addressComponents': {
                        'fromAddress': '1600',
                        'toAddress': '1698',
                        'preQualifier': '',
                        'preDirection': '',
                        'preType': '',
                        'streetName': 'PENNSYLVANIA',
                        'suffixType': 'AVE',
                        'suffixDirection': 'SE',
                        'suffixQualifier': '',
                        'city': 'WASHINGTON',
                        'state': 'DC',
                        'zip': '20003'
                      }
                    }]

coord_resp = {
              '2010 Census Blocks': [{
                'SUFFIX': '',
                'GEOID': '110010062021092',
                'CENTLAT': '+38.8888686',
                'BLOCK': '1092',
                'AREAWATER': 30352,
                'STATE': '11',
                'BASENAME': '1092',
                'OID': 210403964787858,
                'LSADC': 'BK',
                'FUNCSTAT': 'S',
                'INTPTLAT': '+38.8886931',
                'STGEOMETRY.AREA': 221344.39,
                'STGEOMETRY.LEN': 2851.458,
                'NAME': 'Block 1092',
                'OBJECTID': 1695655,
                'TRACT': '006202',
                'CENTLON': '-077.0444327',
                'BLKGRP': '1',
                'AREALAND': 103558,
                'INTPTLON': '-077.0452079',
                'MTFCC': 'G5040',
                'LWBLKTYP': 'B',
                'COUNTY': '001',
                'CENT': (-77.0444327, 38.8888686),
                'INTPT': (-77.0452079, 38.8886931)
              }],
              'States': [{
                'STATENS': '01702382',
                'GEOID': '11',
                'CENTLAT': '+38.9047577',
                'AREAWATER': 18687196,
                'BASENAME': 'District of Columbia',
                'STATE': '11',
                'STUSAB': 'DC',
                'OID': 27490331294090,
                'LSADC': '00',
                'FUNCSTAT': 'A',
                'INTPTLAT': '+38.9041031',
                'DIVISION': '5',
                'STGEOMETRY.AREA': 292745184.0,
                'STGEOMETRY.LEN': 86300.65,
                'NAME': 'District of Columbia',
                'REGION': '3',
                'OBJECTID': 54,
                'CENTLON': '-077.0162863',
                'AREALAND': 158340390,
                'INTPTLON': '-077.0172290',
                'MTFCC': 'G4000',
                'CENT': (-77.0162863, 38.9047577),
                'INTPT': (-77.017229, 38.9041031)
              }],
              'Counties': [{
                'GEOID': '11001',
                'CENTLAT': '+38.9047577',
                'AREAWATER': 18687196,
                'BASENAME': 'District of Columbia',
                'STATE': '11',
                'OID': 27590331264532,
                'LSADC': '00',
                'FUNCSTAT': 'F',
                'INTPTLAT': '+38.9041031',
                'STGEOMETRY.AREA': 292745184.0,
                'STGEOMETRY.LEN': 86300.65,
                'NAME': 'District of Columbia',
                'OBJECTID': 632,
                'CENTLON': '-077.0162863',
                'COUNTYCC': 'H6',
                'COUNTYNS': '01702382',
                'AREALAND': 158340390,
                'INTPTLON': '-077.0172290',
                'MTFCC': 'G4020',
                'COUNTY': '001',
                'CENT': (-77.0162863, 38.9047577),
                'INTPT': (-77.017229, 38.9041031)
              }],
              'Census Tracts': [{
                'GEOID': '11001006202',
                'CENTLAT': '+38.8801546',
                'AREAWATER': 4970897,
                'BASENAME': '62.02',
                'STATE': '11',
                'OID': 20790331304119,
                'LSADC': 'CT',
                'FUNCSTAT': 'S',
                'INTPTLAT': '+38.8809933',
                'STGEOMETRY.AREA': 19021758.0,
                'STGEOMETRY.LEN': 34175.344,
                'NAME': 'Census Tract 62.02',
                'OBJECTID': 47245,
                'TRACT': '006202',
                'CENTLON': '-077.0352173',
                'AREALAND': 6539770,
                'INTPTLON': '-077.0363219',
                'MTFCC': 'G5020',
                'COUNTY': '001',
                'CENT': (-77.0352173, 38.8801546),
                'INTPT': (-77.0363219, 38.8809933)
              }]
            }

batch_resp = [
    OrderedDict([
        ('id', '1'), ('address', '908 N Washtenaw, Chicago, IL, 60622'), ('match', True),
        ('matchtype', 'Non_Exact'), ('parsed', '908 N WASHTENAW AVE, CHICAGO, IL, 60622'),
        ('tigerlineid', '605058427'), ('side', 'L'), ('statefp', '17'), ('countyfp', '031'),
        ('tract', '242600'), ('block', '4008'), ('lon', -87.6943), ('lat', 41.897907)]),
    OrderedDict([
        ('id', '2'), ('address', '1405 Wilshire Blvd, Austin, TX, 78722'), ('match', True),
        ('matchtype', 'Exact'), ('parsed', '1405 WILSHIRE BLVD, AUSTIN, TX, 78722'),
        ('tigerlineid', '63947400'), ('side', 'R'), ('statefp', '48'), ('countyfp', '453'),
        ('tract', '000307'), ('block', '1033'), ('lon', -97.71405), ('lat', 30.296574)]),
    OrderedDict([
        ('id', '3'), ('address', '908 N Washtenaw, Chicago, IL, 60622'), ('match', True),
        ('matchtype', 'Non_Exact'), ('parsed', '908 N WASHTENAW AVE, CHICAGO, IL, 60622'),
        ('tigerlineid', '605058427'), ('side', 'L'), ('statefp', '17'), ('countyfp', '031'),
        ('tract', '242600'), ('block', '4008'), ('lon', -87.6943), ('lat', 41.897907)]),
    OrderedDict([
        ('id', '4'), ('address', '1405 Wilshire Blvd, Austin, TX, 78722'), ('match', True),
        ('matchtype', 'Exact'), ('parsed', '1405 WILSHIRE BLVD, AUSTIN, TX, 78722'),
        ('tigerlineid', '63947400'), ('side', 'R'), ('statefp', '48'), ('countyfp', '453'),
        ('tract', '000307'), ('block', '1033'), ('lon', -97.71405), ('lat', 30.296574)]),
    OrderedDict([
        ('id', '5'), ('address', '908 N Washtenaw, Chicago, IL, 60622'), ('match', True),
        ('matchtype', 'Non_Exact'), ('parsed', '908 N WASHTENAW AVE, CHICAGO, IL, 60622'),
        ('tigerlineid', '605058427'), ('side', 'L'), ('statefp', '17'), ('countyfp', '031'),
        ('tract', '242600'), ('block', '4008'), ('lon', -87.6943), ('lat', 41.897907)])]
