#!/usr/bin/env python
"""Blind benchmark per PREDICTION.md section 3 (registered 2026-11-17).

Registered line: log10(hippocampus_cm3) = -1.6609 + 0.8467 * log10(brain_cm3)

Test set: published hippocampus volumes NOT among the Brain Catalogue's 37
specimens and NOT lion/leopard (section 4).
  Primary: Reep, Finlay & Darlington 2007, Brain Behav Evol 70:57-70, Table 1
    (full text: Cornell CDN PDF, opened and transcribed 2026-11-17).
    Brain volume operationalization (declared): sum of the row's 11 printed
    regional components, mm3 -> cm3. Hippocampus = 9th component.
  Compilation: Patzke et al. 2015, Brain Struct Funct 220:361-383, Table 1
    (PMC8734557 author manuscript, opened and transcribed 2026-11-17).
    Brain volume = Vb as printed (ml; Vb = Mb/1.036 per the paper).
    Species also in Reep Table 1 (source code 3) are graded on Reep values
    only, never double-counted. Multiple specimen rows per species averaged.

Comparator graded: Patzke et al. 2015 exponential model, as published:
  ln(Vh) = 9.26 * (0.72 - exp(-0.097 * ln(Vb)))   [fit to log-transformed data;
  natural-log reading verified numerically against the paper's Table 1 values]
Karbowski 2007: NOT graded - the paper publishes no hippocampal volume
  equation (its -0.14 exponent is for volume-specific glucose metabolic rate).
"""
import csv, math
from statistics import median, mean

# ---------------------------------------------------------------- Reep 2007
# components (mm3): Medulla, Cerebellum, Mesencephalon, Diencephalon, Striatum,
# Septum, Amygdala, Paleocortex, Hippocampus, Schizocortex, Isocortex
REEP = {
 # common name, scientific name, specimen, [11 components]
 "Coyote": ("Canis latrans", "62-301", [3392.64, 6244.80, 1818.72, 3256.32, 1847.04, 144.48, 849.12, 2272.32, 2158.56, 1603.68, 49435.68]),
 "Red fox": ("Vulpes vulpes", "63-392", [1841.76, 4112.64, 1315.68, 1966.08, 1002.72, 108.00, 395.52, 960.48, 1288.32, 594.72, 24216.48]),
 "Fennec": ("Fennecus zerda", "63-388", [957.12, 1860.00, 632.64, 895.68, 510.72, 51.84, 213.12, 510.24, 485.76, 335.04, 8302.08]),
 "Polar bear": ("Ursus maritimus", "62-256", [20285.28, 61999.68, 7129.92, 14129.28, 9889.92, 617.28, 1947.36, 7370.40, 5588.64, 2806.08, 259556.64]),
 "Crab-eating raccoon": ("Procyon cancrivorus", "68-312", [1596.96, 4155.84, 765.60, 1942.08, 1039.68, 107.04, 291.84, 812.16, 1025.76, 565.92, 24555.36]),
 "Coatimundi": ("Nasua nasua", "58-360", [1088.16, 3335.04, 615.36, 1395.36, 1239.84, 48.96, 295.20, 836.16, 494.40, 281.28, 14564.16]),
 "Olingo": ("Bassaricyon gabbii", "62-113", [683.52, 1795.20, 496.32, 1016.64, 811.20, 57.12, 191.52, 575.52, 579.36, 512.64, 9030.72]),  # isocortex printed "90,30.72" -> 9030.72
 "Least weasel": ("Mustela nivalis", "63-10", [149.76, 298.56, 92.16, 148.32, 74.88, 9.60, 17.28, 73.44, 168.00, 42.24, 994.08]),
 "Badger": ("Taxidea taxus", "63-127", [1912.80, 4135.20, 1037.28, 2561.28, 2120.64, 118.56, 422.40, 1641.12, 1447.68, 865.92, 26457.12]),
 "Striped skunk": ("Mephitis mephitis", "57-226", [462.24, 1201.92, 206.40, 445.92, 349.44, 28.32, 116.64, 456.96, 312.00, 180.48, 4053.60]),
 "Spotted hyena": ("Crocuta crocuta", "64-352", [7089.12, 14094.72, 3419.52, 6756.48, 5801.28, 336.00, 1471.20, 3902.88, 3080.64, 2154.24, 92500.80]),
 "Mountain lion": ("Felis concolor", "60-206", [5176.32, 12413.28, 2940.00, 4935.36, 3000.00, 259.20, 855.36, 2014.08, 1798.56, 1082.88, 70327.68]),
 "Leopard": ("Panthera pardus", "63-261", [7482.24, 16028.16, 4802.40, 6180.48, 3809.28, 235.68, 1355.04, 2855.04, 3121.44, 2155.20, 85872.96]),  # EXCLUDED: section 4
 "African lion": ("Panthera leo", "62-79", [11861.76, 32487.36, 6199.20, 8932.32, 3633.60, 422.40, 1578.72, 3082.56, 4496.16, 1324.80, 157070.40]),  # EXCLUDED: section 4
 "Northern fur seal": ("Callorhinus ursinus", "61-512", [10992.00, 40414.56, 4153.44, 12811.68, 6391.20, 391.68, 905.28, 2115.84, 1953.12, 1680.00, 186232.80]),
 "California sea lion": ("Zalophus californianus", "62-294", [13046.04, 73013.64, 5225.22, 12072.48, 9367.26, 501.06, 1253.28, 2638.44, 2328.48, 2367.96, 263153.10]),
 "Stellar sea lion": ("Eumetopias jubatus", "61-513", [20610.04, 93486.80, 5423.00, 14465.00, 9214.04, 310.20, 1760.00, 3355.00, 3530.12, 2509.76, 359900.20]),
 "Harbor seal": ("Phoca vitulina", "61-515", [9209.82, 33550.68, 3720.12, 10289.78, 6096.96, 348.58, 932.06, 1838.02, 2113.52, 2545.04, 169256.18]),
 "Collared peccary": ("Tayassu tajacu", "63-445", [2386.08, 6330.24, 1769.28, 2726.88, 2506.08, 169.92, 544.32, 1881.60, 2667.84, 1023.84, 28429.44]),
 "Llama": ("Lama glama", "65-139", [8955.36, 22925.76, 6617.76, 7921.92, 7429.44, 310.56, 1191.36, 2737.92, 3524.16, 1693.44, 99180.00]),
 "Camel": ("Camelus dromedarius", "60-227", [26781.12, 70519.68, 14904.00, 19111.68, 21388.32, 768.96, 3966.24, 7468.80, 8577.12, 3760.32, 375959.52]),
 "White-tailed deer": ("Odocoileus virginianus", "67-81", [6521.28, 14463.84, 5060.16, 7130.40, 3750.72, 406.08, 1048.80, 3132.48, 3259.68, 2596.80, 68266.08]),
 "Zebu": ("Bos taurus indicus", "64-322", [17187.84, 41459.04, 12054.72, 20231.04, 17609.28, 444.96, 3838.08, 9524.64, 7708.32, 5050.08, 362993.76]),
 "Zebra": ("Equus burchelli", "61-820", [18975.36, 47924.64, 12012.00, 16176.48, 15858.72, 541.44, 2971.20, 7879.68, 10334.88, 3980.16, 294262.56]),  # EXCLUDED: catalogue Plains_zebra
 "Giant anteater": ("Myrmecophaga tridactyla", "67-29", [3816.96, 8314.08, 1813.92, 3568.80, 2063.52, 163.20, 425.28, 2377.92, 2684.64, 915.84, 19503.36]),
 "Collared anteater": ("Tamandua tetradactyla", "61-93", [1287.84, 3420.48, 720.00, 1439.52, 1505.76, 94.56, 216.48, 1189.92, 1070.40, 425.28, 8075.52]),
 "Two-toed sloth": ("Choloepus didactylis", "61-98", [1009.92, 2654.40, 693.12, 1569.60, 1802.88, 84.00, 241.44, 1374.24, 1138.08, 354.72, 8702.40]),
 "Nine-banded armadillo": ("Dasypus novemcinctus", "60-465", [883.68, 1880.64, 432.00, 628.32, 491.04, 89.28, 126.24, 949.44, 927.84, 303.36, 1718.88]),
 "Florida manatee": ("Trichechus manatus", "84-49", [13635.54, 44297.28, 5456.70, 12847.68, 9130.86, 194.40, 1101.60, 2403.54, 3634.20, 1459.08, 188861.22]),  # diencephalon printed "1,2847.68" -> 12847.68
}
REEP_EXCLUDED = {"Leopard": "PREDICTION.md section 4 (already seen)",
                 "African lion": "PREDICTION.md section 4 (already seen)",
                 "Zebra": "Brain Catalogue specimen (Plains_zebra)"}

