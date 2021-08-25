import math
import changeGPS

tileSize = 256
initialResolution = 2 * math.pi * 6378137 / tileSize
# 156543.03392804062 for tileSize 256 pixels
originShift = 2 * math.pi * 6378137 / 2.0
 # 20037508.342789244


def LatLonToMeters(lat, lon):
    #"Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"
    mx = lon * originShift / 180.0
    my = math.log(math.tan((90 + lat) * math.pi / 360.0)) / (math.pi / 180.0)
    my = my * originShift / 180.0
    return mx, my


def MetersToLatLon(mx, my):
    #"Converts XY point from Spherical Mercator EPSG:900913 to lat/lon in WGS84 Datum"
    lon = (mx / originShift) * 180.0
    lat = (my / originShift) * 180.0
    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
    return lat, lon

def Resolution(zoom):
    #Resolution (meters/pixel) for given zoom level (measured at Equator)
    # return (2 * math.pi * 6378137) / (self.tileSize * 2**zoom)
    return initialResolution / (2 ** zoom)

def PixelsToMeters(px, py, zoom):
    #"Converts pixel coordinates in given zoom level of pyramid to EPSG:900913"
    res = Resolution(zoom)
    mx = px * res - originShift
    my = originShift - py * res
    return mx, my


def MetersToPixels(mx, my, zoom):
    #"Converts EPSG:900913 to pyramid pixel coordinates in given zoom level"
    res = Resolution(zoom)
    px = (mx + originShift) / res
    py = (originShift - my) / res
    return px, py


def PixelsToTile(px, py):
    #"Returns a tile covering region in given pixel coordinates"
    tx = int(math.ceil(px / float(tileSize)) - 1)
    ty = int(math.ceil(py / float(tileSize)) - 1)
    return tx, ty


def PixelsToRaster(px, py, zoom):
    #"Move the origin of pixel coordinates to top-left corner"
    mapSize = tileSize << zoom
    return px, mapSize - py


def MetersToTile(mx, my, zoom):
    #"Returns tile for given mercator coordinates"
    px, py = MetersToPixels(mx, my, zoom)
    return PixelsToTile(px, py)


def TileBounds(tx, ty, zoom):
    #"Returns bounds of the given tile in EPSG:900913 coordinates"
    minx, miny = PixelsToMeters(tx * tileSize, ty * tileSize, zoom)
    maxx, maxy = PixelsToMeters((tx + 1) * tileSize, (ty + 1) * tileSize, zoom)
    return (minx, miny, maxx, maxy)


def TileLatLonBounds(tx, ty, zoom):
    #"Returns bounds of the given tile in latutude/longitude using WGS84 datum"
    bounds = TileBounds(tx, ty, zoom)
    minLat, minLon = MetersToLatLon(bounds[0], bounds[1])
    maxLat, maxLon = MetersToLatLon(bounds[2], bounds[3])
    return (minLat, minLon, maxLat, maxLon)

def ZoomForPixelSize(pixelSize):
    #"Maximal scaledown zoom of the pyramid closest to the pixelSize."
    for i in range(30):
        if pixelSize > Resolution(i):
            return i - 1 if i != 0 else 0  # We don't want to scale up

def GoogleTile(tx, ty, zoom):
    #"Converts TMS tile coordinates to Google Tile coordinates"
    # coordinate origin is moved from bottom-left to top-left corner of the extent
    return tx, (2 ** zoom - 1) - ty


#谷歌下转换经纬度对应的层行列
#param lon 经度
#param lat 维度
#param zoom 在第zoom层进行转换
def GoogleLonLatToXYZ(zoom, lon, lat):
    mx, my = LatLonToMeters(lat, lon)
    tx, ty = MetersToTile(mx, my, zoom)
    return [tx, ty]
    '''n = math.pow(2, zoom)
    tileX = ((lon+180.0)/360.0) * n
    secy = 1 / math.cos(math.radians(lat))
    tany = math.tan(math.radians(lat))
    tileY = (1.0 - (math.log(tany + secy) / math.pipi)) / 2.0 * n
    x = int(tileX)
    y = int(tileY)
    return [x, y]'''

#层行列转经纬度
# param x
# param y
# param z
def GoogleXYZtoLonlat(zoom, tx, ty):
    mx, my = PixelsToMeters(tx * tileSize, ty * tileSize, zoom)
    lat, lon = MetersToLatLon(mx, my)
    return [lon, lat]
    '''n = math.pow(2.0, z)
    lon = x / n * 360.0 - 180.0
    lat = math.atan(math.sin(math.pi * (1 - 2 * y / n)))
    lat = math.degrees(lat)
    return [lon, lat]'''

if __name__ == '__main__':

    #lng = 112.982368
    #lat = 28.244211

    #lat = -36.244273
    #lng = 148.710938
    lat = 24.510
    lng = 114.862
    result1 = GoogleLonLatToXYZ(15,lng,lat)
    print(result1)