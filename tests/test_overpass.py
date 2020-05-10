from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder

def assertForQueryResult(minElements=100, overpassKwargs={}, **kwargs):
  print(kwargs)
  overpass = Overpass()
  y = overpass.query(overpassQueryBuilder(**kwargs), **overpassKwargs)
  assert y.isValid()
  assert len(y.elements()) > minElements
  assert len(y.elements()) == y.countElements()
  assert len(y.nodes()) >= 0
  assert len(y.nodes()) == y.countNodes()
  assert len(y.ways()) >= 0
  assert len(y.ways()) == y.countWays()
  assert len(y.relations()) >= 0
  assert len(y.relations()) == y.countRelations()
  assert len(y.areas()) >= 0
  assert len(y.areas()) == y.countAreas()
  assert y.countNodes() + y.countWays() + y.countRelations() + y.countAreas() == y.countElements()
  assert y.toJSON()
  assert y.version() > 0
  assert y.generator()
  assert y.timestamp_osm_base()
  assert y.copyright()
  return y

def test_queryAreaID():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  assertForQueryResult(area=x.areaId(), elementType='node', selector='"highway"="bus_stop"', out='body')

def test_queryAreaIDTimeout():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  assertForQueryResult(area=x.areaId(), elementType='node', selector='"highway"="bus_stop"', out='body', overpassKwargs={'timeout': 25})

def test_queryAreaIDTimeout():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  assertForQueryResult(area=x.areaId(), elementType='node', selector='"highway"="bus_stop"', out='body', overpassKwargs={'date': '2017-01-01T00:00:00Z'})

def test_queryBbox():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  assertForQueryResult(bbox=[52.1, 6.7, 52.3, 6.9], elementType='node', selector='"highway"="bus_stop"', out='body')

def test_queryAreaIDGeometry():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  y = assertForQueryResult(area=x.areaId(), elementType='node', selector='"highway"="bus_stop"', out='body', includeGeometry=True)
  assert (y.nodes()[0].lat() - 52.2) < .5
  assert (y.nodes()[0].lon() - 6.8) < .5

def test_queryBboxGeometry():
  nominatim = Nominatim()
  x = nominatim.query('Enschede')
  y = assertForQueryResult(bbox=[52.1, 6.7, 52.3, 6.9], elementType='node', selector='"highway"="bus_stop"', out='body')
  assert (y.nodes()[0].lat() - 52.2) < .5
  assert (y.nodes()[0].lon() - 6.8) < .5

def test_queryAreaIDSelector():
  nominatim = Nominatim()
  x = nominatim.query('Dublin')
  assertForQueryResult(minElements=5, area=x.areaId(), elementType=['node', 'way'], selector=['"name"~"Tesco"', 'opening_hours'])