# ------------------------------------------------------- Patzke et al. 2015
# (name as printed, Mb g, Vb ml, Vh ml, source code)
# S: 1 Pirlot & Nelson 1978, 2 Stephan et al. 1981, 3 Reep et al. 2007,
#    4 Montie et al. 2008, 5 Patzke et al. current study, 6 Baron et al. 1996
PATZKE = [
 ("Ornithorhynchus anatinus", 9.17, 8.85, 0.51, 1),
 ("Tachyglossus aculeatus", 27.52, 26.56, 1.77, 1),
 ("Didelphis marsupialis", 6.89, 6.65, 0.53, 1),
 ("Solenodon paradoxus", 4.67, 4.51, 0.30, 2),
 ("Tenrec ecaudatus", 2.57, 2.48, 0.15, 2),
 ("Setifer setosus", 1.51, 1.46, 0.10, 2),
 ("Hemicentetes semispinosus", 0.83, 0.80, 0.06, 2),
 ("Echinops telfairi", 0.62, 0.60, 0.05, 2),
 ("Oryzorictes talpoides", 0.58, 0.56, 0.06, 2),
 ("Microgale cowani", 0.42, 0.41, 0.04, 2),
 ("Limnogale mergulus", 1.15, 1.11, 0.08, 2),
 ("Nesogale dobsoni", 0.56, 0.54, 0.07, 2),
 ("Nesogale talazaci", 0.79, 0.76, 0.10, 2),
 ("Micropotamogale lamottei", 0.80, 0.077, 0.08, 2),
 ("Potamogale velox", 4.16, 4.02, 0.30, 2),
 ("Chlorotalpa stuhlmanni", 0.74, 0.71, 0.06, 2),
 ("Chrysochloris asiatica", 0.70, 0.68, 0.07, 2),
 ("Aethechinus algirus", 3.20, 3.09, 0.23, 2),
 ("Erinaceus europaeus", 3.35, 3.23, 0.24, 2),
 ("Hemiechinus auritus", 1.90, 1.83, 0.13, 2),
 ("Sorex minutus", 0.11, 0.10, 0.01, 2),
 ("Sorex araneus", 0.20, 0.19, 0.02, 2),
 ("Neomys fodiens", 0.32, 0.31, 0.03, 2),
 ("Crocidura occidentalis", 0.44, 0.43, 0.04, 2),
 ("Crocidura russula", 0.19, 0.18, 0.02, 2),
 ("Suncus murinus", 0.38, 0.37, 0.03, 2),
 ("Talpa europaea", 1.02, 0.98, 0.09, 2),
 ("Desmana moschata", 4.00, 3.86, 0.27, 2),
 ("Galemys pyrenaicus", 1.33, 1.28, 0.11, 2),
 ("Elephantulus fuscipes", 1.33, 1.28, 0.17, 2),
 ("Rhynchocyon stuhlmanni", 6.10, 5.89, 0.58, 2),
 ("Tupaia glis", 3.20, 3.09, 0.15, 2),
 ("Tupaia minor", 2.58, 2.49, 0.13, 2),
 ("Urogale everetti", 4.28, 4.13, 0.17, 2),
 ("Cheirogaleus major", 6.80, 6.56, 0.35, 2),
 ("Cheirogaleus medius", 3.14, 3.03, 0.17, 2),
 ("Microcebus murinus", 1.78, 1.72, 0.10, 2),
 ("Lepilemur ruficaudatus", 7.60, 7.34, 0.39, 2),
 ("Lemur fulvus", 23.30, 22.49, 0.75, 2),
 ("Lemur variegatus", 31.50, 30.41, 1.40, 2),
 ("Avahi laniger", 10.49, 10.13, 0.53, 2),
 ("Avahi occidentalis", 9.67, 9.33, 0.48, 2),
 ("Propithecus verreauxi", 26.70, 25.77, 1.04, 2),
 ("Indri indri", 38.30, 36.97, 1.52, 2),
 ("Daubentonia madagascarie.", 45.15, 43.58, 1.78, 2),
 ("Loris tardigradus", 6.60, 6.37, 0.19, 2),
 ("Nycticebus coucang", 12.50, 12.07, 0.57, 2),
 ("Perodicticus potto", 14.00, 13.51, 0.61, 2),
 ("Galago crassicaudatus", 10.30, 9.94, 0.46, 2),
 ("Galago demidovii", 3.38, 3.26, 0.15, 2),
 ("Galago senegalensis", 4.80, 4.63, 0.26, 2),
 ("Tarsius sp.", 3.60, 3.47, 0.15, 2),
 ("Callithrix jacchus", 7.60, 7.34, 0.22, 2),
 ("Cebuella pygmaea", 4.50, 4.34, 0.13, 2),
 ("Saguinus oedipus", 10.00, 9.65, 0.26, 2),
 ("Saguinus tamarin", 10.30, 9.94, 0.28, 2),
 ("Callimico goeldii", 11.00, 10.61, 0.28, 2),
 ("Aotus trivirgatus", 17.10, 16.51, 0.54, 2),
 ("Callicebus moloch", 19.00, 18.34, 0.59, 2),
 ("Pithecia monachal", 35.00, 33.78, 0.83, 2),
 ("Alouatta sp.", 52.00, 50.19, 1.32, 2),
 ("Ateles geoffroyi", 108.00, 104.25, 1.37, 2),
 ("Lagothrix lagotricha", 101.00, 97.49, 1.59, 2),
 ("Cebus sp.", 71.00, 68.53, 0.89, 2),
 ("Saimiri sciureus", 24.00, 23.17, 0.35, 2),
 ("Macaca mulatta", 93.00, 89.77, 1.35, 2),
 ("Cercocebus albigena", 104.00, 100.39, 1.49, 2),
 ("Papio anubis", 201.00, 194.02, 3.40, 2),
 ("Cercopithecus mitis", 75.00, 72.39, 1.37, 2),
 ("Cercopithecus ascanius", 67.00, 64.67, 1.19, 2),
 ("Cercopithecus talapoin", 40.00, 38.61, 0.71, 2),
 ("Erythrocebus patas", 108.00, 104.25, 1.59, 2),
 ("Pygathrix nemaeus", 77.00, 74.32, 2.30, 2),
 ("Nasalis larvatus", 97.00, 93.63, 1.97, 2),
 ("Colobus badius", 78.00, 75.29, 1.67, 2),
 ("Hylobates lar", 102.00, 98.46, 2.67, 2),
 ("Pan troglodytes", 405.00, 390.93, 3.78, 2),
 ("Gorilla gorilla", 500.00, 482.63, 4.78, 2),
 ("Homo sapiens", 1330.00, 1283.78, 10.29, 2),
 ("Canis latrans", 88.30, 85.23, 2.16, 3),
 ("Vulpes vulpes", 43.50, 41.99, 1.29, 3),
 ("Fennicus zerda", 17.30, 16.70, 0.49, 3),
 ("Ursus maritimus", 458.60, 442.66, 5.59, 3),
 ("Procyon cancrivorous", 61.56, 59.42, 1.03, 3),
 ("Nasau nasau", 37.00, 35.71, 0.49, 3),
 ("Bassaricyon gabbi", 19.30, 18.63, 0.58, 3),
 ("Mustela nivalis", 1.50, 1.45, 0.17, 3),
 ("Taxidea taxus", 49.00, 47.29, 1.45, 3),
 ("Mephitis mephitis", 10.30, 9.94, 0.31, 3),
 ("Crocuta crocuta", 162.50, 156.85, 3.08, 3),
 ("Felis concolor", 125.50, 121.14, 1.80, 3),
 ("Felis pardis", 125.50, 121.14, 3.12, 3),
 ("Panthera leo", 258.00, 249.03, 4.50, 3),
 ("Zalophus californianus", 379.13, 365.96, 2.33, 3),
 ("Callorhinus ursinus", 328.75, 317.33, 1.95, 3),
 ("Eumetopius jubatus", 661.25, 638.27, 3.53, 3),
 ("Phoca vitulina", 275.00, 265.44, 2.11, 3),
 ("Tayassu tajacu", 80.50, 77.70, 2.67, 3),
 ("Lama glama", 200.30, 193.34, 3.52, 3),
 ("Camelus dromedarius", 518.00, 500.00, 8.58, 3),
 ("Odocoileus virginianus", 160.00, 154.44, 3.26, 3),
 ("Bos indicus", 474.00, 457.53, 7.71, 3),
 ("Hippopotamus amphibius", 579.40, 559.27, 6.81, 5),
 ("Hippopotamus amphibius", 407.50, 393.34, 3.63, 5),
 ("Lagenorhynchus acutus", 1292.20, 1253.90, 1.61, 4),
 ("Lagenorhynchus acutus", 1329.70, 1293.60, 1.67, 4),
 ("Lagenorhynchus acutus", 1305.30, 1255.20, 1.91, 4),
 ("Phocoena phocoena", 503.00, 485.52, 0.60, 5),
 ("Phocoena phocoena", 486.00, 469.11, 0.60, 5),
 ("Tursiops truncatus", 1530.00, 1476.83, 1.05, 5),
 ("Balaenoptera acutorostrata", 2900.00, 2799.23, 1.43, 5),
 ("Balaenoptera acutorostrata", 2800.00, 2702.70, 1.42, 5),
 ("Equus burchelli", 254.99, 246.13, 10.34, 3),
 ("Diceros bicornus", 531.00, 512.55, 7.48, 5),
 ("Myrmechophaga tridactyla", 58.80, 56.76, 2.69, 3),
 ("Tamandua tetradactyla", 24.00, 23.17, 1.07, 3),
 ("Choloepus didactylus", 25.93, 25.03, 1.14, 3),
 ("Dasypus novemcinctus", 16.25, 15.68, 0.93, 3),
 ("Eidolon helvum", 4.29, 4.14, 0.26, 6),
 ("Rousettus aegyptiacus", 2.28, 2.20, 0.15, 6),
 ("Rousettus amplexicaudatus", 1.35, 1.31, 0.10, 6),
 ("Rousettus amplexicaudatus", 1.72, 1.66, 0.13, 6),
 ("Myonycteris torquata", 1.16, 1.12, 0.09, 6),
 ("Pteropus alecto", 7.04, 6.79, 0.36, 6),
 ("Pteropus conspicillatus", 8.35, 8.06, 0.39, 6),
 ("Pteropus hypomelanus", 5.30, 5.12, 0.28, 6),
 ("Pteropus lylei", 6.13, 5.92, 0.29, 6),
 ("Pteropus mahaganus", 5.28, 5.10, 0.28, 6),
 ("Pteropus neohibernicus", 9.11, 8.80, 0.40, 6),
 ("Pteropus poliocephalus", 7.23, 7.00, 0.36, 6),
 ("Pteropus samoensis", 5.79, 5.59, 0.32, 6),
 ("Pteropus scapulatus", 5.36, 5.17, 0.27, 6),
 ("Pteropus temmincki", 4.89, 4.72, 0.28, 6),
 ("Pteropus tonganus", 6.08, 5.87, 0.31, 6),
 ("Pteropus vampyrus", 9.12, 8.80, 0.44, 6),
 ("Dobsonia inermis", 2.70, 2.61, 0.19, 6),
 ("Dobsonia moluccensis", 5.34, 5.16, 0.32, 6),
 ("Dobsonia moluccensis", 3.83, 3.70, 0.24, 6),
 ("Dobsonia praedatrix", 3.01, 2.92, 0.18, 6),
 ("Hypsignathus monstrosus", 3.48, 3.36, 0.22, 6),
 ("Epomops franqueti", 2.21, 2.13, 0.16, 6),
 ("Epomophorus labiatus", 1.59, 1.53, 0.11, 6),
 ("Micropteropus pusillus", 0.83, 0.80, 0.06, 6),
 ("Scotonycteris zenkeri", 0.71, 0.69, 0.07, 6),
 ("Casinycteris argynnis", 0.84, 0.81, 0.07, 6),
 ("Cynopterus brachyotis", 0.98, 0.95, 0.08, 6),
 ("Cynopterus horsfieldi", 1.37, 1.33, 0.11, 6),
 ("Megaerops ecaudatus", 0.80, 0.77, 0.07, 6),
 ("Chironax melanocephalus", 0.61, 0.59, 0.06, 6),
 ("Sphaeris blanfordi", 0.83, 0.80, 0.07, 6),
 ("Balionycteris maculata", 0.51, 0.49, 0.06, 6),
 ("Nyctimene albiventer", 0.83, 0.80, 0.07, 6),
 ("Nyctimene robinsoni", 1.23, 1.19, 0.10, 6),
 ("Nyctimene vizcaccia", 0.99, 0.95, 0.07, 6),
 ("Harpiocephalus hapria", 0.44, 0.43, 0.04, 6),
 ("Paranyctimene raptor", 0.73, 0.71, 0.06, 6),
 ("Eonycteris spelaean", 1.31, 1.26, 0.10, 6),
 ("Megaloglossus woermanni", 0.68, 0.66, 0.06, 6),
 ("Macroglossus minimus", 0.56, 0.54, 0.05, 6),
 ("Macroglossus sobrinus", 0.69, 0.67, 0.06, 6),
 ("Syconycteris sp.", 0.57, 0.55, 0.05, 6),
 ("Syconycteris sp.", 0.63, 0.61, 0.06, 6),
 ("Melonyceris melanops", 1.29, 1.25, 0.08, 6),
 ("Nesonycteris woodfordi", 1.02, 0.98, 0.07, 6),
 ("Notopteris macdonaldi", 1.46, 1.14, 0.10, 6),
 ("Rhinopoma hardwickei", 0.28, 0.27, 0.02, 6),
 ("Rhinopoma microphyllum", 0.39, 0.37, 0.03, 6),
 ("Emballonura monticola", 0.17, 0.16, 0.01, 6),
 ("Emballonura raffrayana", 0.17, 0.17, 0.01, 6),
 ("Emballonura semicaudata", 0.18, 0.18, 0.01, 6),
 ("Coleura afra", 0.26, 0.25, 0.01, 6),
 ("Rhynchonycteris naso", 0.12, 0.11, 0.01, 6),
 ("Saccopteryx bilineata", 0.23, 0.22, 0.01, 6),
 ("Saccopteryx canescens", 0.13, 0.13, 0.01, 6),
 ("Saccopteryx leptura", 0.16, 0.16, 0.01, 6),
 ("Cormura brevirostris", 0.22, 0.21, 0.01, 6),
 ("Peropteryx macrotis", 0.16, 0.16, 0.01, 6),
 ("Peropteryx trinitatis", 0.14, 0.13, 0.01, 6),
 ("Taphozous australis", 0.52, 0.50, 0.03, 6),
 ("Taphozous hildegardeae", 0.55, 0.53, 0.03, 6),
 ("Taphozous mauritianus", 0.55, 0.53, 0.03, 6),
 ("Taphozous melanopogon", 0.54, 0.52, 0.02, 6),
 ("Taphozous theobaldi", 0.68, 0.66, 0.03, 6),
 ("Cyttarops alecto", 0.18, 0.17, 0.01, 6),
 ("Craseonycteris thonglongyai", 0.09, 0.08, 0.01, 6),
 ("Nycteris arge", 0.35, 0.34, 0.02, 6),
 ("Nycteris grandis", 0.71, 0.68, 0.04, 6),
 ("Nycteris hispida", 0.28, 0.27, 0.02, 6),
 ("Nycteris javanica", 0.47, 0.45, 0.03, 6),
 ("Nycteris nana", 0.24, 0.23, 0.02, 6),
 ("Nycteris thebaica", 0.32, 0.31, 0.02, 6),
 ("Nycteris tragata", 0.46, 0.44, 0.02, 6),
 ("Megaderma lyra", 0.91, 0.88, 0.04, 6),
 ("Megaderma spasma", 0.64, 0.62, 0.03, 6),
 ("Macroderma gigas", 1.70, 1.65, 0.07, 6),
 ("Cardioderma cor", 0.67, 0.65, 0.03, 6),
 ("Lavia frons", 0.64, 0.62, 0.03, 6),
 ("Rhinolophus cornutus", 0.19, 0.19, 0.02, 6),
 ("Rhinolophus eloquens", 0.40, 0.39, 0.03, 6),
 ("Rhinolophus hipposerdos", 0.15, 0.14, 0.01, 6),
 ("Rhinolophus landeri", 0.28, 0.27, 0.02, 6),
 ("Rhinolophus lepidus", 0.19, 0.18, 0.01, 6),
 ("Rhinolophus luctus", 0.62, 0.60, 0.03, 6),
 ("Rhinolophus macrotis", 0.21, 0.20, 0.02, 6),
 ("Rhinolophus malayanus", 0.20, 0.19, 0.01, 6),
 ("Rhinolophus megaphyllus", 0.26, 0.25, 0.02, 6),
 ("Rhinolophus megaphyllus", 0.23, 0.22, 0.02, 6),
 ("Rhinolophus paradoxolo.", 0.27, 0.26, 0.02, 6),
 ("Rhinolophus pearsoni", 0.33, 0.32, 0.03, 6),
 ("Rhinolophus pusillus", 0.16, 0.16, 0.01, 6),
 ("Rhinolophus trifoliatus", 0.35, 0.34, 0.02, 6),
 ("Rhinolophus yunanensis", 0.44, 0.42, 0.03, 6),
 ("Hipposideros armiger", 0.80, 0.77, 0.05, 6),
 ("Hipposideros calcaratus", 0.40, 0.39, 0.03, 6),
 ("Hipposideros calcaratus", 0.34, 0.32, 0.02, 6),
 ("Hipposideros cervinus", 0.21, 0.21, 0.01, 6),
 ("Hipposideros commersoni", 0.75, 0.72, 0.05, 6),
 ("Hipposideros diadema", 0.71, 0.69, 0.05, 6),
 ("Hipposideros fulvus", 0.24, 0.23, 0.02, 6),
 ("Hipposideros halophyllus", 0.15, 0.15, 0.01, 6),
 ("Hipposideros lankadiva", 0.73, 0.71, 0.05, 6),
 ("Hipposideros larvatus", 0.41, 0.40, 0.03, 6),
 ("Hipposideros lekaguli", 0.55, 0.53, 0.04, 6),
 ("Hipposideros maggietaylor.", 0.63, 0.61, 0.04, 6),
 ("Hipposideros maggietaylor.", 0.45, 0.44, 0.03, 6),
 ("Hipposideros ridleyi", 0.27, 0.26, 0.02, 6),
 ("Hipposideros sperois", 0.28, 0.027, 0.02, 6),
 ("Hipposideros turpis", 0.60, 0.58, 0.04, 6),
 ("Asellicus stoliczkanus", 0.15, 0.15, 0.01, 6),
 ("Asellicus tricuspidatus", 0.13, 0.13, 0.01, 6),
 ("Rhinonycteris aurantius", 0.25, 0.24, 0.02, 6),
 ("Triaenops persicus", 0.27, 0.26, 0.02, 6),
 ("Noctilio albiventris", 0.60, 0.58, 0.02, 6),
 ("Noctilio leporinus", 1.18, 1.14, 0.05, 6),
 ("Pteronotus gymnonotus", 0.34, 0.33, 0.02, 6),
 ("Pteronotus personatus", 0.23, 0.22, 0.01, 6),
 ("Pteronotus parnelli", 0.54, 0.52, 0.04, 6),
 ("Mormoops megalophylla", 0.39, 0.37, 0.03, 6),
 ("Micronycteris megalotis", 0.27, 0.26, 0.01, 6),
 ("Micronycteris minuta", 0.29, 0.28, 0.02, 6),
 ("Micronycteris schmidtorum", 0.31, 0.30, 0.01, 6),
 ("Micronycteris brachyotis", 0.41, 0.39, 0.02, 6),
 ("Macrophyllum macrophyll.", 0.32, 0.31, 0.02, 6),
 ("Tonatia bidens", 0.79, 0.76, 0.04, 6),
 ("Tonatia schulzi", 0.51, 0.49, 0.02, 6),
 ("Tonatia sylvicola", 0.76, 0.73, 0.03, 6),
 ("Mimon crenulatum", 0.32, 0.31, 0.02, 6),
 ("Phyllostomus discolor", 1.09, 1.05, 0.08, 6),
 ("Phyllostomus elongates", 0.89, 0.85, 0.05, 6),
 ("Phyllostomus hastatus", 1.52, 1.46, 0.08, 6),
 ("Phylloderma stenops", 1.34, 1.29, 0.09, 6),
 ("Trachops cirrhosus", 1.00, 0.97, 0.05, 6),
 ("Vampyrum spectrum", 2.59, 2.50, 0.11, 6),
 ("Glossophaga longirostris", 0.44, 0.42, 0.04, 6),
 ("Glossphaga soricina", 0.39, 0.38, 0.03, 6),
 ("Monophyllus plethodon", 0.45, 0.43, 0.03, 6),
 ("Leptonycteris curasoae", 0.61, 0.59, 0.05, 6),
 ("Leptonycteris nivalis", 0.59, 0.57, 0.04, 6),
 ("Lonchophylla mordax", 0.43, 0.42, 0.04, 6),
 ("Lonchophylla thomasi", 0.34, 0.33, 0.03, 6),
 ("Lionycteris spurrelli", 0.35, 0.34, 0.03, 6),
 ("Anoura caudifer", 0.41, 0.39, 0.03, 6),
 ("Anoura geoffroyi", 0.59, 0.57, 0.05, 6),
 ("Choeroniscus minor", 0.39, 0.38, 0.04, 6),
 ("Carollia castanea", 0.45, 0.44, 0.04, 6),
 ("Carollia perspicullata", 0.55, 0.53, 0.04, 6),
 ("Rhinophylla pumilio", 0.36, 0.34, 0.03, 6),
 ("Sturnira lilium", 0.62, 0.60, 0.05, 6),
 ("Strunira ludovici", 0.68, 0.65, 0.05, 6),
 ("Sturnira tildae", 0.70, 0.68, 0.05, 6),
 ("Uroderma bilobatum", 0.61, 0.59, 0.04, 6),
 ("Vampyrops helleri", 0.52, 0.50, 0.03, 6),
 ("Vampyrops infuscus", 1.11, 1.07, 0.08, 6),
 ("Vampyrops lineatus", 0.74, 0.72, 0.05, 6),
 ("Vampyrops vittatus", 1.18, 1.13, 0.07, 6),
 ("Vampyrodes caraccioloi", 0.95, 0.91, 0.06, 6),
 ("Vampyressa pusilla", 0.38, 0.37, 0.03, 6),
 ("Chiroderma salvini", 0.81, 0.79, 0.06, 6),
 ("Chiroderma trinitatum", 0.54, 0.52, 0.03, 6),
 ("Chiroderma villosum", 0.71, 0.68, 0.04, 6),
 ("Chiroderma villosum", 0.84, 0.81, 0.06, 6),
 ("Echtophylla macconnelli", 0.34, 0.33, 0.03, 6),
 ("Artibeus concolor", 0.63, 0.61, 0.04, 6),
 ("Artibeus jamaicensis", 1.02, 0.98, 0.06, 6),
 ("Artibeus lituratus", 1.23, 1.19, 0.08, 6),
 ("Enchisthenes harti", 0.51, 0.49, 0.04, 6),
 ("Ardops sp.", 0.57, 0.55, 0.04, 6),
 ("Sphaeronycteris toxophyll.", 0.52, 0.51, 0.03, 6),
 ("Brachyphylla cavernarum", 1.20, 1.15, 0.08, 6),
 ("Desmodus rotundus", 1.00, 0.96, 0.04, 6),
 ("Diphylla ecaudata", 0.80, 0.77, 0.04, 6),
 ("Natalus tumidirostris", 0.25, 0.24, 0.03, 6),
 ("Furipterus horrens", 0.13, 0.12, 0.01, 6),
 ("Myotis adversus", 0.25, 0.25, 0.01, 6),
 ("Myotis albescens", 0.13, 0.12, 0.01, 6),
 ("Myotis altarium", 0.24, 0.23, 0.02, 6),
 ("Myotis annectans", 0.22, 0.21, 0.02, 6),
 ("Myotis bechsteini", 0.27, 0.26, 0.03, 6),
 ("Myotis bocagei", 0.19, 0.18, 0.01, 6),
 ("Myotis dasycneme", 0.31, 0.30, 0.03, 6),
 ("Myotis montivagus", 0.17, 0.16, 0.01, 6),
 ("Myotis myotis", 0.49, 0.47, 0.04, 6),
 ("Myotis nattereri", 0.22, 0.21, 0.02, 6),
 ("Myotis nigricans", 0.14, 0.13, 0.01, 6),
 ("Myotis nigricans", 0.16, 0.15, 0.01, 6),
 ("Myotis siligorensis", 0.10, 0.10, 0.01, 6),
 ("Pipistrellus babu", 0.10, 0.09, 0.01, 6),
 ("Pipistrellus ceylonicus", 0.18, 0.18, 0.01, 6),
 ("Pipistrellus circumdatus", 0.23, 0.22, 0.02, 6),
 ("Pipistrellus crassulus", 0.13, 0.13, 0.01, 6),
 ("Pipistrellus imbricatus", 0.14, 0.13, 0.01, 6),
 ("Pipistrellus javanicus", 0.12, 0.12, 0.01, 6),
 ("Pipistrellus mimus", 0.09, 0.09, 0.01, 6),
 ("Pipistrellus nanus", 0.10, 0.10, 0.01, 6),
 ("Pipistrellus papuanus", 0.11, 0.11, 0.01, 6),
 ("Pipistrellus pulveratus", 0.14, 0.14, 0.01, 6),
 ("Pipistrellus subflavus", 0.13, 0.12, 0.01, 6),
 ("Scotozous dormeri", 0.14, 0.14, 0.01, 6),
 ("Nyctalus noctula", 0.36, 0.35, 0.02, 6),
 ("Nyctalus stenopterus", 0.24, 0.24, 0.01, 6),
 ("Glischropus tylopus", 0.10, 0.10, 0.01, 6),
 ("Eptesicus brasiliensis", 0.20, 0.19, 0.01, 6),
 ("Eptesicus brasiliensis", 0.20, 0.19, 0.01, 6),
 ("Eptesicus flavenscens", 0.19, 0.18, 0.01, 6),
 ("Eptesicus fuscus", 0.24, 0.23, 0.02, 6),
 ("Eptesicus pumilis", 0.12, 0.12, 0.01, 6),
 ("Ia io", 0.76, 0.74, 0.05, 6),
 ("Tylonycteris pachypus", 0.08, 0.08, 0.01, 6),
 ("Tylonycteris robustula", 0.12, 0.11, 0.01, 6),
 ("Hesperopterus blandfordi", 0.16, 0.15, 0.01, 6),
 ("Glauconycteris poensis", 0.21, 0.20, 0.01, 6),
 ("Chalinolobus gouldi", 0.24, 0.23, 0.02, 6),
 ("Chalinolobus morio", 0.18, 0.18, 0.02, 6),
 ("Scotorepens sanborni", 0.16, 0.15, 0.01, 6),
 ("Rhogessa parvula", 0.11, 0.11, 0.01, 6),
 ("Scotomanes ornatus", 0.38, 0.37, 0.03, 6),
 ("Scotomanes sp.", 0.34, 0.33, 0.03, 6),
 ("Scotophilus dinganii", 0.44, 0.42, 0.02, 6),
 ("Scotophilus heathi", 0.48, 0.46, 0.03, 6),
 ("Scotophilus kuhli", 0.34, 0.33, 0.02, 6),
 ("Lasiurus borealis", 0.17, 0.16, 0.01, 6),
 ("Miniopterus australis", 0.20, 0.20, 0.02, 6),
 ("Miniopterus haradai", 0.22, 0.22, 0.02, 6),
 ("Miniopterus inflatus", 0.33, 0.31, 0.02, 6),
 ("Miniopterus magnater", 0.32, 0.31, 0.02, 6),
 ("Miniopterus medius", 0.27, 0.26, 0.02, 6),
 ("Miniopterus pusillus", 0.22, 0.21, 0.02, 6),
 ("Miniopterus tristis", 0.33, 0.32, 0.02, 6),
 ("Murina cyclotis", 0.25, 0.24, 0.02, 6),
 ("Murina cyclotis", 0.28, 0.27, 0.02, 6),
 ("Murina huttoni", 0.26, 0.25, 0.02, 6),
 ("Murina turbinaris", 0.22, 0.21, 0.02, 6),
 ("Kerivoula papillosa", 0.31, 0.30, 0.04, 6),
 ("Kerivoula pellucida", 0.20, 0.20, 0.01, 6),
 ("Kerivoula phalaena", 0.12, 0.11, 0.01, 6),
 ("Phoniscus atrox", 0.19, 0.18, 0.03, 6),
 ("Nyctophilus geoffroyi", 0.17, 0.16, 0.01, 6),
 ("Nyctophilus timoriensis", 0.25, 0.25, 0.02, 6),
 ("Tadarida aegyptiaca", 0.39, 0.38, 0.02, 6),
 ("Tadarida condylura", 0.46, 0.44, 0.02, 6),
 ("Tadarida mops", 0.48, 0.46, 0.03, 6),
 ("Tadarida niveiventer", 0.43, 0.42, 0.02, 6),
 ("Tadarida beccarii", 0.23, 0.23, 0.01, 6),
 ("Tadarida jobensis", 0.36, 0.35, 0.02, 6),
 ("Tadarida leucostigma", 0.39, 0.38, 0.02, 6),
 ("Tadarida plicata", 0.45, 0.43, 0.02, 6),
 ("Tadarida plicata", 0.33, 0.31, 0.01, 6),
 ("Otomops martiensseni", 0.76, 0.73, 0.03, 6),
 ("Molossops abrasus", 0.42, 0.40, 0.02, 6),
 ("Molossops greenhalli", 0.30, 0.29, 0.01, 6),
 ("Molossops planirostris", 0.19, 0.18, 0.01, 6),
 ("Eumops auripendulus", 0.61, 0.59, 0.03, 6),
 ("Eumops glaucinus", 0.65, 0.63, 0.03, 6),
 ("Molossus ater", 0.53, 0.51, 0.02, 6),
 ("Molussus molossus", 0.32, 0.31, 0.02, 6),
 ("Molossus trinitatus", 0.44, 0.42, 0.02, 6),
 ("Cheiromeles torquatus", 1.36, 1.32, 0.06, 6),
 ("Loxodonta africana", 5145.00, 4966.22, 11.21, 5),
 ("Loxodonta africana", 5250.00, 5067.57, 10.74, 5),
 ("Loxodonta africana", 4835.00, 4666.99, 10.57, 5),
 ("Trichechus manatus", 350.00, 337.84, 3.63, 3),
]

