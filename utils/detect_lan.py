from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0
print(detect("Humorprogram och reality-tv står i förgrunden"))
