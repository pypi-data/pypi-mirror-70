# GEOSYS

[![PyPI-Status](https://img.shields.io/pypi/v/geosys.svg?style=flat-square)](https://pypi.org/project/geosys/)
[![PyPI - Status](https://img.shields.io/pypi/status/geosys?style=flat-square)](https://pypi.org/project/geosys/)
[![PyPI-Versions](https://img.shields.io/pypi/pyversions/geosys.svg?style=flat-square)](https://pypi.org/project/geosys/)
[![GitHub issues](https://img.shields.io/github/issues/ShadowCodeCz/geosys?style=flat-square)](https://github.com/ShadowCodeCz/geosys/issues)
[![Travis (.com) branch](https://img.shields.io/travis/com/ShadowCodeCz/geosys/master?style=flat-square)](https://travis-ci.com/ShadowCodeCz/geosys)
[![GitHub license](https://img.shields.io/github/license/ShadowCodeCz/geosys?style=flat-square)](https://github.com/ShadowCodeCz/geosys/blob/master/LICENSE)

Geosys is the acronym **Geo**logical **Sys**tems. In current version, it is small package which contains only one function.
The function converts GPS coordinates (longitude, latitude and altitude) to cartesian system. Used referenced ellipsoid is [WSG 84] (also known as WGS 1984, EPSG:4326).    


## Installation 
```python
pip install geosys
``` 

## Example
```python
import geosys 

latitude = 49.2002211
longitude = 16.6078411
altitude = 0

vertex = geosys.to_cartesian(latitude, longitude, altitude)

# Vertex attributes
# vertex.x
# vertex.y
# vertex.z

print(vertex)
``` 

```
>>> [4001412.65349505, 1193469.21673459, 4805137.77147738]
``` 



[WSG 84]: https://en.wikipedia.org/wiki/World_Geodetic_System