# Patzke rows excluded at species level: Brain Catalogue specimens + felids of section 4
PATZKE_EXCLUDED = {
 "Ornithorhynchus anatinus": "Brain Catalogue: Platypus",
 "Nycticebus coucang": "Brain Catalogue: Slow_loris",
 "Galago demidovii": "Brain Catalogue: Demidoff's_dwarf_Galago (Galagoides demidoff)",
 "Aotus trivirgatus": "Brain Catalogue: Night_monkey",
 "Macaca mulatta": "Brain Catalogue: Rhesus_macaque",
 "Cercocebus albigena": "Brain Catalogue: Grey-cheeked_mangabey (Lophocebus albigena)",
 "Papio anubis": "Brain Catalogue: Baboon (Papio sp.; species overlap cannot be excluded)",
 "Pan troglodytes": "Brain Catalogue: Chimpanzee",
 "Gorilla gorilla": "Brain Catalogue: Gorilla",
 "Homo sapiens": "Brain Catalogue: Human",
 "Hylobates lar": "Brain Catalogue: Gibbon",
 "Cebus sp.": "Brain Catalogue: White-headed_capuchin (Cebus capucinus) - genus-level entry, excluded conservatively",
 "Tursiops truncatus": "Brain Catalogue: Bottlenose_dolphin",
 "Diceros bicornus": "Brain Catalogue: Black_rhinoceros (Diceros bicornis)",
 "Equus burchelli": "Brain Catalogue: Plains_zebra",
 "Panthera leo": "PREDICTION.md section 4 (already seen)",
 "Felis pardis": "PREDICTION.md section 4 (already seen; leopard)",
}
# Patzke source-code-3 rows duplicate Reep Table 1 (graded on Reep values instead)
REEP_SCI = {v[0] for v in REEP.values()}
PATZKE_NAME2REEP = {  # Patzke printed name -> Reep scientific name, for cross-check
 "Canis latrans": "Canis latrans", "Vulpes vulpes": "Vulpes vulpes",
 "Fennicus zerda": "Fennecus zerda", "Ursus maritimus": "Ursus maritimus",
 "Procyon cancrivorous": "Procyon cancrivorus", "Nasau nasau": "Nasua nasua",
 "Bassaricyon gabbi": "Bassaricyon gabbii", "Mustela nivalis": "Mustela nivalis",
 "Taxidea taxus": "Taxidea taxus", "Mephitis mephitis": "Mephitis mephitis",
 "Crocuta crocuta": "Crocuta crocuta", "Felis concolor": "Felis concolor",
 "Zalophus californianus": "Zalophus californianus",
 "Callorhinus ursinus": "Callorhinus ursinus",
 "Eumetopius jubatus": "Eumetopias jubatus", "Phoca vitulina": "Phoca vitulina",
 "Tayassu tajacu": "Tayassu tajacu", "Lama glama": "Lama glama",
 "Camelus dromedarius": "Camelus dromedarius",
 "Odocoileus virginianus": "Odocoileus virginianus",
 "Bos indicus": "Bos taurus indicus",
 "Myrmechophaga tridactyla": "Myrmecophaga tridactyla",
 "Tamandua tetradactyla": "Tamandua tetradactyla",
 "Choloepus didactylus": "Choloepus didactylis",
 "Dasypus novemcinctus": "Dasypus novemcinctus",
 "Trichechus manatus": "Trichechus manatus",
}
SRCNAME = {1: "Pirlot & Nelson 1978", 2: "Stephan et al. 1981", 3: "Reep et al. 2007",
           4: "Montie et al. 2008", 5: "Patzke et al. 2015 (current study)",
           6: "Baron et al. 1996"}

