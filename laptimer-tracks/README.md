# LapTimer Tracks - Worldwide Database

Source: racingcircuits.info + TrackAddict TrackList + Wikipedia List of motor racing tracks (5172 lines) + f1db + bacinger/f1-circuits

## Files
- tracks_world_2000.json - 2000 tracks (full list, placeholder lat/lon to be geocoded)
- tracks_world_200.json - 86 tracks with accurate S/F coordinates (ready for ESP32)
- tracks_world.json - 61 core tracks
- tracks_asia.json - 28 Asia tracks (Thailand 6 included)
- tracks_asia_full.json - 128 Asia (with kart tracks)
- tracks_europe.json - Europe
- tracks_north_america.json - NA
- tracks_south_america.json - SA
- tracks_oceania.json - Oceania
- tracks_africa.json - Africa
- tracks_index.json - short index for ESP32 menu

## For racingcircuits.info maps
racingcircuits.info provides SVG track maps, not GPS. To get GPS outline:
1. Use Overpass API: [out:json];way[name="Sepang International Circuit"];out geom;
2. Or use openstreetmap.org export
3. Or use your own GPS logging lap to create mapPoints

## ESP32 usage
See previous code: downloadToSD() + loadTrackFromSD()

## Thailand tracks included
- Buriram/Chang 14.9628444,103.0849972
- Bira 12.92139,101.00917
- Thailand Circuit 13.9118444,100.1678694
- Kaeng Krachen 12.94194,99.70694
- Bangsaen Street 13.3058,100.9045
- Bonanza 14.555,101.475