def our_pred(brain_cm3):
    return 10 ** (-1.6609 + 0.8467 * math.log10(brain_cm3))

def patzke_pred(brain_cm3):
    # ln(Vh) = 9.26 * (0.72 - exp(-0.097 * ln(Vb))), Patzke et al. 2015, as published
    return math.exp(9.26 * (0.72 - math.exp(-0.097 * math.log(brain_cm3))))

def score(rows):
    """rows: list of dicts with obs, our, pat. Returns metric dict."""
    out = {}
    for key, lab in (("our", "registered line"), ("pat", "Patzke 2015 exponential")):
        se = [100.0 * (r[key] - r["obs"]) / r["obs"] for r in rows]
        ae = [abs(x) for x in se]
        out[lab] = {"n": len(rows), "medianAPE": median(ae), "meanAPE": mean(ae),
                    "meanSigned": mean(se)}
    wins = sum(1 for r in rows if abs(100*(r["our"]-r["obs"])/r["obs"]) < abs(100*(r["pat"]-r["obs"])/r["obs"]))
    ties = sum(1 for r in rows if abs(100*(r["our"]-r["obs"])/r["obs"]) == abs(100*(r["pat"]-r["obs"])/r["obs"]))
    out["head2head"] = {"our_wins": wins, "patzke_wins": len(rows) - wins - ties, "ties": ties}
    return out

def main():
    log = []
    # ---- validate Patzke transcription: checksum Vb == Mb/1.036
    # fail only when the discrepancy exceeds both the table's 2-dp rounding
    # (0.01 ml) and 1% relative (the largest brains show ~0.5% internal
    # inconsistency in the printed table, e.g. the Lagenorhynchus rows)
    checksum_fail = []
    for name, mb, vb, vh, s in PATZKE:
        if abs(vb - mb / 1.036) > max(0.01, 0.01 * vb):
            checksum_fail.append((name, mb, vb, vh, s))
    log.append(f"Patzke checksum failures (Vb != Mb/1.036): {len(checksum_fail)}")
    for f in checksum_fail:
        log.append(f"  FAIL {f}")
    fail_names = {f[0] for f in checksum_fail}

    # ---- cross-check Reep hippocampus vs Patzke source-3 rows
    reep_by_sci = {v[0]: v[2][8] / 1000.0 for v in REEP.values()}
    pat_by_name = {}
    for name, mb, vb, vh, s in PATZKE:
        if s == 3:
            pat_by_name[name] = vh
    mism = []
    for pname, rsci in PATZKE_NAME2REEP.items():
        if pname in pat_by_name and rsci in reep_by_sci:
            if abs(pat_by_name[pname] - reep_by_sci[rsci]) > 0.006:
                mism.append((pname, pat_by_name[pname], reep_by_sci[rsci]))
    log.append(f"Reep-vs-Patzke hippocampus cross-check mismatches (>0.006 cm3): {mism}")

    rows = []          # benchmark rows
    # ---- Reep primary subset
    reep_patzke_vb = {}  # sensitivity: Patzke Vb for Reep species
    for name, mb, vb, vh, s in PATZKE:
        if s == 3 and name in PATZKE_NAME2REEP:
            reep_patzke_vb[PATZKE_NAME2REEP[name]] = vb
    for common, (sci, spec, comps) in REEP.items():
        if common in REEP_EXCLUDED:
            continue
        brain = sum(comps) / 1000.0
        obs = comps[8] / 1000.0
        rows.append({"species": f"{common} ({sci})", "subset": "Reep2007_primary",
                     "source": f"Reep et al. 2007 Table 1, specimen {spec}",
                     "brain": brain, "obs": obs, "our": our_pred(brain),
                     "pat": patzke_pred(brain),
                     "alt_brain": reep_patzke_vb.get(sci)})

    # ---- Patzke compilation subset (species not already graded from Reep)
    grouped = {}
    for name, mb, vb, vh, s in PATZKE:
        if name in PATZKE_EXCLUDED or name in fail_names:
            continue
        if s == 3:
            continue  # duplicates Reep Table 1; graded on Reep values
        grouped.setdefault(name, []).append((vb, vh, s))
    for name, vals in sorted(grouped.items()):
        brain = mean([v[0] for v in vals])
        obs = mean([v[1] for v in vals])
        srcs = sorted({SRCNAME[v[2]] for v in vals})
        rows.append({"species": name, "subset": "Patzke2015_compilation",
                     "source": "Patzke et al. 2015 Table 1 ("
                               + "; ".join(srcs) + ")"
                               + (f"; mean of {len(vals)} specimen rows" if len(vals) > 1 else ""),
                     "brain": brain, "obs": obs, "our": our_pred(brain),
                     "pat": patzke_pred(brain), "alt_brain": None})

    # ---- scorecards
    full = score(rows)
    reep_rows = [r for r in rows if r["subset"] == "Reep2007_primary"]
    pat_rows = [r for r in rows if r["subset"] == "Patzke2015_compilation"]
    blind_names = {"Lagenorhynchus acutus", "Phocoena phocoena",
                   "Balaenoptera acutorostrata", "Loxodonta africana",
                   "Hippopotamus amphibius"}
    blind = [r for r in rows if r["species"].split(" (")[0] in blind_names
             or r["species"].startswith("Florida manatee")]
    sub_reep, sub_pat, sub_blind = score(reep_rows), score(pat_rows), score(blind)

    # sensitivity: Reep subset with Patzke mass-derived Vb as brain volume
    alt_rows = []
    for r in reep_rows:
        if r["alt_brain"]:
            alt_rows.append({"obs": r["obs"], "our": our_pred(r["alt_brain"]),
                             "pat": patzke_pred(r["alt_brain"])})
    sub_alt = score(alt_rows) if alt_rows else None

    def fmt(tag, sc):
        o, p = sc["registered line"], sc["Patzke 2015 exponential"]
        return (f"{tag}: n={o['n']} | ours medianAPE={o['medianAPE']:.2f}% "
                f"meanSigned={o['meanSigned']:+.2f}% | Patzke medianAPE={p['medianAPE']:.2f}% "
                f"meanSigned={p['meanSigned']:+.2f}% | W-L-T ours vs Patzke = "
                f"{sc['head2head']['our_wins']}-{sc['head2head']['patzke_wins']}-{sc['head2head']['ties']}")
    log.append(fmt("FULL SET", full))
    log.append(fmt("REEP ONLY", sub_reep))
    log.append(fmt("PATZKE COMPILATION ONLY", sub_pat))
    log.append(fmt("BOTH-BLIND (Patzke fit-excluded groups)", sub_blind))
    if sub_alt:
        log.append(fmt("SENSITIVITY Reep w/ Patzke Vb", sub_alt))
    log.append(f"Test set: {len(rows)} species (Reep {len(reep_rows)}, Patzke {len(pat_rows)})")
    # ---- post-hoc diagnostics (NOT part of the registered scorecard):
    # where does the line fail - by brain-size band, and inside its fit range?
    for lo, hi in ((0, 2), (2, 20), (20, 1e9)):
        band = [r for r in rows if lo <= r["brain"] < hi]
        if band:
            log.append(fmt(f"DIAG brain {lo}-{hi if hi < 1e9 else 'inf'} cm3", score(band)))
    inrange = [r for r in rows if 5.0 <= r["brain"] <= 450.0]
    log.append(fmt("DIAG inside registered fit range 5-450 cm3", score(inrange)))
    reep_big = [r for r in reep_rows if r["brain"] >= 20]
    reep_small = [r for r in reep_rows if r["brain"] < 20]
    log.append(fmt("DIAG Reep brain>=20", score(reep_big)))
    log.append(fmt("DIAG Reep brain<20", score(reep_small)))
    print("\n".join(log))

    # ---- write CSV
    with open("outputs/benchmark_testset.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["species", "subset", "source", "brain_vol_cm3",
                    "published_hippocampus_cm3", "our_prediction_cm3",
                    "our_signed_pct_err", "our_abs_pct_err",
                    "patzke2015_prediction_cm3", "patzke2015_signed_pct_err",
                    "patzke2015_abs_pct_err"])
        for r in sorted(rows, key=lambda r: (r["subset"], r["species"])):
            ose = 100 * (r["our"] - r["obs"]) / r["obs"]
            pse = 100 * (r["pat"] - r["obs"]) / r["obs"]
            w.writerow([r["species"], r["subset"], r["source"],
                        f"{r['brain']:.3f}", f"{r['obs']:.3f}",
                        f"{r['our']:.4f}", f"{ose:.2f}", f"{abs(ose):.2f}",
                        f"{r['pat']:.4f}", f"{pse:.2f}", f"{abs(pse):.2f}"])
    # worst rows for the report
    worst = sorted(rows, key=lambda r: -abs(100*(r["our"]-r["obs"])/r["obs"]))[:10]
    print("\nWorst 10 for registered line:")
    for r in worst:
        print(f"  {r['species']}: brain {r['brain']:.2f}, obs {r['obs']:.3f}, "
              f"pred {r['our']:.3f} ({100*(r['our']-r['obs'])/r['obs']:+.1f}%), "
              f"Patzke {r['pat']:.3f} ({100*(r['pat']-r['obs'])/r['obs']:+.1f}%)")
    best = sorted(rows, key=lambda r: abs(100*(r["our"]-r["obs"])/r["obs"]))[:5]
    print("Best 5 for registered line:")
    for r in best:
        print(f"  {r['species']}: obs {r['obs']:.3f}, pred {r['our']:.3f} "
              f"({100*(r['our']-r['obs'])/r['obs']:+.1f}%)")

if __name__ == "__main__":
    main()
